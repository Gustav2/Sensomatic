from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from . import forms
from django.shortcuts import redirect
from operations.models import Route
from django.contrib.auth.models import User
from datetime import date
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

# Create your views here.
def index_login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None and user.is_superuser == True:
                login(request, user)
                return redirect('dashboard')
            else:
                message = 'Login failed!'
    return render(request, 'index.html', context={'form': form, 'message' : message})

def dashboard(request):
    if request.user.is_authenticated:
        user= User.objects.filter(is_superuser=False)
        routes = Route.objects.all().filter(completed=False, operating_date=date.today())
        return render(request, 'dashboard.html', context= {'routes':routes, 'user':user,})
    else:
        return redirect('index')

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    
@csrf_exempt
def add_driver(request):
    if  request.method=='POST':
        data = json.loads(request.body)
        driver_name = data.get('driver')
        route_id = data.get('id')
        driver_user = User.objects.get(username=driver_name)
        route = Route.objects.get(id=route_id)
        route.user = driver_user
        route.save()
        return JsonResponse({'message': 'Driver assigned successfully'}, status=200)
        