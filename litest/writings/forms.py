"""
Forms module for writings app
"""

from django import forms


class LoginForm(forms.Form):
    """Form for user login page"""

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
