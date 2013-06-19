from django import template

register = template.Library()

@register.filter(is_safe=True)
def deslug(value):
    ret = value.replace('-', ' ').replace('_', ' ')
    return ret.title()

@register.filter(is_safe=True)
def fix_ft_in(value):
    # ret = value.replace('Ft.','ft.').replace('In.','in.')
    return value.lower()

@register.filter
def qr(value,size="25x25"):
    """
        Usage:
        <img src="{{object.code|qr:"120x130"}}" />
    """
    return "http://chart.apis.google.com/chart?chs=%s&cht=qr&chl=%s&choe=UTF-8&chld=H|0" % (size, value)
