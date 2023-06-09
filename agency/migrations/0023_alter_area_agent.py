# Generated by Django 4.1.7 on 2023-04-06 09:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("agency", "0022_remove_area_unique_name_of_area_alter_area_agent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="area",
            name="agent",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="areas",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
