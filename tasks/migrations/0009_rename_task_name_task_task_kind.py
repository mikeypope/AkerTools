# Generated by Django 4.2.1 on 2023-05-16 04:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_alter_task_due_date_alter_task_task_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='task_name',
            new_name='task_kind',
        ),
    ]