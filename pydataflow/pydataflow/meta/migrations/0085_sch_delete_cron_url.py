# Generated by Django 2.1.1 on 2019-12-01 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0084_auto_20191130_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='sch',
            name='delete_cron_url',
            field=models.CharField(default='/sch_delete_cron/0', max_length=100),
        ),
    ]
