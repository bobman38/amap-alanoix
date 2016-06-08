from django import template

register = template.Library()

@register.simple_tag
def get_order(obj, epk, second_arg):
    return obj.get_order(epk, second_arg)

@register.simple_tag
def get_order_family(obj, epk, second_arg):
    return obj.get_order_family(epk, second_arg)

@register.simple_tag
def get_order_all(obj, epk):
    return obj.get_order_all(epk)
