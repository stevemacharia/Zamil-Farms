# Generated by Django 3.2.17 on 2023-02-15 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='product_quantity',
            field=models.IntegerField(default=0, max_length=100),
        ),
    ]
