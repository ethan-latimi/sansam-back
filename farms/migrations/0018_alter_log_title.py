# Generated by Django 4.0.5 on 2022-07-13 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farms', '0017_alter_log_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='title',
            field=models.CharField(blank=True, default='<function now at 0x7fa18b38e5e0>', max_length=255, null=True),
        ),
    ]
