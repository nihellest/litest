"""
Apps module for tests app
"""

from django.apps import AppConfig


class TestsConfig(AppConfig):
    """App configuration class"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tests'
