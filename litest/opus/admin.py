from django.contrib import admin
from .models import Opus, Author

admin.site.register((
    Opus,
    Author,
))