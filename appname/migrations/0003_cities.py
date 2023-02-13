# Generated by Django 4.1.6 on 2023-02-13 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appname', '0002_alter_kayipuser_age'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('coordinate_x', models.FloatField(blank=True, max_length=10, null=True)),
                ('coordinate_y', models.FloatField(blank=True, max_length=10, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appname.countries')),
            ],
        ),
    ]