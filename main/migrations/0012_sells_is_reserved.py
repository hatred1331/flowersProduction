# Generated by Django 4.2.7 on 2023-12-27 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_status_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='sells',
            name='is_reserved',
            field=models.BooleanField(default=False),
        ),
    ]
