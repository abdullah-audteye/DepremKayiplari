# Generated by Django 4.1.6 on 2023-02-11 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_managers_user_date_joined_user_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Kullanici', 'verbose_name_plural': 'Kullanicilar'},
        ),
    ]