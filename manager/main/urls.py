from django.urls import path
from main.views import by_status
from main.views import TaskCreateView, UserList, UserDetail, TaskList, TaskDetail
from main import views
from django.contrib import admin
from .feeds import LatestTasksFeed

app_name = "main" #именное пространство

#маршрутизатор
urlpatterns = [
    path('', views.main_page, name="home"),
    path('all_tasks/', views.all_tasks, name="all_tasks"),
    path('<int:status_id>/', views.by_status, name="by_status"), #именованный маршрут
    path('add/', TaskCreateView.as_view(), name='add'),
    path('<int:year>/<int:month>/<int:day>/<slug:task>/', views.task_detail, name='task_detail'),
    path('<int:year>/<int:month>/<int:day>/<slug:task>/delete/<int:id>/', views.delete, name='delete'),
    path('<int:year>/<int:month>/<int:day>/<slug:task>/edit/<int:id>/', views.edit, name='edit'),
    path('<int:task_id>/share/', views.task_share, name="task_share"),
    path('<int:task_id>/comment/', views.task_comment, name="task_comment"),
    path('tag/<slug:tag_slug>/', views.all_tasks, name = "task_list_by_tag"),
    # <int:id> - конвертер пути
    path('feed/', LatestTasksFeed(), name='task_feed'),
    path('search/', views.task_search, name="task_search"),
    path('main_page/', views.main_page, name='main_page'),

    # pdf 
    path('all_tasks/pdf', views.tasks_pdf, name='tasks_pdf'),
    path('<int:year>/<int:month>/<int:day>/<slug:task>/task_pdf/<int:id>', views.task_pdf, name='task_pdf'),
    
    # сереализаторы 
    path('users/', UserList.as_view()),
    path('users/<int:pk>', UserDetail.as_view()),
    path('tasks/', TaskList.as_view()),
    path('tasks/<int:pk>', TaskDetail.as_view()),

]


admin.site.header = "IT PROJECT MANAGER"
admin.site.site_title = "Browser Title"
admin.site.index_title = "Welcom To IT Project Manager"