# Generated by Django 3.2.9 on 2022-04-25 14:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('quickstart', '0046_auto_20220414_1758'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config_rapport',
            fields=[
                ('id_config_rapport', models.AutoField(primary_key=True, serialize=False)),
                ('expression', models.CharField(choices=[('ET', 'AND'), ('OU', 'OR')], max_length=10)),
                ('acteur', models.CharField(choices=[('C', 'Chef de mission'), ('T', 'tout le monde')], max_length=10)),
                ('id_process_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='quickstart.processus')),
            ],
        ),
        migrations.CreateModel(
            name='Rapport_droit',
            fields=[
                ('id_rapport_droit', models.AutoField(primary_key=True, serialize=False)),
                ('consultation_rapport', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='consultation_rapport', to='auth.group')),
                ('id_config_rapport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.config_rapport')),
                ('suppression_rapport', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='suppression_rapport', to='auth.group')),
                ('validation_rapport', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='validation_rapport', to='auth.group')),
            ],
        ),
        migrations.CreateModel(
            name='Rapport',
            fields=[
                ('id_rapport', models.AutoField(primary_key=True, serialize=False)),
                ('resultats_attendu', models.CharField(max_length=500)),
                ('recommendations', models.CharField(max_length=500)),
                ('date_creation', models.DateField()),
                ('date_derniere_modification', models.DateField()),
                ('validation', models.DateField(blank=True, null=True)),
                ('id_createur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_createur', to=settings.AUTH_USER_MODEL)),
                ('id_modificateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_modificateur', to=settings.AUTH_USER_MODEL)),
                ('id_validateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_validateur', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Config_blocage',
            fields=[
                ('id_config_blocage', models.AutoField(primary_key=True, serialize=False)),
                ('id_process_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.processus')),
                ('step_debut', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sep_debut', to='quickstart.stepprocess')),
                ('step_fin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sep_fin', to='quickstart.stepprocess')),
            ],
        ),
        migrations.CreateModel(
            name='Bloque',
            fields=[
                ('id_bloque', models.AutoField(primary_key=True, serialize=False)),
                ('id_envoye_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.envoye')),
                ('step_process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.stepprocess')),
            ],
        ),
    ]