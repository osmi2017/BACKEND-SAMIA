# Generated by Django 3.2.9 on 2022-04-12 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0026_auto_20220412_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paiement',
            name='chaque',
            field=models.BooleanField(default=False),
        ),
    ]