# Generated by Django 4.2.1 on 2023-05-16 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_alter_task_task_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobtype',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
