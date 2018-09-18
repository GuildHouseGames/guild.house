from django import template
from project.site.models import Navigation


register = template.Library()


@register.simple_tag(takes_context=True)
def nav_menu(context):
    nav_menu = Navigation.objects.filter(is_active=True)
    context['nav_items'] = nav_menu
    return ""
