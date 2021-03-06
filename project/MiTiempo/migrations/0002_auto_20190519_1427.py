# Generated by Django 2.1.7 on 2019-05-19 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MiTiempo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='color',
            field=models.CharField(default='red', max_length=50),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='color_fondo',
            field=models.CharField(default='blue', max_length=50),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='pueblos',
            field=models.ManyToManyField(blank=True, to='MiTiempo.Pueblo'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='size',
            field=models.IntegerField(default=12),
        ),
    ]
