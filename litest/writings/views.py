"""
Views module for writings app
"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from tests.services import TEST_STATISTICS_SERVICES
from .forms import LoginForm


def index_page(request) -> HttpResponse:
    """View for main page"""

    return render(request, 'writings/index.html')


def login_page(request) -> HttpResponse:
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

def logout_page(request: HttpRequest) -> HttpResponse:
    """View for logout current user"""
    if request.user.is_authenticated:
        logout(request)
    return redirect(index_page)

def profile_page(request: HttpRequest) -> HttpResponse:
    user = request.user
    if not user:
        redirect(login_page)
    statistics = []
    for service_name, service in TEST_STATISTICS_SERVICES.items():
        statistics.append(service.get_runs_per_user(user))
    context = {
        'username': user.username,
        'statistics': statistics,
    }

    return render(request, 'writings/profile.html', context)