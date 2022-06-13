"""
Utils for writings app
"""

from django.urls import reverse
from django.http import HttpRequest
from .views import login_page, logout_page


def global_context(request: HttpRequest):
    """
    Context processor for adding navigation
    & other features over all project
    """

    if request.user.is_authenticated:
        user = {
            'username': request.user.username
        }
    else:
        user = None

    return {
        'global': {
            'login': {
                'label': 'Войти',
                'link': reverse(login_page),
            },
            'logout': {
                'label': 'Выйти',
                'link': reverse(logout_page),
            },
            'user': user,
        }
    }
