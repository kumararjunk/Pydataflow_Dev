# Generated by Django 2.1.1 on 2019-05-10 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0010_auto_20190510_0701'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nome')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='telefone')),
                ('gender', models.CharField(choices=[('0', ''), ('man', 'homem'), ('woman', 'mulher')], default='0', max_length=5, verbose_name='sexo')),
            ],
            options={
                'verbose_name': 'Contato',
                'verbose_name_plural': 'Contatos',
                'ordering': ('name',),
            },
        ),
    ]
