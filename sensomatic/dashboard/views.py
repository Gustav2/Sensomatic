from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from . import forms
from django.shortcuts import redirect
from operations.models import Route
import json

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
        routes = Route.objects.all().filter(completed=False)
        for i in routes:
            adresslist = i.adresses["adresses"]
            print(adresslist)
        return render(request, 'dashboard.html', context= {'routes':routes, 'adresslist': adresslist})
    else:
        return redirect('index')

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    