from django.contrib.auth.models import User
from .models import UserProfile
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name','username', 'email', 'password')
        # labels = {
        #     'username': 'Unique service no',
        # }

class UserProfileForm(forms.ModelForm):
    # phone_no = forms.CharField(widget=forms.)         need to complete it

    class Meta:
        model = UserProfile
        fields = ('address', 'phone_no')

class NameForm(forms.Form):
    complaint = forms.CharField(label='Complaint', max_length=100)
