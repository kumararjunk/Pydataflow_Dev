# Generated by Django 2.1.1 on 2019-09-09 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0074_remove_processlog_project_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='processlog',
            name='project_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='meta.Project'),
        ),
    ]
