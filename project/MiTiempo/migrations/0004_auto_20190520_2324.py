# Generated by Django 2.1.7 on 2019-05-20 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MiTiempo', '0003_usuario_cookie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pueblo',
            name='id_url',
        ),
        migrations.AddField(
            model_name='pueblo',
            name='url_html',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='pueblo',
            name='url_xml',
            field=models.CharField(default='', max_length=500),
        ),
    ]
