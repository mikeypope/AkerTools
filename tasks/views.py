from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from .models import Task
from django.contrib.auth.decorators import login_required
from .forms import TaskUpdateForm, TaskCreateForm, MyTaskUpdateForm, MyTaskCreateForm, TaskFilterForm, MyTaskFilterForm
from django.contrib import messages
from django.utils import timezone



@login_required
def admin(request):
    return redirect('admin')

@login_required
def home(request):
    if not request.user.is_staff:
        return redirect('mytasks')
    if request.method == 'POST' :
        form = TaskCreateForm(request.POST)
        form_filter = TaskFilterForm(request.POST)
        if form.is_valid():
            logged_in_user = request.user
            task = form.save(commit=False)
            task.task_description = form.cleaned_data.get('task_description')
            task.task_notes = form.cleaned_data.get('task_notes')
            task.created_by = logged_in_user
            task.save()
            return redirect('task-home')
        if form_filter.is_valid():
            assigned_to = form_filter.cleaned_data['assigned_to']
            client = form_filter.cleaned_data['client']
            job_type = form_filter.cleaned_data['job_type']
            
            tasks = Task.objects.all().exclude(task_status='1').order_by('due_date')
            
            if assigned_to:
                tasks = tasks.filter(assigned_to=assigned_to)

            if client:
                tasks = tasks.filter(for_client=client)

            if job_type:
                tasks = tasks.filter(job_type=job_type)

            context = {
                'form' : TaskCreateForm(),
                'form_filter': form_filter,
                'tasks': tasks,
            }
            return render(request, 'tasks/home.html', context)
            
    else:
        form = TaskCreateForm()
        form_filter = TaskFilterForm()
    context = {
        'form': form,
        'form_filter' : form_filter,
         'tasks' : Task.objects.all().exclude(task_status='1').order_by('due_date')
    }
    return render(request, 'tasks/home.html', context)

@login_required
def completedtasks(request):
    if not request.user.is_staff:
        return redirect('mytasks')
        
    else:
        form_filter = TaskFilterForm(request.POST)
        if form_filter.is_valid():
            assigned_to = form_filter.cleaned_data['assigned_to']
            client = form_filter.cleaned_data['client']
            job_type = form_filter.cleaned_data['job_type']
            start_date = form_filter.cleaned_data['start_date']
            end_date = form_filter.cleaned_data['end_date']

            
            tasks = Task.objects.all().filter(task_status='1').order_by('-due_date')
            
            if assigned_to:
                tasks = tasks.filter(assigned_to=assigned_to)

            if client:
                tasks = tasks.filter(for_client=client)

            if job_type:
                tasks = tasks.filter(task_kind=job_type)
            
            if start_date and end_date:
                
                tasks = tasks.filter(due_date__range=[start_date, end_date]) 

            context = {
                'form_filter': form_filter,
                'tasks': tasks,
            }
            return render(request, 'tasks/completedtasks.html', context)
        form_filter = TaskFilterForm()
        context = {
         'tasks' : Task.objects.all().filter(task_status='1').order_by('-due_date')
    }
    return render(request, 'tasks/completedtasks.html', context)

@login_required
def mytasks(request):
    logged_in_user = request.user
    form_filter = MyTaskFilterForm(request.POST)
    if form_filter.is_valid():
            client = form_filter.cleaned_data['client']
            job_type = form_filter.cleaned_data['job_type']
            
            tasks = Task.objects.filter(assigned_to=logged_in_user).exclude(task_status='1').order_by('due_date')
            
            if client:
                tasks = tasks.filter(for_client=client)

            if job_type:
                tasks = tasks.filter(job_type=job_type)

            context = {
                'form_filter': form_filter,
                'tasks': tasks,
            }
            return render(request, 'tasks/mytasks.html', context)
    else:
        tasks = Task.objects.filter(assigned_to=logged_in_user).exclude(task_status='1').order_by('due_date')
        form_filter = MyTaskFilterForm()
        context = {
                'form_filter': form_filter,
                'tasks': tasks,
            }
        return render(request, 'tasks/mytasks.html', context)


