# Generated by Django 2.1.7 on 2019-05-22 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MiTiempo', '0009_auto_20190521_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cookie_navegador', models.CharField(max_length=20)),
                ('estado', models.IntegerField(default=0)),
            ],
        ),
    ]
