# Generated by Django 4.1.7 on 2023-04-06 08:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("agency", "0019_alter_area_agent_alter_client_search_area_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deal",
            name="date",
            field=models.DateField(),
        ),
    ]
