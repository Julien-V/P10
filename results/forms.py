from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ConnectionForm(forms.Form):
    username = forms.CharField(label="Adresse Email", max_length=150)
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput
    )


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "username", "email",
            'first_name', 'last_name',
            'password1', "password2"
        ]
