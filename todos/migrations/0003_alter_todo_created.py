# Generated by Django 4.0.5 on 2022-07-02 00:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0002_rename_user_todo_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 2, 0, 18, 53, 32449)),
        ),
    ]
