# Generated by Django 4.1.10 on 2023-08-05 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_strip_product_id_product_stripe_price_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='strip_product_id',
            new_name='stripe_product_id',
        ),
    ]
