from django.contrib import admin
from .models import Character, CharacterTag, Quote

admin.site.register((
    Character,
    CharacterTag,
    Quote,
))
