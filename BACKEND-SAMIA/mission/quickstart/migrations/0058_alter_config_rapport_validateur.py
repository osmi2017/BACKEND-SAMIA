# Generated by Django 3.2.9 on 2022-05-04 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0057_config_rapport_validateur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config_rapport',
            name='Validateur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='quickstart.typesteps'),
        ),
    ]
