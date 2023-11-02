from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task


class UserSerializer(serializers.ModelSerializer):
    app_tasks = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    class Meta:
        model = User
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    person = UserSerializer(many = True, read_only = True)
    class Meta:
        model = Task
        fields = '__all__'
