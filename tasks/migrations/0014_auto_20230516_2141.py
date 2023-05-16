# Generated by Django 4.2.1 on 2023-05-16 21:41

from django.db import migrations

def populate_job_types(apps, schema_editor):
    JobType = apps.get_model('tasks', 'JobType')

    job_types = [
        ('Communication', 0),
        ('Communication Contractor', 0),
        ('Communication Vendor', 0),
        ('Drive Time', 0),
        ('Install', 0),
        ('Meetings/Review/Internal Coordination', 0),
        ('Meetings/Site Visits', 0),
        ('Ongoing', 0),
        ('Ordering/Returns', 0),
        ('Paid Vacation', 0),
        ('Project Management', 0),
        ('Sourcing', 0),
        ('Tracking/Scheduling', 0),
        ('Update CAD/Sketchup', 0),
        ('Update Design Board', 0),
    ]
    for name, billable in job_types:
        JobType.objects.create(job_type=name, billable=billable)

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0013_alter_jobtype_id'),
    ]

    operations = [
        migrations.RunPython(populate_job_types),
    ]