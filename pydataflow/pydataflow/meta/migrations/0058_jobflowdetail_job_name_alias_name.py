# Generated by Django 2.1.1 on 2019-08-10 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0057_auto_20190810_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobflowdetail',
            name='job_name_alias_name',
            field=models.CharField(default='job_name', max_length=50),
        ),
    ]
