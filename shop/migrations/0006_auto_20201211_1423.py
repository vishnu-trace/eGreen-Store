# Generated by Django 3.1.3 on 2020-12-11 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20201211_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='password',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='password',
            field=models.CharField(default='', max_length=64),
        ),
    ]
