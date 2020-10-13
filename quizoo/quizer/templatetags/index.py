from django import template

register = template.Library()


@register.filter
def index(li, i):
    return li[i]


