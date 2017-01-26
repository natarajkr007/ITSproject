from django.contrib.auth.models import User
from .models import UserProfile
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name','username', 'email', 'password')
        labels = {
            'username': 'Unique service no',
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('Address', 'phone_no')