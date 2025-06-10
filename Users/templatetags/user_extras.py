from django import template

register = template.Library()

@register.filter
def has_workshop(user):
    return user.workshops.exists()
