# Generated by Django 3.2.9 on 2022-02-07 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0003_auto_20220207_1707'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rights',
            options={'default_permissions': (), 'managed': False, 'permissions': (('billets', "peut actribuer un billet d'avion"), ('validation', 'peut faire une validation'), ('numero', 'peut attribuer le numero'), ('forfait', 'peut changer le forfait'))},
        ),
    ]