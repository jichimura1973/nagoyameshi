from django import template
import datetime

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

@register.filter
def honor(val):
    return 'さん'

@register.filter
def honor2(val):
    return f'{val} さん'

@register.filter
def greet(val):
    greeting = 'ようこそ'
    now = datetime.datetime.now()
    if now.hour <= 8:
        greeting = 'おはようございます'
    elif now.hour <= 18:
        greeting = 'こんにちは'
    else:
        greeting = 'こんばんは'
    
    return f'{greeting}'
