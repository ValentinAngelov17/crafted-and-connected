from django import template
from crafted_and_connected.social.models import Post

register = template.Library()

@register.filter
def get_category_display(value):
    return dict(Post.CATEGORY_CHOICES).get(value)

@register.filter
def get_subcategory_display(value, category):
    subcategories = dict(Post.SUBCATEGORY_CHOICES.get(category, []))
    return subcategories.get(value)