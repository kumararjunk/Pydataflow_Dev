# Generated by Django 2.1.1 on 2019-08-10 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0060_auto_20190810_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobflowdetail',
            name='additional_param',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
    ]