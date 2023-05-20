# Generated by Django 4.2.1 on 2023-05-20 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0018_alter_timeentry_job_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeentry',
            name='job_type_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tasks.jobtype'),
            preserve_default=False,
        ),
    ]
