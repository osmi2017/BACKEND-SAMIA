# Generated by Django 3.2.9 on 2022-06-07 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0061_alter_rights_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rights',
            options={'default_permissions': (), 'managed': False, 'permissions': (('billets', "peut actribuer un billet d'avion"), ('validation', 'peut faire une validation'), ('numero', 'peut attribuer le numero'), ('forfait', 'peut changer le forfait'), ('paiement', 'peut faire un paiement'), ('justification', 'peut valider des justificatifs'), ('traite_mission', 'peut traiter des missions'), ('valide_rapport', 'peut valider les rapports'))},
        ),
        migrations.AlterField(
            model_name='config_blocage',
            name='step_debut',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='step_debut', to='quickstart.stepprocess'),
        ),
        migrations.AlterField(
            model_name='config_blocage',
            name='step_fin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='step_fin', to='quickstart.stepprocess'),
        ),
    ]
