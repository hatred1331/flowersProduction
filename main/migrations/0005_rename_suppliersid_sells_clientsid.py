# Generated by Django 4.2.7 on 2023-12-24 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_productsforpurchase_price_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sells',
            old_name='suppliersId',
            new_name='clientsId',
        ),
    ]
