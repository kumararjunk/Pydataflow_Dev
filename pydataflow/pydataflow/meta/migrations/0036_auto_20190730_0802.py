# Generated by Django 2.1.1 on 2019-07-30 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0035_auto_20190730_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='script',
            name='priority_id',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='tbllist',
            name='priority_id',
            field=models.SmallIntegerField(default=1),
        ),
    ]
