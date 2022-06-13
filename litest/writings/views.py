"""
Views module for writings app
"""

from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm


def index_page(request):
    """View for main page"""

    return render(request, 'writings/index.html')


def login_page(request):
    """View for login page"""
    if request.user.is_authenticated:
        return redirect(index_page)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['name'],
                password=form.cleaned_data['password']
            )
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(index_page)
                # TODO: process case
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'writings/login.html', context)

def logout_page(request: HttpRequest):
    """View for logout current user"""
    if request.user.is_authenticated:
        logout(request)
    return redirect(index_page)
