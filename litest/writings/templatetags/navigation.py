"""
Tags module for display navigation & user related stuff
"""

from typing import Dict, Any
from django import template
from writings.utils import NavItem, NavSection

register = template.Library()


@register.inclusion_tag('navigation/navbar.html', takes_context=True)
def navbar(context: dict) -> Dict[str, Any]:
    return context['global']


@register.inclusion_tag('navigation/navsection.html')
def navsection(section: NavSection):
    return section.__dict__


@register.inclusion_tag('navigation/navitem.html')
def navitem(item: NavItem):
    return item.__dict__

@register.inclusion_tag('navigation/userblock.html')
def userblock(data):
    return data
