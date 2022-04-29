# Generated by Django 3.2.9 on 2022-04-25 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0048_fiches'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloque',
            name='id_envoye_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='envoye1', to='quickstart.envoye'),
        ),
        migrations.AlterField(
            model_name='bloque',
            name='step_process',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='process1', to='quickstart.stepprocess'),
        ),
    ]