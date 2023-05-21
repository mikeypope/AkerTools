from django.shortcuts import render, redirect
from tasks.models import TimeEntry, Task, Client, JobType
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TimeEntryForm, TimeEntryEditForm
from django.db.models import Sum
from django import template
from django.contrib.auth.models import Group
from datetime import date, timedelta
from django.template.defaultfilters import date as datefilter
from .forms import GenerateReportForm


register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


def send_task(request, task_id):
    # Retrieve the task based on the task_id
    task = Task.objects.get(id=task_id)

    # Create a new TimeEntry instance with the task details
    time_entry = TimeEntry(
        employee=request.user,
        client=task.for_client,
        date=task.due_date,
        hours_worked=0.0,
        job_type=task.task_kind
    )
    time_entry.save()

    # Redirect the user to a success page or desired URL
    return redirect('mytimes')

@login_required
def mytimes(request):
    logged_in_user = request.user
    times = TimeEntry.objects.filter(employee=logged_in_user)
    context = {
        'times': times
    }
    return render(request, 'timesheet/mytimesheet.html', context)

@login_required
def alltimesbyclient(request):
    if not request.user.groups.filter(name='LeadDesigner').exists():
        return redirect('mytimes')
    context = {
         'times' : TimeEntry.objects.all().order_by('client','date')
    }
    return render(request, 'timesheet/timesheet.html', context)

@login_required
def alltimesbyemployee(request):
    if not request.user.groups.filter(name='LeadDesigner').exists():
        return redirect('mytimes')
    context = {
         'times' : TimeEntry.objects.all().order_by('employee','date')
    }
    return render(request, 'timesheet/timesheet.html', context)

@login_required
def alltimes(request):
    if not request.user.groups.filter(name='LeadDesigner').exists():
        return redirect('mytimes')
    context = {
         'times' : TimeEntry.objects.all().order_by('date')
    }
    return render(request, 'timesheet/timesheet.html', context)

@login_required
def create_entry(request):
    if not request.user.has_perm('tasks.delete_task'):
        return redirect('mytasks')

    if request.method == 'POST':
        form = TimeEntryForm(request.POST, user=request.user)
        if form.is_valid():
            time = form.save(commit=False)
            time.employee = request.user
            time.client = form.cleaned_data.get('client')
            time.hours = form.cleaned_data.get('hours')
            time.job_type = form.cleaned_data.get('job_type')
            time.save()
            return redirect('mytimes')
    else:
        form = TimeEntryForm(user=request.user)

    context = {
        'form': form,
    }
    return render(request, 'timesheet/create_entry.html', context)



@login_required
def edit_entry(request, entry_id):
    entry = TimeEntry.objects.get(id=entry_id)
    if request.method == 'POST':
        form = TimeEntryEditForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            # Redirect to success page or desired URL
            return redirect('mytimes')
    else:
        form = TimeEntryEditForm(instance=entry)
    return render(request, 'timesheet/edit_entry.html', {'form': form, 'entry': entry})

@login_required
def delete_time_fromall(request, entry_id):
    entry = TimeEntry.objects.get(id=entry_id)

    if not entry:
        # Task not found
        return HttpResponseNotFound()

    # Check if the logged-in user has permission to delete the task
    else:
        entry.delete()
        messages.success(request, ' Time deleted successfully.')
        return redirect('alltimes')

def report_hours_by_employee(request):
    if not request.user.groups.filter(name='LeadDesigner').exists():
        return redirect('mytimes')
    
    hours_by_employee = TimeEntry.objects.values('employee__username', 'client__client_name', 'job_type__job_type') \
        .annotate(total_hours=Sum('hours_worked')) \
        .order_by('employee__username', 'client__client_name', 'job_type__job_type')
    
    context = {
        'hours_by_employee': hours_by_employee
    }
    return render(request, 'timesheet/report.html', context)

@login_required
def delete_time(request, entry_id):
    entry = TimeEntry.objects.get(id=entry_id)

    if not entry:
        # Task not found
        return HttpResponseNotFound()

    # Check if the logged-in user has permission to delete the task
    else:
        entry.delete()
        messages.success(request, 'Time deleted successfully.')
        return redirect('mytimes')
    
@login_required
def generate_report(request):
    clients = Client.objects.all()

    if request.method == 'POST':
        form = GenerateReportForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            client_name = form.cleaned_data['client']

            client = Client.objects.get(client_name=client_name)
            bill_amount, breakdown = client.calculate_bill(start_date, end_date)

            context = {
                'form': form,
                'clients': clients,
                'bill_amount': bill_amount,
                'breakdown': breakdown,
                'start_date': start_date,
                'end_date': end_date,
                'lead_designer_rate': client.lead_designer_rate,
                'associate_designer_rate': client.associate_designer_rate,
                'admin_rate': client.admin_rate,
            }
            return render(request, 'timesheet/report.html', context)
    else:
        form = GenerateReportForm()

        context = {
            'form': form,
            'clients': clients,
        }
        return render(request, 'timesheet/report.html', context)
    
@login_required
def create_myentry(request):

    if request.method == 'POST':
        form = TimeEntryForm(request.POST, user=request.user)
        if form.is_valid():
            time = form.save(commit=False)
            time.employee = request.user
            time.client = form.cleaned_data.get('client')
            time.hours = form.cleaned_data.get('hours')
            time.job_type = form.cleaned_data.get('job_type')
            time.save()
            return redirect('mytimes')
    else:
        form = TimeEntryForm(user=request.user)

    context = {
        'form': form,
    }
    return render(request, 'timesheet/create_entry.html', context)
