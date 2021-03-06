# Generated by Django 2.1.1 on 2019-07-21 07:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0024_auto_20190721_0731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_access',
            name='project_owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='project_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project_access',
            name='requester',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='requester', to=settings.AUTH_USER_MODEL),
        ),
    ]
