from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .models import Task
from django.contrib.auth.decorators import login_required
from .forms import TaskUpdateForm, TaskCreateForm
from django.contrib import messages

def home(request):
    context = {
        'tasks' : Task.objects.all()
    }
    return render(request, 'tasks/home.html', context)

@login_required
def mytasks(request):
    logged_in_user = request.user
    tasks = Task.objects.filter(assigned_to=logged_in_user)
    context = {
        'tasks': tasks
    }
    return render(request, 'tasks/mytasks.html', context)

@login_required
def edit_task(request, task_id):
    logged_in_user = request.user
    task = Task.objects.filter(id=task_id, assigned_to=logged_in_user).first()

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


def home(request):
    context = {
        'tasks' : Task.objects.all()
    }
    return render(request, 'tasks/home.html', context)

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.task_description = form.cleaned_data.get('task_description')
            task.save()
            return redirect('mytasks')
    else:
        form = TaskCreateForm()
    context = {
        'form': form,
         'tasks' : Task.objects.all()
    }
    return render(request, 'tasks/create_task.html', context)