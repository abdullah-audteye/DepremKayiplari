# Generated by Django 4.1.6 on 2023-02-11 09:54

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('object', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]