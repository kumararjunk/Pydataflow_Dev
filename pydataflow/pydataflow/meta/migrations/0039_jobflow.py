# Generated by Django 2.1.1 on 2019-07-30 08:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meta', '0038_auto_20190730_0805'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobflowname', models.CharField(max_length=50, unique=True)),
                ('project_name', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='meta.Project')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
