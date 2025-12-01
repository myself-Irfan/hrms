from django import template
from accounts.services.user_create_service import UserCreateService

register = template.Library()


@register.simple_tag(takes_context=True)
def can_create_users(context):
    request = context.get('request')
    if not request or not request.user.is_authenticated:
        return False

    user = request.user
    if user.is_superuser:
        return True

    allowed_groups = UserCreateService.get_allowed_groups(user)
    return len(allowed_groups) > 0