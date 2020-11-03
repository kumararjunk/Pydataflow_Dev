# Generated by Django 2.1.1 on 2019-07-25 23:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meta', '0026_auto_20190721_2217'),
    ]

    operations = [
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('script_path_name', models.CharField(max_length=200)),
                ('parameters', models.CharField(max_length=300)),
                ('project_name', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='meta.Project')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]