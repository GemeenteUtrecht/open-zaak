# Generated by Django 2.2.10 on 2020-03-26 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("config", "0002_rename_nlx_inway"),
    ]

    operations = [
        migrations.AlterField(
            model_name="nlxconfig",
            name="outway",
            field=models.URLField(
                blank=True,
                help_text="Example: http://my-outway.nlx:8080",
                verbose_name="outway address",
            ),
        ),
    ]