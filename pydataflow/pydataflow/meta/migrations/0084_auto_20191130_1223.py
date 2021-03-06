# Generated by Django 2.1.1 on 2019-11-30 20:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meta', '0083_processlog_pid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_type', models.CharField(default='Script', max_length=50)),
                ('sch_type', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('etl_sch_time', models.CharField(default='', max_length=50)),
            ],
            options={
                'ordering': ['project_name', 'jobflowname', 'create_time'],
            },
        ),
        migrations.RemoveField(
            model_name='report_monitor',
            name='project_name',
        ),
        migrations.RemoveField(
            model_name='jobflow',
            name='etl_sch_time',
        ),
        migrations.RemoveField(
            model_name='jobflowdetail',
            name='etl_sch_time',
        ),
        migrations.RemoveField(
            model_name='project',
            name='etl_sch_time',
        ),
        migrations.RemoveField(
            model_name='project',
            name='max_num_of_threads',
        ),
        migrations.RemoveField(
            model_name='project',
            name='sch_indicator',
        ),
        migrations.RemoveField(
            model_name='script',
            name='etl_sch_time',
        ),
        migrations.RemoveField(
            model_name='spname',
            name='etl_sch_time',
        ),
        migrations.RemoveField(
            model_name='tbllist',
            name='etl_sch_time',
        ),
        migrations.AddField(
            model_name='processlog',
            name='project_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='meta.Project'),
        ),
        migrations.AlterField(
            model_name='processlog',
            name='pid',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Report_monitor',
        ),
        migrations.AddField(
            model_name='sch',
            name='jobflowdetail',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='meta.Jobflowdetail'),
        ),
        migrations.AddField(
            model_name='sch',
            name='jobflowname',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='meta.Jobflow'),
        ),
        migrations.AddField(
            model_name='sch',
            name='project_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='meta.Project'),
        ),
        migrations.AddField(
            model_name='sch',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
