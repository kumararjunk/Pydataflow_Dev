# Generated by Django 2.1.1 on 2019-07-19 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0019_auto_20190717_0114'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_access',
            name='change_role',
            field=models.CharField(choices=[('Master', 'Master: Full Access'), ('Developer', 'Developer: Add/Edit jobs'), ('Operator', 'Operator:Only Execute jobs')], default='Master', max_length=10),
        ),
    ]
