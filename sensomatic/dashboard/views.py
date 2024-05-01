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
# Denne funktion viser loginsiden som kommer fra forms siden
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

# Denne funktion viser dashboardsidan med data fra databasen
def dashboard(request):
    if request.user.is_authenticated:
        user= User.objects.filter(is_superuser=False)
        routes = Route.objects.filter(completed=False, operating_date=date.today())
        return render(request, 'dashboard.html', context= {'routes':routes, 'user':user,})
    else:
        return redirect('index')

# Denne funktion skaber funktionen for logud knappen
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    
# Denne funktion håndterer post requesten som sender den opdaterede kører til databasen
@csrf_exempt
def add_driver(request):
    if  request.method=='POST':
        data = json.loads(request.body)
        driver_name = data.get('driver')
        route_id = data.get('id')
        route = Route.objects.get(id=route_id)
        if driver_name == 'None':
            route.user = None
            route.save()
        else:
            driver_user = User.objects.get(username=driver_name)
            route.user = driver_user
            route.save()
    return JsonResponse({'message': 'Driver assigned successfully'}, status=200)

def setting(request):
    pass

def historik(request):
    user= User.objects.filter(is_superuser=False)
    routes = Route.objects.exclude(operating_date = date.today())
    return render(request, 'historik.html', context= {'routes':routes, 'user':user,})

def storskrald(request):
    pass

def skaldeniveau(request):
    pass