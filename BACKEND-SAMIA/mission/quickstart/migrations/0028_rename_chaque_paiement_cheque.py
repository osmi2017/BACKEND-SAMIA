# Generated by Django 3.2.9 on 2022-04-12 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0027_alter_paiement_chaque'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paiement',
            old_name='cheque',
            new_name='cheque',
        ),
    ]
