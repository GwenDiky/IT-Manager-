from django.contrib import admin
from .models import Profile, Message

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'sex', 'date_of_birth', ]
    raw_id_fields = ['user']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['title', 'content']
