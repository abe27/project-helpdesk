# Generated by Django 5.1 on 2024-09-04 03:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("report_repair", "0003_alter_repairoutside_end_date_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="report",
            name="employee",
        ),
        migrations.AddField(
            model_name="report",
            name="staff",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="staff_reports",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
