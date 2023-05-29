from django import template

register = template.Library()

@register.filter(name="num_to_str")
def num_to_str(value):
    if value == 0:
        return "ZERO"
    elif value == 1:
        return "ONE"
    return "NUMBER"
