"""
URL configuration for AkerTools project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from tasks import views as task_views
from timesheet import views as time_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('tasks/', include('tasks.urls')),
    path('mytasks/', task_views.mytasks, name='mytasks'),
    path('mycompletedtasks/', task_views.mycompletedtasks, name='mycompletedtasks'),
    #path('edit_task/', task_views.edit_task, name='edit_task'),
    path('send_task/<int:task_id>', time_views.send_task, name='send_task'),
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('timesheet/', time_views.alltimes, name='alltimes'), 
    path('mytimesheet/', time_views.mytimes, name='mytimes'),    
    path('timesheet/create/', time_views.create_entry, name='create-entry'),
    path('timesheet/mycreate/', time_views.create_myentry, name='create-myentry'),
    path('timesheet/edit/<int:entry_id>/', time_views.edit_entry, name='edit-entry'),
    path('timesheet/delete/<int:entry_id>/', time_views.delete_time, name='delete-entry'),
    path('timesheet/deletefromall/<int:entry_id>/', time_views.delete_time_fromall, name='delete-entry-fromall'),
    path('timesheet/report/', time_views.generate_report, name='generate_report'),
]