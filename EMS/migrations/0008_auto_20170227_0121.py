# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-26 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0007_auto_20170222_0654'),
    ]

    operations = [
        migrations.AddField(
            model_name='energy',
            name='day',
            field=models.CharField(default='-', max_length=10),
        ),
        migrations.AddField(
            model_name='energy',
            name='hour',
            field=models.CharField(default='-', max_length=10),
        ),
        migrations.AddField(
            model_name='energy',
            name='month',
            field=models.CharField(default='-', max_length=10),
        ),
        migrations.AddField(
            model_name='energy',
            name='year',
            field=models.CharField(default='-', max_length=10),
        ),
    ]
