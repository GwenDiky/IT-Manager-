from django.db import models
from datetime import date
from django.db.models.query import QuerySet 
from django.utils.translation import gettext as _
from django.core import validators
from django.contrib.auth.models import User
from django.urls import reverse 
from taggit.managers import TaggableManager

"""
Разработка программы управления ИТ-проектами: задача составления расписания выполнения проекта
"""
class Status(models.Model):
    NOT_PREPARE = "-"
    IN_PROCESS = "+/-"
    DONE = "+"
    TITLES = {
        (NOT_PREPARE, "Не завершено"),
        (IN_PROCESS, "В процессе"),
        (DONE, "Завершено")
    }
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 30, choices = TITLES, verbose_name="Завершенность", default = NOT_PREPARE)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return '/main/%s' % self.pk
    class Meta:
        db_table = "Статус"
        verbose_name_plural = "Статусы"
        verbose_name = "Статус"
        ordering = ['title']


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 100)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "Компания"
        verbose_name_plural = "Компании"
        verbose_name = "Компания"

# Менеджер, позволяющий извлекать посты, используя обозначение Task.status.all() (Task.my_manager.status())
# конкретно-прикладной менеджер
"""
class DifficultManager(models.Manager):
    def get_queryset(self) -> QuerySet: #возвращает набор запросов QuerySet, который будет исполнен
        return super().get_queryset()\
            .filter(type = Task.Types.DIFFICULT)
    # переопределили этот метод, чтобы сформировать конкретно-прикладной набор запросов QuerySet, фильтрующий посты по их статусу и возвращающий поочередный набор запросов QuerySet, содержащий посты только со статусом NOT_PREPARE
"""

class DoneManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset() \
            .filter(status = Status.TITLES[2])
    
class ProccessManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset() \
            .filter(status = Status.TITLES[1])
    
class NotDoneManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset() \
            .filter(status=Status.TITLES[0])
    
class Task(models.Model):
    class Types(models.TextChoices):
        DIFFICULT = 'Сложная', 'Повышенная сложность'
        AVERAGE = 'Средняя', 'Средняя сложность'
        EASY = 'Легкая', 'Минимальная сложность'
        __empty__ = 'Уровень сложности задачи не указан'
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250, verbose_name = "Заголовок")
    tags = TaggableManager()
    slug = models.SlugField(max_length=250, verbose_name="Слаг", unique_for_date='created')
    content = models.TextField(null = True, blank = True, verbose_name = "Описание", help_text="Текст помощи: ")
    image = models.ImageField(null = True, blank = True, verbose_name="Фотография")
    type = models.CharField(max_length = 30, choices = Types.choices, default = Types.AVERAGE, verbose_name="Уровень сложности")
    person = models.ManyToManyField(User, blank=True, related_name="app_tasks", verbose_name="Участник")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Компания")
    status = models.ForeignKey(Status, on_delete = models.PROTECT, verbose_name="Статус", null=True)
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата редактирования")
    created = models.DateTimeField(auto_now_add = True, db_index = True, verbose_name="Дата создания")
    complete_date = models.DateField(_("Дата завершения"), blank=True)
    #difficult = DifficultManager() # конкретно-прикладной менеджер
    objects = models.Manager() # менеджер, применяемый по умолчанию
    done_tasks = DoneManager() # конкретно-прикладной менеджер
    proccess_tasks = ProccessManager()
    not_done_tasks = NotDoneManager()
    
    class Meta:
        verbose_name_plural = "Задачи"
        verbose_name = "Задача" 
        ordering = ["-complete_date"]
        indexes = [
            models.Index(fields=['-complete_date'])
        ]
        db_table = "Задача"
    def get_absolute_url(self):
        return reverse('main:task_detail', args=[self.created.year, self.created.month, self.created.day, self.slug])
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments") #каждый комментарий связан с 1 постом (многие-к-одному)
    # атрибут related_name позволяет назначать имя атрибуту, который используется для связи от ассоциированного объекта назад к нему
    # задачу комментированного объекта можно извлекать посредством comments.task  и все комментарии ассоциированные с объектом-задачей посредством task.comments.all()
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    activate = models.BooleanField(default = True) # данное поле позволяет деактивировать неуместные комментарии вручную с помощью сайта администрирования

    class Meta:

        verbose_name_plural = "Комментарии"
        verbose_name = "Комментарий" 

        ordering = ['created']
        indexes = [
            models.Index(fields=['created']) # в результате этого будет повышена производительность поиска в базе данных и упорядочивания результатом с использованием поля created
        ]

    def __str__(self):
        return f"Комментарий пользователя {self.name} на задачу {self.task}"