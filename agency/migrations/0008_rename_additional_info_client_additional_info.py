# Generated by Django 4.1.7 on 2023-03-30 07:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("agency", "0007_remove_client_budget"),
    ]

    operations = [
        migrations.RenameField(
            model_name="client",
            old_name="Additional_info",
            new_name="additional_info",
        ),
    ]
