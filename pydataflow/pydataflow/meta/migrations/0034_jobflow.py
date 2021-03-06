# Generated by Django 2.1.1 on 2019-07-26 00:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meta', '0033_auto_20190726_0033'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField(default=1)),
                ('job_type', models.CharField(default='Stored_Proc', max_length=25)),
                ('job_name', models.CharField(default='job_name', max_length=25)),
                ('priority_id', models.SmallIntegerField(default=1, max_length=2)),
                ('etl_sch_time', models.CharField(blank=True, default='job_name', max_length=100)),
                ('execution_flag', models.CharField(default='Y', max_length=1)),
                ('project_name', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='meta.Project')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
