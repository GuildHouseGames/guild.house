from django import template

register = template.Library()


def complexity(value):
    hue = 150-float(value)*40
    if hue >= 0:
        return round(hue, 0)
    else:
        return 0


register.filter('complexity_hue', complexity)
