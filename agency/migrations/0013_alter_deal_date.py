# Generated by Django 4.1.7 on 2023-04-01 06:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("agency", "0012_rename_created_at_deal_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deal",
            name="date",
            field=models.DateField(),
        ),
    ]
