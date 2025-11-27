from django.contrib.auth.models import Group


def assign_user_to_group(user, group_enum):
    group = Group.objects.get(name=group_enum.value)
    user.groups.add(group)

def has_group(user, group_enum):
    return user.groups.filter(name=group_enum.value).exists()
