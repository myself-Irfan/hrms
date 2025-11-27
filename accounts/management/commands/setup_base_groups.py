from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from accounts.enums import UserGroup


class Command(BaseCommand):
    help = 'Create initial user groups for RBAC'

    def handle(self, *args, **options):
        for group in UserGroup:
            group_obj, created = Group.objects.get_or_create(name=group.value)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {group.label}'))
            else:
                self.stdout.write(f'Group already exists: {group.label}')
