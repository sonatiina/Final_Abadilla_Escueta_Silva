# Generated by Django 5.2 on 2025-04-30 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payroll_app', '0003_remove_payslip_date_range_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payslip',
            name='rate',
        ),
    ]
