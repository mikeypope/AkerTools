from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Client(models.Model):
    client_name = models.CharField(max_length=255)

    def __str__(self):
        return self.client_name


class TaskStatus(models.Model):
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.status


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks', null=True, default=None)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks', null=True, default=None)
    task_name = models.CharField(max_length=255, null=True, default=None)
    task_description = models.CharField(max_length=255, null=True, default=None)
    task_status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE, null=True, default=None)
    for_client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='tasks', null=True, default=None)
    due_date = models.DateField(default=timezone.now, null=True)

    def __str__(self):
        return self.task_description
