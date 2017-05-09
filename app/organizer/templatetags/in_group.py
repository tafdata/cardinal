from django.template import Library
register = Library()

@register.filter
def in_group(user, team_name):
    if user.groups.filter(name=team_name).exists():
        return True
    else:
        return False
