from dataclasses import fields
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NeighborhoodForm(forms.ModelForm):
    class Meta:
     model=Neighborhood
     fields='__all__'

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields='__all__'

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields='__all__'

class BusinessForm(forms.ModelForm):
    class Meta:
        model=Business
        fields='__all__'

class RegistrationForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class UserForm(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username','email']

# for fieldname in ['username', 'password1', 'password2']:
#         self.fields[fieldname].help_text = None

