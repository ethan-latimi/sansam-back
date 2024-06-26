# Generated by Django 4.0.5 on 2022-07-02 00:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('farms', '0005_alter_farm_created_alter_log_created_alter_log_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farm',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='log',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='log',
            name='title',
            field=models.CharField(blank=True, default='<function now at 0x7f7d9bc8e1f0>', max_length=255, null=True),
        ),
    ]
