from django import template

register = template.Library()


@register.filter
def sort_case_insensitive(queryset, field):
    return sorted(queryset, key=lambda x: getattr(x, field).lower())


@register.filter
def sort_by_date(queryset, field):
    return sorted(queryset, key=lambda x: getattr(x, field), reverse=True)
