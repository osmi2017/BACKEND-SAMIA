# Generated by Django 3.2.9 on 2022-03-28 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0009_auto_20220328_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employe',
            name='id_entite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.entite'),
        ),
    ]
