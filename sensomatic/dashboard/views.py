from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from . import forms
from django.shortcuts import redirect
from operations.models import Route
from django.contrib.auth.models import User
from datetime import date

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
        complete_adresslist = []
        for i in routes:
            adresslist = i.adresses["adresses"]
            complete_adresslist.append(adresslist)
        return render(request, 'dashboard.html', context= {'user':user, 'complete_adresslist': complete_adresslist,})
    else:
        return redirect('index')

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    
def add_driver():
    pass #add a driver to the database