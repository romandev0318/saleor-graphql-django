# Generated by Django 2.0.3 on 2018-07-24 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0049_auto_20180719_0520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordernote',
            name='is_public',
        ),
    ]
