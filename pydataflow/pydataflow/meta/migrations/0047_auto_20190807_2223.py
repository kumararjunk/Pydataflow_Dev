# Generated by Django 2.1.1 on 2019-08-07 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0046_auto_20190806_0241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='is_active',
            field=models.CharField(choices=[('Y', 'Y'), ('N', 'N')], default='Y', max_length=1),
        ),
    ]
