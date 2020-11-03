# Generated by Django 2.1.1 on 2019-07-17 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0017_project_access_project_owner_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_access',
            name='role',
            field=models.CharField(default='Master', max_length=50),
        ),
        migrations.AlterField(
            model_name='project_access',
            name='status',
            field=models.CharField(default='Pending', max_length=50),
        ),
    ]