from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from .models import Task
from django.contrib.auth.decorators import login_required
from .forms import TaskUpdateForm, TaskCreateForm
from django.contrib import messages

@login_required
def home(request):
    if not request.user.has_perm('tasks.delete_task') :
        return redirect('mytasks')
    if request.method == 'POST' :
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            logged_in_user = request.user
            task = form.save(commit=False)
            task.task_description = form.cleaned_data.get('task_description')
            task.created_by = logged_in_user
            task.save()
            return redirect('task-home')
    else:
        form = TaskCreateForm()
    context = {
        'form': form,
         'tasks' : Task.objects.all()
    }
    return render(request, 'tasks/home.html', context)

@login_required
def mytasks(request):
    logged_in_user = request.user
    tasks = Task.objects.filter(assigned_to=logged_in_user).exclude(task_status='1').order_by('due_date')
    context = {
        'tasks': tasks
    }
    return render(request, 'tasks/mytasks.html', context)

@login_required
def edit_task(request, task_id):
    logged_in_user = request.user
    task = Task.objects.filter(id=task_id).first()

    if not task:
        # Task not found or not assigned to the logged-in user
        return HttpResponseNotFound()

    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('mytasks')
    else:
        form = TaskUpdateForm(instance=task)

    context = {
        'form': form,
        'task': task
    }
    return render(request, 'tasks/edit_task.html', context)


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


