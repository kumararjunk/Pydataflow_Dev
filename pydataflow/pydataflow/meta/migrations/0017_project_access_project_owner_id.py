# Generated by Django 2.1.1 on 2019-07-15 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0016_project_access_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_access',
            name='project_owner_id',
            field=models.IntegerField(default=1, max_length=2),
        ),
    ]