@login_required
def mycompletedtasks(request):
    logged_in_user = request.user
    tasks = Task.objects.filter(assigned_to=logged_in_user, task_status='1').order_by('due_date')
    form_filter = MyTaskFilterForm()

    if request.method == 'POST':
        form_filter = MyTaskFilterForm(request.POST)
        if form_filter.is_valid():
            client = form_filter.cleaned_data['client']
            job_type = form_filter.cleaned_data['job_type']
            start_date = form_filter.cleaned_data['start_date']
            end_date = form_filter.cleaned_data['end_date']
            
            if client:
                tasks = tasks.filter(for_client=client)

            if job_type:
                tasks = tasks.filter(task_kind=job_type)

            if start_date and end_date:
                
                tasks = tasks.filter(due_date__range=[start_date, end_date]) 
        context = {
            'form_filter': form_filter,
            'tasks': tasks,
        }
        return render(request, 'tasks/mycompletedtasks.html', context)
    else:
        tasks = Task.objects.filter(assigned_to=logged_in_user,task_status='1').order_by('-due_date')
        form_filter = MyTaskFilterForm()
        context = {
                'form_filter': form_filter,
                'tasks': tasks,
            }
        return render(request, 'tasks/mycompletedtasks.html', context)

@login_required
def edit_task(request, task_id):
    logged_in_user = request.user
    task = Task.objects.filter(id=task_id).first()

    if not task:
        # Task not found or not assigned to the logged-in user
        return HttpResponseNotFound()

    initial_values = {}

    if not task.due_date:
        initial_values['due_date'] = timezone.now().date()

    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task-home')
    else:
        form = TaskUpdateForm(instance=task, initial=initial_values)

    context = {
        'form': form,
        'task': task
    }
    return render(request, 'tasks/edit_task.html', context)

@login_required
def edit_mytask(request, task_id):
    logged_in_user = request.user
    task = Task.objects.filter(id=task_id).first()

    if not task:
        # Task not found or not assigned to the logged-in user
        return HttpResponseNotFound()

    initial_values = {}

    if not task.due_date:
        initial_values['due_date'] = timezone.now().date()

    if request.method == 'POST':
        form = MyTaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('mytasks')
    else:
        form = MyTaskUpdateForm(instance=task, initial=initial_values)

    context = {
        'form': form,
        'task': task
    }
    return render(request, 'tasks/edit_mytask.html', context)

@login_required
def delete_task(request, task_id):
    task = Task.objects.filter(id=task_id).first()

    if not task:
        # Task not found
        return HttpResponseNotFound()

    # Check if the logged-in user has permission to delete the task
    if not request.user.has_perm('tasks.delete_task') :
        return HttpResponseForbidden()
    if request.user.has_perm('tasks.delete_task') :
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('mytasks')

    return render(request, 'tasks/mytasks.html')

@login_required
def delete_task_fromall(request, task_id):
    task = Task.objects.filter(id=task_id).first()

    if not task:
        # Task not found
        return HttpResponseNotFound()

    # Check if the logged-in user has permission to delete the task
    if not request.user.has_perm('tasks.delete_task') :
        return HttpResponseForbidden()
    if request.user.has_perm('tasks.delete_task') :
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('task-home')

    return render(request, 'tasks/home.html')


@login_required
def create_mytask(request):
    if request.method == 'POST' :
            form = MyTaskCreateForm(request.POST)
            if form.is_valid():
                logged_in_user = request.user
                task = form.save(commit=False)
                task.task_description = form.cleaned_data.get('task_description')
                task.task_notes = form.cleaned_data.get('task_notes')
                task.created_by = logged_in_user
                task.assigned_to = logged_in_user
                task.save()
                return redirect('mytasks')
    else:
        form = MyTaskCreateForm()
    context = {
        'form': form,
    }
    return render(request, 'tasks/create_mytask.html', context)
