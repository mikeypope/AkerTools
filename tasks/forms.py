from django import forms
from.models import Task

class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'task_description', 'task_status', 'due_date', 'task_status', 'for_client', 'assigned_to']

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_description']
        labels = {
            'task_description': 'Description'
        }

