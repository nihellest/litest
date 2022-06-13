"""
Admin panel configuration module for tests app
"""

from django.contrib import admin
from .models import QuoteQuestion


@admin.register(QuoteQuestion)
class QuoteQuestionAdmin(admin.ModelAdmin):
    """Customization of admin-page for quote questions"""

    filter_horizontal = ('alt_answers',)
