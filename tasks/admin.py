from django.contrib import admin
from .models import Task, Client, TaskStatus, JobType, TimeEntry

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass

@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    pass

@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    pass

