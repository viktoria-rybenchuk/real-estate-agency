# Generated by Django 4.2 on 2023-04-30 18:22

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("agency", "0033_alter_property_property_type"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="agent",
            options={"ordering": ("last_name",)},
        ),
        migrations.AlterModelOptions(
            name="property",
            options={
                "ordering": ("created_at",),
                "verbose_name": "property",
                "verbose_name_plural": "properties",
            },
        ),
    ]
