# Generated by Django 3.2.9 on 2022-04-29 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0055_alter_rapport_id_validateur'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rapport',
            name='id_modificateur',
        ),
    ]