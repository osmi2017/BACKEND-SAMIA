# Generated by Django 3.2.9 on 2022-03-28 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0010_alter_employe_id_entite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employe',
            name='id_service',
        ),
    ]
