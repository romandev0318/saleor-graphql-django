# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-16 15:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0029_auto_20180111_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderhistoryentry',
            name='comment',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
