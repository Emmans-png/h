import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date
from .models import CalorieLog
from .forms import CalorieForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf import settings
from django.urls import reverse

from .mpesa import mpesa_stk_push, mpesa_access_token_info, _discover_ngrok_callback_url

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
            # Auto-categorize if no category is selected
            if not new_log.category or new_log.category == 'carbohydrates':
                new_log.category = categorize_food(new_log.food_name)
            new_log.user = request.user 
            new_log.save()             
            return redirect('dashboard')
    else:
        form = CalorieForm(instance=instance)

    # 6. Pass everything to the template
    # Fetch Daraja access token for debugging/display
    mpesa_token = None
    mpesa_token_error = None
    token_info = mpesa_access_token_info()
    if token_info.get('success'):
        mpesa_token = token_info.get('access_token')
    else:
        mpesa_token_error = token_info.get('message')

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
    })

@login_required
def delete_log(request, pk):
    get_object_or_404(CalorieLog, pk=pk, user=request.user).delete()
    return redirect('dashboard')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto-login the new user
            from django.contrib.auth import authenticate, login
            login(request, user)
            messages.success(request, "Account created! Welcome to CalorieTracker.")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'health/signup.html', {'form': form})


def products(request):
    return render(request, 'health/products.html')

def community(request):
    return render(request, 'health/community.html')

def mindfuel(request):
    return render(request, 'health/mindfuel.html')

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
        result = mpesa_stk_push(
            phone=context['phone'],
            amount=amount,
            account_reference=product,
            transaction_desc=f"Purchase: {product}",
            callback_url=callback_url,
        )
        context['success'] = result.get('success', False)
        context['message'] = result.get('message')
        context['raw'] = result.get('data')
        # show the actual URL used when we auto-discover ngrok or other overrides
        context['mpesa_callback_url'] = result.get('used_callback_url') or callback_url

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

    # TODO: Persist callback payload to database/logs for reconciliation
    print('MPESA Callback payload:', payload)

    return JsonResponse({'status': 'Success'})
