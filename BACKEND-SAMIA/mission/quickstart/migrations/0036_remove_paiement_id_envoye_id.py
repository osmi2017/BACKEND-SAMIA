# Generated by Django 3.2.9 on 2022-04-12 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0035_paiement_id_envoye_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paiement',
            name='id_envoye_id',
        ),
    ]