# Generated by Django 3.2.4 on 2021-08-02 07:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0028_voucher_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]