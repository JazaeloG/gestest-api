# Generated by Django 4.2.5 on 2024-02-04 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_proyecto_usuario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proyecto',
            old_name='usuario',
            new_name='usuario_id',
        ),
    ]
