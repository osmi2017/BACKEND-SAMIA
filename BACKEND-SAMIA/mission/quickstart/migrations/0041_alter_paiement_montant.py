# Generated by Django 3.2.9 on 2022-04-12 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0040_paiement_id_envoye_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paiement',
            name='montant',
            field=models.IntegerField(),
        ),
    ]
