# Generated by Django 2.1.1 on 2019-09-09 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0073_auto_20190909_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processlog',
            name='project_name',
        ),
    ]
