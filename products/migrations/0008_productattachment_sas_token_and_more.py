# Generated by Django 4.1.10 on 2023-08-07 07:20

import cfehome.custom_storage.custom_azure
from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_productattachment_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='productattachment',
            name='sas_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='productattachment',
            name='file',
            field=models.FileField(storage=cfehome.custom_storage.custom_azure.AzureProtectedStorage(), upload_to=products.models.handle_product_attachment_upload),
        ),
    ]
