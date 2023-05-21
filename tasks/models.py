from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal,ROUND_DOWN



class Client(models.Model):
    client_name = models.CharField(max_length=255, unique=True)
    lead_designer_rate = models.DecimalField(max_digits=5, decimal_places=2)
    associate_designer_rate = models.DecimalField(max_digits=5, decimal_places=2)
    admin_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def calculate_bill(self, start_date=None, end_date=None):
        breakdown = {}
        bill_amount = Decimal('0.00')

        time_entries = TimeEntry.objects.filter(client=self)

        if start_date and end_date:
            time_entries = time_entries.filter(date__range=[start_date, end_date])

        employee_ranks = {
            'LeadDesigner': self.lead_designer_rate,
            'AssociateDesigner': self.associate_designer_rate,
            'Admin': self.admin_rate
        }

        for employee_rank, rate in employee_ranks.items():
            employee_entries = time_entries.filter(
                employee__groups__name=employee_rank
            ).values('job_type__job_type').annotate(total_hours=Sum('hours_worked'))

            job_types = {entry['job_type__job_type']: entry['total_hours'] for entry in employee_entries}

            employee_hours = sum(job_types.values()) or Decimal('0.00')

            breakdown[employee_rank] = {
                'hours_worked': employee_hours,
                'job_types': job_types,
                'rate': rate,
            }

            bill_amount += employee_hours * Decimal(rate)
            bill_amount = bill_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

        return bill_amount, breakdown

    def __str__(self):
        return self.client_name


class TaskStatus(models.Model):
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.status

class JobType(models.Model):
    id = models.AutoField(primary_key=True)
    job_type = models.CharField(max_length=100)
    billable = models.SmallIntegerField()

    def __str__(self):
        return self.job_type


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks', null=True, default=None)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks', null=True, default=None)
    task_kind = models.ForeignKey(JobType, on_delete=models.CASCADE, null=True, default=None)
    task_description = models.TextField(null=True, default=None)
    task_status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE, null=True, default=None)
    for_client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='tasks', null=True, default=None)
    due_date = models.DateField(default=None, null=True)

    def __str__(self):
        return self.task_description

    
class TimeEntry(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='time_entries')
    date = models.DateField(default=timezone.now)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)


    def __str__(self):
        return f"TimeEntry {self.id}"

    