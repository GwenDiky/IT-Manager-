from django.test import TestCase
from .models import Task
from django.contrib.auth.models import User
# Create your tests here.

class TaskModelTest(TestCase):

    @classmethod
    def setUpData(cls):
        user = User.objects.get(id=40)
        task = Task.objects.create(title = 'TestTask', slug = 'test-task-create', tags='test', type=Task.Types.AVERAGE, complete_date = '2024-07-09', person = user)
        task.save()

    def test_task_title(self):
        task = Task.objects.filter(title = 'TestTask')
        if task:
            expected_task_name = f'{task[0].title}'
            self.assertEqual(expected_task_name, 'TestTask')


