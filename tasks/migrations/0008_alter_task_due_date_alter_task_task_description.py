# Generated by Django 4.2.1 on 2023-05-16 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_alter_task_assigned_to_alter_task_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_description',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
