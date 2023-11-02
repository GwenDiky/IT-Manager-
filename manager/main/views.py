from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, FileResponse
import io
from reportlab.pdfgen import canvas 
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .models import Task, Status, Comment
from django.template import loader
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import TaskForm, EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.db.models import Case, When, Value, CharField
from django import template 
import datetime
from datetime import datetime
from django.contrib.postgres.search import SearchVector, \
                                        SearchQuery, SearchRank
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from . import serializers
from django.contrib.auth.models import User

class AllTasksView(ListView): #имплементация представления, основанного на классе, которое наследуется от класса ListView
    queryset = Task.objects.all() #используется для того, чтобы иметь конкретно-прикладной набор запросов QuerySet, не извлекая все объекты. 
    # вместо определения атрибута queryset мы могли бы указать model=Task и Django сформировал бы типовой набор запросов Task.objects.all()
    context_object_name = 'tasks' # контекстная переменная используется для результатов запроса. если не указано имя контекстного объекта, то по умолчанию используется переменная object_list
    paginate_by = 10 # возвращает 5 объектов на страницу
    template_name = 'main/all_tasks.html' # конкретно-прикладной шаблон

@login_required
def all_tasks(request, tag_slug = None): #контроллер / представление. параметр request необходим для всех функций-представлений.
    priority_values = [Status.NOT_PREPARE, Status.DONE, Status.IN_PROCESS]

    priority_values = ["+/-", "-", "+"]
    
    tasks = Task.objects.annotate(
        custom_order=Case(
            When(status__title = "+/-", then=1),
            When(status__title = "-", then=2),
            When(status__title = "+", then=3),
            default=4,  # Можете добавить значение по умолчанию, если есть другие статусы
            output_field=CharField()
        )
    ).filter(status__title__in=priority_values, person = request.user).order_by('custom_order')
    
    form = SearchForm()
    query = None
    results = []

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        tasks = tasks.filter(tags__in=[tag])
    else:
        tag = None

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', config='russian', weight='A') + \
                            SearchVector('content', weight='B')
            search_query = SearchQuery(query, config='russian')
            results = Task.objects.annotate(
                search = search_vector, rank = SearchRank(search_vector, search_query),
            ).filter(rank__gte=0.3).order_by('-rank')

    paginator = Paginator(tasks, 4)
    page_number = request.GET.get('page', 1)
    try:
        tasks = paginator.get_page(page_number)
    except EmptyPage:
        tasks = paginator.get_page(paginator.num_pages)
    except PageNotAnInteger:
        tasks = paginator.get_page(1)
        
    return render(request, 
                  'main/all_tasks.html',
                  {'form':form,
                   'query':query,
                   'results':results, 
                   'tasks':tasks,
                   'tag':tag,
                   'page_obj':page_number}
                  )

@login_required
def main_page(request, tag_slug=None):
    task_list = Task.objects.filter(person = request.user)
    statuses = Status.objects.all()
    
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        task_list = task_list.filter(tags__in=[tag])

    paginator = Paginator(task_list, 2)
    page_number = request.GET.get('page', 1)
    try:
        tasks = paginator.page(page_number)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        tasks = paginator.page(1)

    context = {"tasks":tasks, "statuses":statuses, 'tag':tag}

    return render(request, 'main/main_page.html', context)

def task_detail(request, year, month, day, task):
    task = get_object_or_404(Task, slug=task, created__year = year, created__month = month, created__day = day)
    
    # Список активных комментариев к посту
    comments = task.comments.filter(activate=True) 
    # добавили набор запросов QuerySet, чтобы извлекать все активные комментарии к посту
    form = CommentForm()

    # Список схожих постов
    task_tags_ids = task.tags.values_list('id', flat=True)
    similar_tasks = Task.objects.filter(tags__in=task_tags_ids)\
                                  .exclude(id=task.id)
    similar_tasks = similar_tasks.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags','-complete_date')[:4]  # применяется функция агрегирования Count
    
    return render(request, 'main/detail.html', {'task':task, 'comments':comments, 'form':form, 'similiar_tasks':similar_tasks})

def by_status(request, status_id):
    tasks_by_status = Task.objects.filter(status = status_id)
    statuses = Status.objects.all()
    current_status = Status.objects.get(pk = status_id)
    context = {"statuses":statuses, 'current_status':current_status, 'tasks_by_status':tasks_by_status}
    return render(request, 'main/by_statuses.html', context)


class TaskCreateView(CreateView):
    """def get(self, request, *args, **kwargs):
        context = {"form":"TaskForm"}
        return render(request, 'main/create.html', context) 
    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            task.save()
            return HttpResponseRedirect(reverse_lazy('main:home'))
        return render(request, 'main/create.html', {'form': form})"""
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('main:main_page')
    template_name = 'main/create.html'




    
