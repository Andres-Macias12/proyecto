# Generated by Django 5.1.2 on 2024-10-23 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0007_cita_tratamiento'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='fotos_pacientes/'),
        ),
    ]
