from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from . import forms
from django.shortcuts import redirect
from operations.models import Route
from django.contrib.auth.models import User
from datetime import date
from django.views.decorators.csrf import csrf_exempt
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
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                message = 'Login failed!'
    return render(request, 'index.html', context={'form': form, 'message' : message})

def dashboard(request):
    if request.user.is_authenticated:
        user= User.objects.all()
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
        driver_name = request.POST.get('driver')
        print(driver_name)
        route_id = request.POST.get('id')
        print(route_id)
        route = Route.objects.get(id=route_id)
        print(route)
        route.user = driver_name
        route.save()
        