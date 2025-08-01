# Generated by Django 5.1.6 on 2025-02-28 09:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pest_weed_db', '0002_crop'),
        ('reports', '0002_pestsighting_time_treatmentoutcome_time_applied'),
    ]

    operations = [
        migrations.AddField(
            model_name='pestsighting',
            name='crop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pest_sightings', to='pest_weed_db.crop'),
        ),
    ]
