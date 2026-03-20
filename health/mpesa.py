"""M-Pesa Daraja (STK Push) helper utilities.

This module contains helpers for talking to the Safaricom Daraja API.

Configuration is expected to be provided via Django settings (or environment variables):
- MPESA_ENVIRONMENT: "sandbox" or "production" (default: "sandbox")
- MPESA_CONSUMER_KEY
- MPESA_CONSUMER_SECRET
- MPESA_SHORTCODE (Business ShortCode / PayBill)
- MPESA_PASSKEY
- MPESA_CALLBACK_URL (optional - auto-built from request if not provided)
"""

import base64
import json
import urllib.error
import urllib.request
from datetime import datetime

from django.conf import settings


class MpesaConfigError(Exception):
    """Raised when required MPESA settings are missing."""


def _get_setting(name: str, default=None):
    # Prefer explicit Django settings, then environment variables.
    return getattr(settings, name, None) or default


def _discover_ngrok_callback_url(path='/mpesa/callback/') -> str | None:
    """Try to detect an ngrok HTTPS tunnel running locally.

    If the user runs `ngrok http 8000`, ngrok exposes a local API at
    http://127.0.0.1:4040/api/tunnels. We can use that to auto-fill a valid
    callback URL without requiring manual configuration.

    Returns a full https callback URL (including path) or None.
    """
    try:
        with urllib.request.urlopen('http://127.0.0.1:4040/api/tunnels', timeout=2) as resp:
            data = json.load(resp)
            for tunnel in data.get('tunnels', []):
                if tunnel.get('proto') == 'https' and tunnel.get('public_url'):
                    url = tunnel['public_url'].rstrip('/')
                    return f"{url}{path}"
    except Exception:
        return None
    return None


def _sanitize_phone(phone: str) -> str:
    """Normalize phone to the 12-digit format expected by Daraja (e.g. 2547XXXXXXXX)."""
    if not phone:
        raise ValueError('Phone number is required')

    cleaned = ''.join([c for c in phone if c.isdigit()])

    # Support both 07XXXXXXXX and +2547XXXXXXXX formats
    if cleaned.startswith('0') and len(cleaned) == 10:
        cleaned = '254' + cleaned[1:]
    if cleaned.startswith('7') and len(cleaned) == 9:
        cleaned = '254' + cleaned

    if not cleaned.startswith('254'):
        raise ValueError('Phone number must start with 254 and be 12 digits long (e.g. 2547XXXXXXXX)')

    if len(cleaned) != 12:
        raise ValueError('Phone number must be 12 digits long (e.g. 2547XXXXXXXX)')

    return cleaned


def _daraja_base_url() -> str:
    env = (_get_setting('MPESA_ENVIRONMENT') or 'sandbox').strip().lower()
    if env == 'production':
        return 'https://api.safaricom.co.ke'
    return 'https://sandbox.safaricom.co.ke'


