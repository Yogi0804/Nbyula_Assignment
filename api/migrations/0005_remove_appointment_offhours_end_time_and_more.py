# Generated by Django 4.0.5 on 2022-07-03 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_appointment_date_alter_appointment_end_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='offhours_end_time',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='offhours_start_time',
        ),
    ]
