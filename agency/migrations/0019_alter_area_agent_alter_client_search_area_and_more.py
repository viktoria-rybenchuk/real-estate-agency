# Generated by Django 4.1.7 on 2023-04-05 21:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("agency", "0018_remove_client_unique_email_remove_property_title_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="area",
            name="agent",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="areas",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="client",
            name="search_area",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="clients",
                to="agency.area",
            ),
        ),
        migrations.AlterField(
            model_name="property",
            name="agent",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="properties",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="property",
            name="area",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="properties",
                to="agency.area",
            ),
        ),
    ]
