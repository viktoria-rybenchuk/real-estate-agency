# Generated by Django 4.1.7 on 2023-03-30 04:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("agency", "0004_property_agent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="property",
            name="agent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="properties",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
