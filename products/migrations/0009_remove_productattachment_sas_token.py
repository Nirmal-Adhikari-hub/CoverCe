# Generated by Django 4.1.10 on 2023-08-07 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_productattachment_sas_token_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productattachment',
            name='sas_token',
        ),
    ]
