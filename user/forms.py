from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'avatar', 'bio', 'date_of_birth', 'location', 'education']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'avatar': forms.FileInput(),
        }