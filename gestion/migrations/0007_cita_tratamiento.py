# Generated by Django 5.1.2 on 2024-10-23 22:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0006_delete_ciudad_remove_paciente_medicamentos_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='tratamiento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion.tratamiento'),
        ),
    ]
