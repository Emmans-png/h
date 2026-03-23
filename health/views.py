import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date, timedelta
from .models import CalorieLog, UserProfile, WeightLog
from .forms import CalorieForm, CustomUserCreationForm, UserProfileForm, WeightLogForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf import settings
from django.urls import reverse

from .mpesa import mpesa_stk_push, mpesa_access_token_info, _discover_ngrok_callback_url
from .food_dictionary import estimate_calories, categorize_food_enhanced, get_food_info
from .calorie_database import get_calorie_info, search_calorie_foods

def check_weekly_weight_checkin(user):
    """Check if user needs a weekly weight check-in"""
    try:
        profile = user.userprofile
        # Get the most recent weight log
        latest_weight_log = WeightLog.objects.filter(user=user).order_by('-date').first()
        
        if not latest_weight_log:
            return None, "no_weight_logs"
        
        # Calculate days since last weight entry
        days_since_last = (date.today() - latest_weight_log.date).days
        
        # Check if it's been 7 days or more since last weight entry
        if days_since_last >= 7:
            return days_since_last, "due_for_checkin"
        else:
            return days_since_last, "not_due"
            
    except UserProfile.DoesNotExist:
        return None, "no_profile"

def categorize_food(food_name):
    """Automatically categorize food based on name"""
    food_name_lower = food_name.lower()
    
    # Proteins
    protein_keywords = ['beef', 'lobster', 'fish', 'eggs', 'chicken', 'turkey', 'pork', 'lamb', 'meat', 'salmon', 'tuna', 'shrimp', 'bacon', 'sausage', 'steak']
    if any(keyword in food_name_lower for keyword in protein_keywords):
        return 'proteins'
    
    # Carbohydrates
    carb_keywords = ['maize', 'seed', 'rice', 'bread', 'pasta', 'potato', 'corn', 'wheat', 'oats', 'quinoa', 'cereal', 'flour', 'sugar']
    if any(keyword in food_name_lower for keyword in carb_keywords):
        return 'carbohydrates'
    
    # Vitamins (fruits and vegetables)
    vitamin_keywords = ['apple', 'banana', 'orange', 'grape', 'berry', 'vegetable', 'salad', 'carrot', 'broccoli', 'spinach', 'tomato', 'onion', 'garlic', 'pepper', 'cucumber', 'lettuce']
    if any(keyword in food_name_lower for keyword in vitamin_keywords):
        return 'vitamins'
    
    # Default to carbohydrates if no match
    return 'carbohydrates'

def _mask_key(key: str) -> str:
    if not key:
        return ''
    if len(key) <= 8:
        return key
    return f"{key[:4]}...{key[-4:]}"

