# Generated by Django 2.1.1 on 2019-05-09 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0006_auto_20190509_2139'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('rank', models.PositiveIntegerField(verbose_name='Rank')),
                ('year', models.PositiveIntegerField(verbose_name='Year')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='meta.Artist', verbose_name='Artist')),
                ('genres', models.ManyToManyField(related_name='albums', to='meta.Genre', verbose_name='Genres')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
