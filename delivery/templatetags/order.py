from django import template

register = template.Library()

@register.simple_tag
def get_order(obj, epk, second_arg):
    return obj.get_order(epk, second_arg)
