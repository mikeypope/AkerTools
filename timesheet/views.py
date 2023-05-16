from django.shortcuts import render, redirect
from tasks.models import TimeEntry, Task, Client, JobType
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TimeEntryForm, TimeEntryEditForm

def take_task(request, task_id):
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
    return redirect('mytimesheet')

@login_required
def mytimes(request):
    logged_in_user = request.user
    times = TimeEntry.objects.filter(employee=logged_in_user).order_by('date')
    context = {
        'times': times
    }
    return render(request, 'timesheet/mytimesheet.html', context)

@login_required
def alltimes(request):
    if not request.user.has_perm('timeentry.delete_task') :
        return redirect('mytimesheet')
    context = {
         'times' : TimeEntry.objects.all().order_by('date')
    }
    return render(request, 'timesheet/timesheet.html', context)

@login_required
def create_entry(request):
    if request.method == 'POST':
        form = TimeEntryForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to success page or desired URL
    else:
        form = TimeEntryForm()
    return render(request, 'timesheet/create_entry.html', {'form': form})

@login_required
def edit_entry(request, entry_id):
    entry = TimeEntry.objects.get(id=entry_id)
    if request.method == 'POST':
        form = TimeEntryEditForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            # Redirect to success page or desired URL
    else:
        form = TimeEntryEditForm(instance=entry)
    return render(request, 'edit_entry.html', {'form': form, 'entry': entry})