from django.contrib import admin
from .models import Task, Status, Company, Comment
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'complete_date', 'content', 'created', 'status', )
    list_display_links = ('title',) #должны быть преобразованы в гиперссылки, ведущие на страницу правки записи
    search_fields = ('title', 'complete_date', 'created',)
    prepopulated_fields = {
        'slug':['title'],
                           } 
    raw_id_fields = ('person',)
    row_id_fields = ('complete_date', 'created',)
    list_filter = ('complete_date', 'status', 'created',)
    date_hierarchy = 'complete_date'

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'task', 'created', 'activate']
    list_filter = ['activate', 'created', 'updated']
    search_fields = ['name', 'email', 'body']

admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Status)
admin.site.register(Company)

