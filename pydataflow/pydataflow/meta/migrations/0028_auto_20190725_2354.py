# Generated by Django 2.1.1 on 2019-07-25 23:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0027_script'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='script',
            name='project_name',
        ),
        migrations.RemoveField(
            model_name='script',
            name='user',
        ),
        migrations.DeleteModel(
            name='Script',
        ),
    ]