@login_required(login_url='login')
def tracker_dashboard(request, update_id=None):
    # Check for weekly weight check-in
    days_since_last, checkin_status = check_weekly_weight_checkin(request.user)
    
    # Get user profile and BMR info
    try:
        profile = request.user.userprofile
        user_bmr = profile.bmr
        weight_progress = profile.get_weight_progress_message()
        weight_diff = profile.get_weight_difference()
    except UserProfile.DoesNotExist:
        user_bmr = 0
        weight_progress = "Please complete your profile to calculate BMR"
        weight_diff = 0
    
    # 1. Fetch data for Today's Feed
    today_logs = CalorieLog.objects.filter(user=request.user, date=date.today()).order_by('-id')
    total_calories = today_logs.aggregate(Sum('calories'))['calories__sum'] or 0

    # 2. Fetch Grouped History (Calculates total per day for the sidebar)
    history_summary = (
        CalorieLog.objects.filter(user=request.user)
        .values('date')
        .annotate(day_total=Sum('calories'))
        .order_by('-date')
    )
    
    # 2.5. Fetch nutrition breakdown for today's pie chart
    nutrition_data = (
        today_logs.values('category')
        .annotate(category_total=Sum('calories'))
        .order_by('category')
    )
    
    # 3. Fetch All Logs (To list individual meals under the daily totals)
    all_logs = CalorieLog.objects.filter(user=request.user).order_by('-date', '-id')
    
    # 3.5. Prepare nutrition data for each day in history
    history_nutrition = {}
    for day in history_summary:
        day_logs = all_logs.filter(date=day['date'])
        day_nutrition = (
            day_logs.values('category')
            .annotate(category_total=Sum('calories'))
            .order_by('category')
        )
        # Convert queryset to list of dicts and format date as string
        history_nutrition[str(day['date'])] = list(day_nutrition)

    # 4. Check if this is a new account (no calorie logs at all)
    is_new_user = not CalorieLog.objects.filter(user=request.user).exists()

    # 5. Handle "ADD" and "UPDATE" Actions
    instance = get_object_or_404(CalorieLog, id=update_id, user=request.user) if update_id else None
    
    if request.method == 'POST':
        form = CalorieForm(request.POST, instance=instance)
        if form.is_valid():
            new_log = form.save(commit=False)
            # Auto-categorize and estimate calories using enhanced food dictionary
            food_info = get_food_info(new_log.food_name)
            if food_info:
                new_log.category = food_info['category']
                # Auto-fill calories if not provided or if zero
                if not new_log.calories or new_log.calories == 0:
                    new_log.calories = food_info['calories']
            else:
                # Fallback to enhanced categorization if not in database
                new_log.category = categorize_food_enhanced(new_log.food_name)
                # Auto-estimate calories if not provided or if zero
                if not new_log.calories or new_log.calories == 0:
                    new_log.calories = estimate_calories(new_log.food_name)
            
            new_log.user = request.user 
            new_log.save()             
            return redirect('dashboard')
    else:
        form = CalorieForm(instance=instance)

    # 6. Pass everything to the template
    # Fetch Daraja access token for debugging/display (with error handling)
    mpesa_token = None
    mpesa_token_error = None
    try:
        token_info = mpesa_access_token_info()
        if token_info.get('success'):
            mpesa_token = token_info.get('access_token')
        else:
            mpesa_token_error = token_info.get('message')
    except Exception as e:
        # Handle network errors gracefully without breaking the dashboard
        mpesa_token_error = f"Network error: {str(e)}"

    return render(request, 'health/home.html', {
        'logs': today_logs,
        'total': total_calories,
        'history_summary': history_summary,
        'all_logs': all_logs,
        'form': form,
        'editing': instance,
        'is_new_user': is_new_user,
        'nutrition_data': nutrition_data,
        'history_nutrition': json.dumps(history_nutrition),
        'mpesa_token': mpesa_token,
        'mpesa_token_error': mpesa_token_error,
        'user_bmr': user_bmr,
        'weight_progress': weight_progress,
        'weight_diff': weight_diff,
        'days_since_last': days_since_last,
        'checkin_status': checkin_status,
    })

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

@login_required
def delete_log(request, pk):
    # For now, allow both GET and POST to fix the immediate issue
    # TODO: Restrict to POST only after debugging
    get_object_or_404(CalorieLog, pk=pk, user=request.user).delete()
    return redirect('dashboard')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto-login the new user
            from django.contrib.auth import authenticate, login
            login(request, user)
            return redirect('bmr_setup')
    else:
        form = CustomUserCreationForm()
    return render(request, 'health/signup.html', {'form': form})

@login_required
def bmr_setup(request):
    """Setup user profile with BMR calculation"""
    # Check if user already has a profile
    try:
        profile = request.user.userprofile
        return redirect('dashboard')
    except UserProfile.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            # Calculate BMR
            profile.calculate_bmr()
            profile.save()
            
            # Create initial weight log
            WeightLog.objects.create(
                user=request.user,
                weight=profile.current_weight,
                notes="Initial weight entry during setup"
            )
            
            messages.success(request, f"Your BMR is {profile.bmr} calories per day!")
            return redirect('dashboard')
    else:
        form = UserProfileForm()
    
    return render(request, 'health/bmr_setup.html', {'form': form})

