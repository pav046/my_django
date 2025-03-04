from django.contrib.auth.models import Group

def user_social(backend, user, response, *args, **kwargs):
    group = Group.objects.filter(name='social')
    if len(group):
        user.groups.add(group[0])

