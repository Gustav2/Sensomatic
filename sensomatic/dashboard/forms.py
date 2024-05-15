from django import forms
from datacollector.models import Trashcan, TrashIsland


# Denne funktion skaber login felterne
class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

class AddSensor(forms.ModelForm):
    class Meta:
        model = Trashcan
        fields = ["MAC_adress", "island", "capacity", "type"]

class AddIsland(forms.ModelForm):
    class Meta:
        model = TrashIsland
        fields = "__all__"

