# forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254, label='User ID', widget=forms.TextInput(attrs={'autofocus': True}))



class MemberNoForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields =('user_no',)