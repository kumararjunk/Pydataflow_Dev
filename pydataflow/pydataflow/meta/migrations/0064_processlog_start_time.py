# Generated by Django 2.1.1 on 2019-08-28 22:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0063_auto_20190828_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='processlog',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
