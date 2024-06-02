from django import template

register = template.Library()


@register.filter
def unread_notifications_count(user):
    if user.is_authenticated:
        return user.notifications.filter(read=False).count()
    return 0
