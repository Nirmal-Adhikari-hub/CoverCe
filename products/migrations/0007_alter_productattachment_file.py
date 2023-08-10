# Generated by Django 4.1.10 on 2023-08-05 16:04

import django.core.files.storage
from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_rename_strip_product_id_product_stripe_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattachment',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='storages.backends.azure_storage.AzureStorage'), upload_to=products.models.handle_product_attachment_upload),
        ),
    ]
