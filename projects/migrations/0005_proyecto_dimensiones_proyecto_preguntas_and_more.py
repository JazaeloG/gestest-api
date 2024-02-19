# Generated by Django 4.2.5 on 2024-02-19 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_rename_usuario_id_proyecto_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='dimensiones',
            field=models.ManyToManyField(to='projects.dimensiones'),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='preguntas',
            field=models.ManyToManyField(to='projects.preguntas'),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='tests',
            field=models.ManyToManyField(to='projects.tests'),
        ),
    ]
