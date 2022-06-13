"""
Admin panel configuration module for writings app
"""

from django.contrib import admin

from . import models

admin.site.register((
    models.Author,
    models.Writing,
    models.Character,
    models.CharacterTag,
    models.Quote,
))
