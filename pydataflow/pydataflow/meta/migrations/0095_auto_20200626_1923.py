# Generated by Django 2.1.1 on 2020-06-27 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0094_processlog_executed_job_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='sch',
            name='failure_option',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sch',
            name='sla_long_running_job',
            field=models.IntegerField(default=0),
        ),
    ]