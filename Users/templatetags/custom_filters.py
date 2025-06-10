from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    try:
        old, new = arg.split(';')
        return value.replace(old, new)
    except ValueError:
        return value  # noto‘g‘ri format bo‘lsa, asl qiymatni qaytaradi
