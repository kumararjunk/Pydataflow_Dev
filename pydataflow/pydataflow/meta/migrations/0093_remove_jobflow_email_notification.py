# Generated by Django 2.1.1 on 2020-06-13 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0092_auto_20200531_0342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobflow',
            name='email_notification',
        ),
    ]
