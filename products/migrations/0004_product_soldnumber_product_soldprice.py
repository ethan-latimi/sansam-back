# Generated by Django 4.0.5 on 2022-07-06 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='soldNumber',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='soldPrice',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
