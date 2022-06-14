"""
Tags for tests templates
"""

from django import template

register = template.Library()

@register.inclusion_tag('tests/questions_progress.html')
def questions_progress(run):
    return { 
        'questions': run['questions'],
        'current_index': run['current_index'],
    }
