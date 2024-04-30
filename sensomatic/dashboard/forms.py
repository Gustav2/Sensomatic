from django import forms
from django.contrib.auth.models import User

# Denne funktion skaber login felterne
class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

