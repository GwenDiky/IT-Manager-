from django import template
from main.models import Task
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.simple_tag  # шаблонный тег
def total_tasks():
    return Task.objects.count()

# шаблонный тег включения
@register.inclusion_tag('main/task/latest_tasks.html')
def show_latest_tasks(count=3):
    latest_tasks = Task.objects.order_by('-complete_date')[:count]
    return {'latest_tasks':latest_tasks} # теги включения должны возвращать словарь значений, который используется в качестве контекста для прорисовки заданного шаблона

@register.simple_tag
def get_most_commented_tasks(count=3):
    return Task.objects.annotate(total_comments = Count('comments')
                                 ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
