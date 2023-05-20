# Generated by Django 4.2.1 on 2023-05-20 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0016_client_adminrate_client_associatedesignerrate_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='AdminRate',
            new_name='admin_rate',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='AssociateDesignerRate',
            new_name='associate_designer_rate',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='LeadDesignerRate',
            new_name='lead_designer_rate',
        ),
        migrations.AlterField(
            model_name='client',
            name='client_name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='timeentry',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_entries', to='tasks.client'),
        ),
    ]