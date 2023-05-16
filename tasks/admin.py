from django.contrib import admin
from .models import Task, Client, TaskStatus
# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass

@admin.register(TaskStatus)
class ClientAdmin(admin.ModelAdmin):
    pass
