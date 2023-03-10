# Generated by Django 4.1.6 on 2023-02-12 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Ülkeler',
                'verbose_name_plural': 'Ülkeler',
            },
        ),
        migrations.CreateModel(
            name='KayipStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Kayıp Durumları',
                'verbose_name_plural': 'Kayıp Durumları',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Tagler',
                'verbose_name_plural': 'Tagler',
            },
        ),
        migrations.CreateModel(
            name='KayipUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kayip_first_name', models.CharField(db_index=True, max_length=100)),
                ('kayip_last_name', models.CharField(max_length=100)),
                ('cordinate_x', models.FloatField(blank=True, max_length=10, null=True)),
                ('cordinate_y', models.FloatField(blank=True, max_length=10, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('detail', models.TextField(blank=True, null=True)),
                ('status', models.TextField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('age', models.IntegerField(blank=True, db_index=True, null=True)),
                ('kayip_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kayiplar', to='appname.kayipstatus')),
                ('tags', models.ManyToManyField(blank=True, to='appname.tag')),
            ],
            options={
                'verbose_name': 'Kaybolan Kişiler',
                'verbose_name_plural': 'Kaybolan Kişiler',
            },
        ),
        migrations.CreateModel(
            name='IhbarUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ihbar_first_name', models.CharField(max_length=100)),
                ('ihbar_last_name', models.CharField(max_length=100)),
                ('phonenumber', models.CharField(max_length=100)),
                ('eposta', models.EmailField(blank=True, max_length=100, null=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appname.countries')),
            ],
            options={
                'verbose_name': 'Ihbar Eden Kişiler',
                'verbose_name_plural': 'Ihbar Eden Kişiler',
            },
        ),
        migrations.CreateModel(
            name='Ihbar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_created=True, blank=True, null=True)),
                ('access_code', models.IntegerField(blank=True, db_index=True, null=True)),
                ('ihbar_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appname.ihbaruser')),
                ('kayip_user', models.ManyToManyField(to='appname.kayipuser')),
            ],
            options={
                'verbose_name': 'Ihbar',
                'verbose_name_plural': 'Ihbarlar',
            },
        ),
    ]
