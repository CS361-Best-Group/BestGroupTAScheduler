from django.contrib.auth.models import User, Group

def determineRole(user):
    if user.groups.filter(name='manager').exists():
        return 'manager'
    elif user.groups.filter(name='instructor').exists():
        return 'instructor'
    else:
        return 'ta'
