# Generated by Django 3.2.4 on 2021-08-09 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table_service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tableservice',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]