"""
Utils for writings app
"""

from dataclasses import dataclass
from typing import List
from django.urls import reverse
from django.http import HttpRequest
from .views import login_page, logout_page, profile_page
from tests.views import generic_test_page


@dataclass
class NavItem:
    label: str
    link: str


@dataclass
class NavSection:
    label: str
    childs: List[NavItem]


def global_context(request: HttpRequest):
    """
    Context processor for adding navigation
    & other features over all project
    """
    navigation = [
        NavSection(
            label="Тесты",
            childs=[
                NavItem(
                    label="Цитаты",
                    link=reverse(
                        generic_test_page,
                        kwargs={'test_name': 'quotes'}
                    )
                ),
            ]
        ),
        NavItem(
            label="О сайте",
            link="#"
        )
    ]

    user_block = {
        'user': { 
            'username': request.user.username,
            'profile': NavItem(
                label=request.user.username,
                link=reverse(profile_page)
            )
        } if request.user.is_authenticated else None,
        'login': NavItem(
            label='Войти',
            link=reverse(login_page)
        ),
        'logout': NavItem(
            label='Выйти',
            link=reverse(logout_page)
        ),
    }

    return {
        'global': {
            'navigation': navigation,
            'user_block': user_block,
        }
    }
