# Generated by Django 4.1.7 on 2023-04-06 11:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("agency", "0028_remove_deal_additinal_info_deal_deal"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deal",
            name="date",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="deal",
            name="deal",
            field=models.CharField(blank=True, max_length=63),
        ),
    ]
