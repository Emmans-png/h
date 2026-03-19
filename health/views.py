from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date
from .models import CalorieLog
from .forms import CalorieForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

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
    
    # 3. Fetch All Logs (To list individual meals under the daily totals)
    all_logs = CalorieLog.objects.filter(user=request.user).order_by('-date', '-id')

    # 4. Handle "ADD" and "UPDATE" Actions
    instance = get_object_or_404(CalorieLog, id=update_id, user=request.user) if update_id else None
    
    if request.method == 'POST':
        form = CalorieForm(request.POST, instance=instance)
        if form.is_valid():
            new_log = form.save(commit=False)
            new_log.user = request.user 
            new_log.save()             
            return redirect('dashboard')
    else:
        form = CalorieForm(instance=instance)

    # 5. Pass everything to the template
    return render(request, 'health/home.html', {
        'logs': today_logs,
        'total': total_calories,
        'history_summary': history_summary, # Used for the day headers
        'all_logs': all_logs,               # Used for the meal lists
        'form': form,
        'editing': instance,
    })

@login_required
def delete_log(request, pk):
    get_object_or_404(CalorieLog, pk=pk, user=request.user).delete()
    return redirect('dashboard')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You can now log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'health/signup.html', {'form': form})


def products(request):
    return render(request, 'health/products.html')

def contact(request):
    return render(request, 'health/contacts.html')

def about(request):
    return render(request, 'health/about.html')


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt # Only for testing; better to use CSRF tokens in production
def initiate_stk_push(request):
    if request.method == "POST":
        data = json.loads(request.body)
        phone = data.get('phone')
        amount = data.get('amount')
        
        # This is where your Daraja Python logic goes.
        # For now, we return a success message to stop the error.
        print(f"Requesting {amount} KES from {phone}")
        
        return JsonResponse({"status": "Success", "message": "STK Push Initiated"})
    return JsonResponse({"status": "Error", "message": "Invalid Request"}, status=400)
