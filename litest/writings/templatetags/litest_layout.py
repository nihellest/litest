from django import template

register = template.Library()


@register.inclusion_tag('layout/glyph.html')
def glyph(name: str):
    return { 'name': name }