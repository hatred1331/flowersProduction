# Generated by Django 4.2.7 on 2023-12-24 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_rename_purchaseid_productsforsell_sellid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sells',
            name='amount_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
    ]
