# Generated by Django 5.1.2 on 2024-10-25 03:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0011_alter_tratamiento_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='fecha_registro',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
