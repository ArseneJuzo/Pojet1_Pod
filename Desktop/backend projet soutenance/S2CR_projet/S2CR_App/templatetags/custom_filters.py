import base64
from django import template

register = template.Library()

@register.filter
def base64encode(value):
    """Encode une chaîne en base64 pour les liens"""
    try:
        return base64.b64encode(value.encode('utf-8')).decode('utf-8')
    except:
        return ''