""" 
        Базовый класс "знает", как создать форму, вывести на
        экран страницу с применением указанного шаблона, получить занесенные в форму
        данные, проверить их, сохранить в новой записи модели  
"""


def task_share(request, task_id):
    task = get_object_or_404(Task, id = task_id) # функция сокращенного доступа

    sent = False

    if request.method == "POST":
        # форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            task_url = request.build_absolute_uri(task.get_absolute_url())
            subject = f"{cd['name']} оповестил вас о добавлении задачи " \
                      f"{task.title}"
            message = f"Откройте задачу '{task.title}' по ссылке {task_url}.\n\n" \
                      f"{cd['name']}\' добавил(а) комментарий: {cd['comments']}"
            send_mail(subject, message, 'tamagiltamagil@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    
    context = {'task':task, 'form':form, 'sent':sent}
    return render(request, 'main/share.html', context)

@require_POST
def task_comment(request, task_id):
    task = get_object_or_404(Task, id = task_id)
    comment = None
    form = CommentForm(data=request.POST)

    if form.is_valid():
        comment = form.save(commit=False) # создать объект класса Comment, не сохраняя его в базе данных
        # т.к. commit=False, то экземпляр модели создается, но не сохраняется в базе данных
        
        # назначить задачу комментарию
        comment.task = task
        comment.save()
    return render(request, 'main/comment.html', {'task':task, 'comment':comment, 'form':form})


def task_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', config='russian', weight='A') + \
                            SearchVector('content', weight='B')
            search_query = SearchQuery(query, config='russian')
            results = Task.objects.annotate(
                search = search_vector, rank = SearchRank(search_vector, search_query),
            ).filter(rank__gte=0.3).order_by('-rank')
        
    return render(request, 
                  'main/search.html',
                  {'form':form,
                   'query':query,
                   'results':results}
                  )

def delete(request, year, month, day, task, id):
    try:
        task = Task.objects.get(id=id)
        task.delete()
        return HttpResponseRedirect(reverse_lazy('main:home'))
    except:
        return HttpResponseRedirect(reverse_lazy('main:home'))
    
def edit(request, year, month, day, task, id):
    try:
        task = Task.objects.get(id=id)
        if request.method == 'POST':
            task.title = request.POST.get('title')
            task.complete_date = request.POST.get('complete_date')
            task.content = request.POST.get('content')
            task.tags = request.POST.get('tags')
            task.type = request.POST.get('type')
            task.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, 'main/edit.html', {'task':task})
    except Task.DoesNotExist:
        return HttpResponseNotFound('<h2>Задача не найдена</h2>')
    

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class TaskList(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer

    def perform_create(self, serializer):
        serializer.save(person=self.request.user) # перезаписали функцию по умолчанию, чтобы задать поле person текущего пользователя

class TaskDetail(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer


def task_pdf(request, year, month, day, task, id):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize = letter, bottomup = 0)
    text_object = c.beginText()
    text_object.setTextOrigin(inch, inch)
    
    MyFontObject = TTFont('Arial', 'arial.ttf')
    pdfmetrics.registerFont(MyFontObject)
    text_object.setFont("Arial", 14)

    task = Task.objects.get(id=id)
    lines = [f"Название задачи: {task.title}", f"{task.content}", f"Компания: {task.company}", f"Дедлайн: {str(task.complete_date)}"]

    lines.append("Участвуют в задаче:")
    i = 1
    for person in task.person.all():
        lines.append(f"{i}) {person.username}")

    for line in lines:
        text_object.textLine(line)

    c.drawText(text_object)
    c.showPage()
    c.save()

    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f'{task.title}.pdf')


def tasks_pdf(request):
    # create bytestream buffer
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize = letter, bottomup = 0)
    text_object = c.beginText()
    text_object.setTextOrigin(inch, inch)
    

    MyFontObject = TTFont('Arial', 'arial.ttf')
    pdfmetrics.registerFont(MyFontObject)
    text_object.setFont("Arial", 14)

    tasks = Task.objects.all()

    lines = []

    for task in tasks:
        lines.append(f"Название задачи: {task.title}")
        lines.append(task.content)
        lines.append("Участвуют в задаче:")

        i = 1
        for person in task.person.all():
            lines.append(f"{i}) {person.username}")
            i += 1
        lines.append(f"Компания: {task.company}")
        lines.append(f"Дедлайн: {str(task.complete_date)}")
        lines.append("================================================")

    for line in lines:
        text_object.textLine(line)

    c.drawText(text_object)
    c.showPage()
    c.save()

    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='tasks.pdf')



