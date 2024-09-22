from django import template

register = template.Library()

@register.filter
def unit(val):
    # return str(val) + '円'
    return f'{val:,}円'

@register.filter
def post(val:str):
    return f'{val[0:3]}-{val[3:7]}'

@register.filter
def seat(val:int):
    return f'{val}席'
 