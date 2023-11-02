from django import template
from main.models import Task


register = template.Library()

@register.simple_tag  #шаблонный тег
def total_tasks():
    return Task.objects.all()