@login_required
def weight_tracking(request):
    """Track weight progress and provide motivational messages"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, "Please complete your profile setup first.")
        return redirect('bmr_setup')
    
    # Get weight logs - ensure latest is always on top
    weight_logs = WeightLog.objects.filter(user=request.user).order_by('-date', '-id')[:10]
    
    if request.method == 'POST':
        form = WeightLogForm(request.POST)
        if form.is_valid():
            weight_log = form.save(commit=False)
            weight_log.user = request.user
            weight_log.save()
            
            # Update user's current weight in profile
            profile.current_weight = weight_log.weight
            profile.calculate_bmr()
            
            # Provide motivational message
            progress_message = profile.get_weight_progress_message()
            
            # Check if this is an AJAX request from the modal
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                from django.http import JsonResponse
                return JsonResponse({'status': 'success', 'message': progress_message})
            
            messages.info(request, progress_message)
            return redirect('weight_tracking')
    else:
        form = WeightLogForm()
    
    # Calculate weight change
    if len(weight_logs) >= 2:
        latest_weight = weight_logs[0].weight
        previous_weight = weight_logs[1].weight
        weight_change = latest_weight - previous_weight
        weight_change_days = (weight_logs[0].date - weight_logs[1].date).days
    else:
        weight_change = 0
        weight_change_days = 0
    
    context = {
        'profile': profile,
        'weight_logs': weight_logs,
        'form': form,
        'weight_change': weight_change,
        'weight_change_days': weight_change_days,
        'progress_message': profile.get_weight_progress_message(),
    }
    
    return render(request, 'health/weight_tracking.html', context)


def products(request):
    return render(request, 'health/products.html')

def community(request):
    return render(request, 'health/community.html')

def mindfuel(request):
    return render(request, 'health/mindfuel.html')

@login_required
def delete_account(request):
    """Handle account deletion with confirmation"""
    if request.method == 'POST':
        # Double-check confirmation
        confirmation = request.POST.get('confirmation', '').lower()
        if confirmation == 'delete my account':
            try:
                # Delete user's data
                user = request.user
                
                # Delete related data (CASCADE should handle this, but let's be explicit)
                CalorieLog.objects.filter(user=user).delete()
                WeightLog.objects.filter(user=user).delete()
                
                # Delete user profile if it exists
                try:
                    user.userprofile.delete()
                except UserProfile.DoesNotExist:
                    pass
                
                # Delete the user account
                user.delete()
                
                # Log out and redirect to home with success message
                from django.contrib.auth import logout
                logout(request)
                
                return render(request, 'health/account_deleted.html')
            except Exception as e:
                messages.error(request, "Error deleting account. Please try again.")
                return redirect('profile')
        else:
            messages.error(request, "Incorrect confirmation. Please type 'delete my account' exactly.")
            return redirect('profile')
    
    return redirect('profile')

@login_required
def profile(request):
    # Calculate user statistics
    user_logs = CalorieLog.objects.filter(user=request.user)
    total_logs = user_logs.count()
    total_calories = user_logs.aggregate(Sum('calories'))['calories__sum'] or 0
    
    # Calculate active days (days with at least one log)
    active_days = user_logs.values('date').distinct().count()
    
    # Calculate average daily calories
    if active_days > 0:
        avg_daily = round(total_calories / active_days)
    else:
        avg_daily = 0
    
    # Find best day (highest calorie count)
    best_day_data = user_logs.values('date').annotate(day_total=Sum('calories')).order_by('-day_total').first()
    best_day = best_day_data['day_total'] if best_day_data else 0
    
    # Calculate current streak (consecutive days with logs)
    from datetime import datetime, timedelta
    today = date.today()
    streak = 0
    current_date = today
    
    while streak < 365:  # Limit to reasonable streak length
        if user_logs.filter(date=current_date).exists():
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
    
    return render(request, 'health/profile.html', {
        'total_logs': total_logs,
        'total_calories': total_calories,
        'active_days': active_days,
        'avg_daily': avg_daily,
        'best_day': best_day,
        'streak': streak,
    })

def contact(request):
    return render(request, 'health/contacts.html')

def about(request):
    return render(request, 'health/about.html')

def food_search_api(request):
    """API endpoint for food search with autocomplete"""
    query = request.GET.get('q', '').lower().strip()
    search_type = request.GET.get('type', 'food')  # 'food' or 'calorie'
    
    if not query:
        return JsonResponse({'foods': [], 'calories': []})
    
    if search_type == 'calorie':
        # Search calorie database
        calorie_results = search_calorie_foods(query)
        return JsonResponse({'foods': [], 'calories': calorie_results})
    else:
        # Search calorie database for food suggestions and auto-fill
        calorie_results = search_calorie_foods(query)
        return JsonResponse({'foods': calorie_results, 'calories': []})


import json
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

@login_required
def mpesa_checkout(request):
    """Render an MPESA checkout page and trigger an STK Push when the form is submitted."""
    product = request.GET.get('product', '').strip()
    amount = request.GET.get('amount', '').strip()

    # Ensure we always have a product and amount to avoid an empty checkout screen
    if not product or not amount:
        messages.error(request, 'Missing product or amount information')
        return redirect('products')

    # Validate amount
    try:
        amount_int = int(amount)
        if amount_int <= 0:
            messages.error(request, 'Amount must be greater than 0')
            return redirect('products')
    except ValueError:
        messages.error(request, 'Invalid amount format')
        return redirect('products')

    callback_url = getattr(settings, 'MPESA_CALLBACK_URL', '') or request.build_absolute_uri(reverse('mpesa_callback'))

    # If callback is a local URL, try auto-detecting ngrok so the user doesn't need to manually
    # copy/paste a URL (if ngrok is running on 127.0.0.1:4040).
    if callback_url.startswith('http://127.0.0.1') or callback_url.startswith('http://localhost'):
        ngrok_url = _discover_ngrok_callback_url(path='/mpesa/callback/')
        if ngrok_url:
            callback_url = ngrok_url

    token_info = mpesa_access_token_info()

    context = {
        'product': product,
        'amount': amount,
        'phone': request.POST.get('phone', '').strip() if request.method == 'POST' else '',
        'success': None,
        'message': None,
        'raw': None,
        'mpesa_callback_url': callback_url,
        'mpesa_env': getattr(settings, 'MPESA_ENVIRONMENT', 'sandbox'),
        'mpesa_key_preview': _mask_key(getattr(settings, 'MPESA_CONSUMER_KEY', '')),
        'mpesa_secret_preview': _mask_key(getattr(settings, 'MPESA_CONSUMER_SECRET', '')),
        'mpesa_token_ok': token_info.get('success'),
        'mpesa_token_message': token_info.get('message'),
    }

    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        
        # Additional client-side validation
        if not phone:
            context['success'] = False
            context['message'] = 'Phone number is required'
            return render(request, 'health/mpesa_checkout.html', context)

        result = mpesa_stk_push(
            phone=phone,
            amount=amount_int,
            account_reference=product,
            transaction_desc=f"Purchase: {product}",
            callback_url=callback_url,
        )
        
        context['success'] = result.get('success', False)
        context['message'] = result.get('message')
        context['raw'] = result.get('data')
        # show the actual URL used when we auto-discover ngrok or other overrides
        context['mpesa_callback_url'] = result.get('used_callback_url') or callback_url

        # Add success message to Django messages framework
        if result.get('success'):
            messages.success(request, f'STK Push sent to {phone}. Please check your phone to complete the payment.')
        else:
            messages.error(request, f'Payment failed: {result.get("message")}')

    return render(request, 'health/mpesa_checkout.html', context)

@login_required
def initiate_stk_push(request):
    """API endpoint used by the frontend to trigger an STK Push via Daraja."""
    if request.method != 'POST':
        return JsonResponse({'status': 'Error', 'message': 'Invalid request method'}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'Error', 'message': 'Invalid JSON'}, status=400)

    phone = (data.get('phone') or '').strip()
    amount = data.get('amount')
    product = data.get('product', 'Item')
    callback_url = data.get('callback_url') or request.build_absolute_uri(reverse('mpesa_callback'))

    result = mpesa_stk_push(
        phone=phone,
        amount=amount,
        account_reference=product,
        transaction_desc=f"Purchase: {product}",
        callback_url=callback_url,
    )

    if result.get('success'):
        return JsonResponse({'status': 'Success', 'message': result.get('message', ''), 'data': result.get('data')})

    return JsonResponse({'status': 'Error', 'message': result.get('message', ''), 'data': result.get('data')}, status=400)

@csrf_exempt
def mpesa_callback(request):
    """Handle Daraja callback from the STK Push request."""
    if request.method != 'POST':
        return JsonResponse({'status': 'Error', 'message': 'Invalid request method'}, status=405)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        payload = request.body.decode(errors='ignore')

    # Log the callback for debugging and reconciliation
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f'MPESA Callback received: {payload}')
    
    # Extract transaction details
    result_code = None
    result_desc = None
    merchant_request_id = None
    checkout_request_id = None
    amount = None
    mpesa_receipt = None
    phone_number = None
    
    try:
        # Parse the callback structure
        if isinstance(payload, dict):
            body = payload.get('Body', {})
            stk_callback = body.get('stkCallback', {})
            
            result_code = stk_callback.get('ResultCode')
            result_desc = stk_callback.get('ResultDesc')
            merchant_request_id = stk_callback.get('MerchantRequestID')
            checkout_request_id = stk_callback.get('CheckoutRequestID')
            
            # Extract callback metadata
            callback_metadata = stk_callback.get('CallbackMetadata', {})
            metadata_items = callback_metadata.get('Item', [])
            
            for item in metadata_items:
                name = item.get('Name')
                value = item.get('Value')
                
                if name == 'Amount':
                    amount = value
                elif name == 'MpesaReceiptNumber':
                    mpesa_receipt = value
                elif name == 'PhoneNumber':
                    phone_number = value
            
            # Log successful transactions
            if result_code == 0:
                logger.info(f'Successful MPESA transaction: Receipt={mpesa_receipt}, Amount={amount}, Phone={phone_number}')
                # TODO: Store transaction in database, update user's purchase status, send confirmation email, etc.
            else:
                logger.warning(f'Failed MPESA transaction: Code={result_code}, Desc={result_desc}, CheckoutID={checkout_request_id}')
                
    except Exception as e:
        logger.error(f'Error parsing MPESA callback: {e}')

    # TODO: Persist callback payload to database/logs for reconciliation
    print('MPESA Callback payload:', payload)

    return JsonResponse({'status': 'Success'})
