# Generated by Django 3.2.9 on 2022-03-28 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0012_employe_id_service'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Service',
            new_name='Service1',
        ),
        migrations.RemoveField(
            model_name='employe',
            name='id_service',
        ),
    ]
