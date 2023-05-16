from django import forms
from.models import Task

class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_kind', 'task_description', 'task_status', 'due_date', 'task_status', 'for_client', 'assigned_to']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task_kind'].required = False
        self.fields['task_status'].required = False
        self.fields['due_date'].required = False
        self.fields['for_client'].required = False
        self.fields['assigned_to'].required = False

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_description']
        labels = {
            'task_description': 'Description'
        }

