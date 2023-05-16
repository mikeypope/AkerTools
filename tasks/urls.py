from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='task-home'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
]