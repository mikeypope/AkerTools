# Generated by Django 4.2.1 on 2023-05-20 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0019_timeentry_job_type_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeentry',
            name='job_type_id',
        ),
        migrations.AlterField(
            model_name='timeentry',
            name='job_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tasks.jobtype'),
            preserve_default=False,
        ),
    ]