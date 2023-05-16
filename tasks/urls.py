from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='task-home'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('deletefromall/<int:task_id>/', views.delete_task_fromall, name='delete_task_fromall'),

]