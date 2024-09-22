from django import template

register = template.Library()

@register.filter
def unit(val):
    # return str(val) + '円'
    return f'{val:,}円'
    