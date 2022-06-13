"""
App configuration module for writings app
"""

from django.apps import AppConfig


class WritingsConfig(AppConfig):
    """App congiguration class"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'writings'
