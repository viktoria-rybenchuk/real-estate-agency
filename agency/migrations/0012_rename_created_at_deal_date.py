# Generated by Django 4.1.7 on 2023-04-01 06:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("agency", "0011_alter_deal_created_at"),
    ]

    operations = [
        migrations.RenameField(
            model_name="deal",
            old_name="created_at",
            new_name="date",
        ),
    ]
