# Generated by Django 2.1.1 on 2019-08-06 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0045_jobflowdetail_etl_sch_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='script',
            name='execution_flag',
        ),
        migrations.AddField(
            model_name='script',
            name='is_active',
            field=models.CharField(default='Y', max_length=1),
        ),
    ]