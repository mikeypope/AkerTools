from django import forms
from.models import Task, JobType, TaskStatus, Client, User
from django.utils import timezone

# class TaskUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = ['task_kind', 'task_description', 'for_client', 'assigned_to', 'due_date', 'task_status',]
#         widgets = {
#             'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['task_kind'].required = False
#         self.fields['task_status'].required = False
#         self.fields['for_client'].required = False
#         self.fields['assigned_to'].required = False

#         if 'instance' in kwargs:
#             instance = kwargs['instance']
#             self.initial['due_date'] = instance.due_date.strftime('%Y-%m-%d') if instance.due_date else None

#         self.fields['task_kind'].queryset = JobType.objects.order_by('job_type')
#         self.fields['task_status'].queryset = TaskStatus.objects.order_by('status')
#         self.fields['for_client'].queryset = Client.objects.order_by('client_name')
#         self.fields['assigned_to'].queryset = User.objects.order_by('username')
class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_kind', 'task_description','task_notes','for_client', 'assigned_to', 'due_date', 'task_status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task_kind'].required = False
        self.fields['task_notes'].required = False
        self.fields['task_status'].required = False
        self.fields['for_client'].required = False
        self.fields['assigned_to'].required = False
        self.fields['due_date'].required = False

        if 'instance' in kwargs:
            instance = kwargs['instance']
            self.initial['due_date'] = instance.due_date.strftime('%Y-%m-%d') if instance.due_date else timezone.now().strftime('%Y-%m-%d')

        self.fields['task_kind'].queryset = JobType.objects.order_by('job_type')
        self.fields['task_status'].queryset = TaskStatus.objects.order_by('status')
        self.fields['for_client'].queryset = Client.objects.order_by('client_name')
        self.fields['assigned_to'].queryset = User.objects.order_by('username')

class MyTaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_kind', 'task_description','task_notes', 'for_client', 'due_date', 'task_status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task_kind'].required = False
        self.fields['task_status'].required = False
        self.fields['for_client'].required = False
        self.fields['due_date'].required = False
        self.fields['task_notes'].required = False

        if 'instance' in kwargs:
            instance = kwargs['instance']
            self.initial['due_date'] = instance.due_date.strftime('%Y-%m-%d') if instance.due_date else timezone.now().strftime('%Y-%m-%d')

        self.fields['task_kind'].queryset = JobType.objects.order_by('job_type')
        self.fields['task_status'].queryset = TaskStatus.objects.order_by('status')
        self.fields['for_client'].queryset = Client.objects.order_by('client_name')



class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_description']
        labels = {
            'task_description': 'Enter task description'
        }

