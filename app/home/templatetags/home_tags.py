from django import template
from home.models import Procedure, Tag

register = template.Library()


@register.simple_tag()
def get_procedures():
    """Получить все процедуры"""
    return Procedure.objects.filter(unpublished=False)


@register.simple_tag()
def get_all_tags():
    """Получить все тэги"""
    return Tag.objects.all()


@register.inclusion_tag('home/tags/best_procedures.html')
def get_best_procedures(count=3):
    procedures = Procedure.objects.order_by("-sorting")[:count]
    return {"best_procedures": procedures}


@register.inclusion_tag('home/tags/tags_cloud.html')
def get_tags_cloud():
    tags = Tag.objects.all()
    return {"tags": tags}
