# Generated by Django 3.2.4 on 2021-10-28 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0157_alter_product_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='sort_order',
            field=models.IntegerField(db_index=True, editable=False, null=True),
        ),
    ]