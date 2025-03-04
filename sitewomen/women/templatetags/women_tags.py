from django import template
from django.db.models import Count

from women.models import Category, TagPost
from women.views_example import menu

register = template.Library()

# @register.simple_tag()
# def get_db():
#     return views.cats_db

# @register.simple_tag()
# def get_menu():
#     return {'menu': menu}

@register.inclusion_tag('women/inclusion_teg1.html')
def get_cats(cat_id):
    cats_db = Category.objects.annotate(total=Count('posts')).filter(total__gt=0)
    return {'cats_db': cats_db, 'cat_id': cat_id}

@register.inclusion_tag('women/list_tags.html')
def get_tags():
    tags = TagPost.objects.annotate(total=Count('your_tags')).filter(total__gt=0)
    return {'tags': tags}