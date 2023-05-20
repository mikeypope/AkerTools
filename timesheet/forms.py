from django import forms
from tasks.models import TimeEntry, Client
from django.contrib.auth import get_user_model
from django.utils import timezone


class TimeEntryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Get the logged-in user from the kwargs
        super().__init__(*args, **kwargs)
        self.fields['employee'].initial = user  # Set the initial value to the logged-in user

    employee = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        empty_label=None,  # Optional: To remove the empty label from the dropdown
    )
    class Meta:
        model = TimeEntry  # Specify the model class
        fields = ['employee', 'client', 'hours_worked', 'job_type']


class TimeEntryEditForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['employee', 'client', 'date', 'hours_worked', 'job_type']
        # Add other fields as needed

class GenerateReportForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))
    client = forms.ChoiceField(label='Client')

    def __init__(self, *args, **kwargs):
        super(GenerateReportForm, self).__init__(*args, **kwargs)
        clients = Client.objects.all()
        client_choices = [(client.client_name, client.client_name) for client in clients]
        self.fields['client'].choices = client_choices
        self.set_default_dates()

    def set_default_dates(self):
        today = timezone.now().date()
        self.initial['start_date'] = today.replace(day=1)
        self.initial['end_date'] = today