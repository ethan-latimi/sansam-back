# Generated by Django 4.0.4 on 2022-05-30 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='receiver',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
