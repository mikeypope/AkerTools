from django import forms
from tasks.models import TimeEntry

class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['employee', 'client', 'date', 'hours_worked', 'job_type']
        # Add other fields as needed

class TimeEntryEditForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['employee', 'client', 'date', 'hours_worked', 'job_type']
        # Add other fields as needed