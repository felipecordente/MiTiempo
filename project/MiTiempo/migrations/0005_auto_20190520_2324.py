# Generated by Django 2.1.7 on 2019-05-20 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MiTiempo', '0004_auto_20190520_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pueblo',
            name='url_html',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='pueblo',
            name='url_xml',
            field=models.CharField(max_length=500),
        ),
    ]
