from django import forms
from tasks.models import TimeEntry, Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import User



class TimeEntryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Get the logged-in user from the kwargs
        super().__init__(*args, **kwargs)
       

    class Meta:
        model = TimeEntry  # Specify the model class
        fields = [ 'client', 'hours_worked', 'job_type']


class TimeEntryEditForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['client', 'date', 'hours_worked', 'job_type']
        # Add other fields as needed

class GenerateReportForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))
    client = forms.ChoiceField(label='Client')

    def __init__(self, *args, **kwargs):
        super(GenerateReportForm, self).__init__(*args, **kwargs)
        clients = Client.objects.all().order_by('client_name')
        client_choices = [(client.client_name, client.client_name) for client in clients]
        self.fields['client'].choices = client_choices
        self.set_default_dates()

    def set_default_dates(self):
        today = timezone.now().date()
        self.initial['start_date'] = today.replace(day=1)
        self.initial['end_date'] = today

class TimeEntryFilterForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}),required=False)
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}),required=False)
    
    employee = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'),
        empty_label='All Employees',
        required=False
    )
    client = forms.ModelChoiceField(
        queryset=Client.objects.all().order_by('client_name'),
        empty_label='All Clients',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(TimeEntryFilterForm, self).__init__(*args, **kwargs)
        self.set_default_dates()
        

    def set_default_dates(self):
        today = timezone.now().date()
        self.initial['start_date'] = today.replace(day=1)
        self.initial['end_date'] = today
        
class MyTimeEntryFilterForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}),required=False)
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}),required=False)
    client = forms.ModelChoiceField(
        queryset=Client.objects.all().order_by('client_name'),
        empty_label='All Clients',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(MyTimeEntryFilterForm, self).__init__(*args, **kwargs)
        self.set_default_dates()
        
    def set_default_dates(self):
        today = timezone.now().date()
        self.initial['start_date'] = today.replace(day=1)
        self.initial['end_date'] = today
