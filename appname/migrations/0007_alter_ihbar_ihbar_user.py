# Generated by Django 4.1.6 on 2023-02-07 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("appname", "0006_alter_kayipuser_cordinate_x_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ihbar",
            name="ihbar_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="appname.ihbaruser",
            ),
        ),
    ]
