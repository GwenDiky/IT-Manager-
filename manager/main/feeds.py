from django.db.models.base import Model
import markdown 
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatechars_html
from django.urls import reverse_lazy
from .models import Task

class LatestTasksFeed(Feed):
    title = 'My Blog'
    link = reverse_lazy('main:all_tasks')
    description = 'New post of my blog'

    def items(self):
        return Task.objects.all()[:5]
    
    def item_title(self, item):
        return item.title 
    
    def item_description(self, item):
        return truncatechars_html(markdown.markdown(item.content), 30)
    
    def item_pubdate(self, item):
        return item.created