def _fetch_access_token() -> dict:
    """Fetch an access token from Daraja using consumer key/secret.

    Returns:
        dict: Raw parsed JSON response from Daraja, which includes at least
            "access_token" and "expires_in".
    """
    consumer_key = _get_setting('MPESA_CONSUMER_KEY')
    consumer_secret = _get_setting('MPESA_CONSUMER_SECRET')
    if not consumer_key or not consumer_secret:
        raise MpesaConfigError('Missing MPESA_CONSUMER_KEY/MPESA_CONSUMER_SECRET')

    token_url = f"{_daraja_base_url()}/oauth/v1/generate?grant_type=client_credentials"
    auth = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode('utf-8')).decode('utf-8')

    req = urllib.request.Request(
        token_url,
        headers={
            'Authorization': f'Basic {auth}',
            'Accept': 'application/json',
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.load(resp)
            if not data.get('access_token'):
                raise MpesaConfigError('Daraja did not return an access token')
            return data
    except urllib.error.HTTPError as exc:
        message = exc.read().decode(errors='ignore')
        raise MpesaConfigError(f'Failed to get access token: {message}')


def _get_access_token() -> str:
    """Return the access token string (for existing internal use)."""
    return _fetch_access_token().get('access_token')


def mpesa_access_token_info() -> dict:
    """Return a small dict that can be shown in the UI for debugging."""
    try:
        data = _fetch_access_token()
        return {
            'success': True,
            'access_token': data.get('access_token'),
            'expires_in': data.get('expires_in'),
        }
    except MpesaConfigError as exc:
        return {'success': False, 'message': str(exc)}


def mpesa_stk_push(
    phone: str,
    amount: int | str,
    account_reference: str,
    transaction_desc: str | None = None,
    callback_url: str | None = None,
) -> dict:
    """Send an STK Push request to Daraja.

    Returns a dict with:
      - success: bool
      - message: str
      - data: parsed response from Daraja (or error payload)
    """
    try:
        phone = _sanitize_phone(phone)
    except ValueError as exc:
        return {'success': False, 'message': str(exc)}

    try:
        amount_value = int(amount)
    except (TypeError, ValueError):
        return {'success': False, 'message': 'Amount must be an integer'}

    shortcode = _get_setting('MPESA_SHORTCODE')
    passkey = _get_setting('MPESA_PASSKEY')
    if not shortcode or not passkey:
        return {'success': False, 'message': 'Missing MPESA_SHORTCODE / MPESA_PASSKEY in settings'}

    env = (_get_setting('MPESA_ENVIRONMENT') or 'sandbox').strip().lower()

    if not callback_url:
        callback_url = _get_setting('MPESA_CALLBACK_URL') or ''

        # If no explicit callback is provided, try to auto-detect an ngrok tunnel.
        if not callback_url:
            ngrok_url = _discover_ngrok_callback_url(path='/mpesa/callback/')
            if ngrok_url:
                callback_url = ngrok_url
            elif env == 'sandbox':
                # For sandbox, allow localhost HTTP for testing
                callback_url = 'http://127.0.0.1:8000/mpesa/callback/'

    # Daraja requires callback URL to be HTTPS in production.
    if env == 'production' and (not callback_url or not callback_url.startswith('https://')):
        return {
            'success': False,
            'message': (
                'Invalid CallBackURL. Daraja requires a public HTTPS callback URL in production. '
                'Run ngrok and set MPESA_CALLBACK_URL to the HTTPS ngrok URL (e.g. https://xxxx.ngrok.io/mpesa/callback/).'
            ),
            'callback_url': callback_url,
        }

    used_callback_url = callback_url

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode('utf-8')).decode('utf-8')

    payload = {
        'BusinessShortCode': shortcode,
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': amount_value,
        'PartyA': phone,
        'PartyB': shortcode,
        'PhoneNumber': phone,
        'CallBackURL': callback_url,
        'AccountReference': str(account_reference)[:12],
        'TransactionDesc': transaction_desc or str(account_reference),
    }

    access_token = None
    try:
        access_token = _get_access_token()
    except MpesaConfigError as exc:
        return {'success': False, 'message': str(exc)}

    request_url = f"{_daraja_base_url()}/mpesa/stkpush/v1/processrequest"
    req = urllib.request.Request(
        request_url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
            return {
                'success': True,
                'message': 'STK Push initiated',
                'data': data,
                'used_callback_url': used_callback_url,
            }
    except urllib.error.HTTPError as exc:
        try:
            error_data = json.loads(exc.read().decode('utf-8'))
        except Exception:
            error_data = {'error': exc.read().decode(errors='ignore')}
        return {
            'success': False,
            'message': 'STK Push failed',
            'data': error_data,
            'used_callback_url': used_callback_url,
        }
    except Exception as exc:
        return {
            'success': False,
            'message': str(exc),
            'used_callback_url': used_callback_url,
        }
