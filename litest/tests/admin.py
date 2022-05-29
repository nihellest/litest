from django.contrib import admin
from .models import QuoteQuestion


@admin.register(QuoteQuestion)
class QuoteQuestionAdmin(admin.ModelAdmin):
    filter_horizontal = ('alt_answers',)
