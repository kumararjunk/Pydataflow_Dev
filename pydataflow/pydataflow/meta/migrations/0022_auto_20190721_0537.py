# Generated by Django 2.1.1 on 2019-07-21 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0021_auto_20190719_2117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project_access',
            name='project_name',
        ),
        migrations.RemoveField(
            model_name='project_access',
            name='user',
        ),
        migrations.DeleteModel(
            name='Project_access',
        ),
    ]