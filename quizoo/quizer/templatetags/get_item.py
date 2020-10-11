from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return list(dictionary.get(key)[0])[0]
