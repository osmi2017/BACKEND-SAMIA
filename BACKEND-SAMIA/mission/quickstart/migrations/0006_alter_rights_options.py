# Generated by Django 3.2.9 on 2022-02-10 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0005_auto_20220209_1727'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rights',
            options={'default_permissions': (), 'managed': False, 'permissions': (('billets', "peut actribuer un billet d'avion"), ('validation', 'peut faire une validation'), ('numero', 'peut attribuer le numero'), ('forfait', 'peut changer le forfait'), ('paiement', 'peut faire un paiement'), ('justification', 'peut valider des justificatifs'), ('traite_mission', 'peut traiter des missions'))},
        ),
    ]
