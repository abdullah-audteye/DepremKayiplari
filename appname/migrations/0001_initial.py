# Generated by Django 4.1.6 on 2023-02-08 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IhbarUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ihbar_first_name', models.CharField(max_length=100)),
                ('ihbar_last_name', models.CharField(max_length=100)),
                ('phonenumber', models.CharField(max_length=100)),
                ('eposta', models.EmailField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TagArabic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='KayipUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kayip_first_name', models.CharField(max_length=100)),
                ('kayip_last_name', models.CharField(max_length=100)),
                ('kayip_phone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('cordinate_x', models.FloatField(blank=True, max_length=10, null=True)),
                ('cordinate_y', models.FloatField(blank=True, max_length=10, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('detail', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('tags', models.ManyToManyField(blank=True, to='appname.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Ihbar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ihbar_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appname.ihbaruser')),
                ('kayip_user', models.ManyToManyField(to='appname.kayipuser')),
            ],
        ),
    ]
