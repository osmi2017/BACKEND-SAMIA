# Generated by Django 3.2.9 on 2022-02-04 12:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rights',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('supervision', 'peut superviser'), ('approbation', 'peut faire une approbbation'), ('numero', 'peut attribuer le numero'), ('forfait', 'peut changer le forfait'), ('validation_rh', 'peut validation du drh'), ('validation_tg', 'peut validation du tg')),
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Bareme',
            fields=[
                ('id_bareme', models.AutoField(primary_key=True, serialize=False)),
                ('jour_max', models.IntegerField()),
                ('jour_min', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Bareme_detail',
            fields=[
                ('id_bareme_detail', models.AutoField(primary_key=True, serialize=False)),
                ('id_bareme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.bareme')),
            ],
        ),
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id_categorie', models.AutoField(primary_key=True, serialize=False)),
                ('nom_categorie', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('Code', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=52)),
                ('Continent', models.CharField(choices=[('Africa', 'Africa'), ('Asia', 'Asia'), ('Europe', 'Europe'), ('North America', 'North America'), ('South America', 'South America'), ('Oceania', 'Oceania'), ('Antarctica', 'Antarctica')], max_length=52)),
                ('Region', models.CharField(max_length=52)),
                ('SurfaceArea', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('IndepYear', models.IntegerField()),
                ('Population', models.IntegerField()),
                ('LifeExpectancy', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('GNP', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('GNPOld', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('LocalName', models.CharField(max_length=52)),
                ('GovernmentForm', models.CharField(max_length=52)),
                ('HeadOfState', models.CharField(max_length=52)),
                ('Capital', models.IntegerField()),
                ('Code2', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('id_employe', models.AutoField(primary_key=True, serialize=False)),
                ('nom_employe', models.CharField(max_length=50)),
                ('prenoms_employe', models.CharField(max_length=50)),
                ('date_naiss_employe', models.DateField()),
                ('matricule_employe', models.CharField(max_length=50)),
                ('email_employe', models.CharField(max_length=50)),
                ('tel_employe', models.CharField(max_length=50)),
                ('fonction_employe', models.CharField(max_length=100)),
                ('login_employe', models.CharField(max_length=20)),
                ('password_employe', models.CharField(max_length=50)),
                ('compte_actif', models.CharField(max_length=10)),
                ('verrou_employe', models.CharField(max_length=10)),
                ('date_creation', models.DateTimeField()),
                ('id_categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.categorie')),
                ('id_createur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='createur', to=settings.AUTH_USER_MODEL)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Entite',
            fields=[
                ('id_entite', models.AutoField(primary_key=True, serialize=False)),
                ('nom_entite', models.CharField(max_length=50)),
                ('logo', models.ImageField(upload_to='logo')),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id_notifications', models.AutoField(primary_key=True, serialize=False)),
                ('A', models.CharField(max_length=255)),
                ('cc', models.CharField(max_length=255)),
                ('message', models.CharField(max_length=255)),
                ('prochaine_action', models.CharField(max_length=50)),
                ('sent', models.CharField(max_length=20)),
                ('auteur', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Pole',
            fields=[
                ('id_pole', models.AutoField(primary_key=True, serialize=False)),
                ('nom_pole', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Processus',
            fields=[
                ('id_process', models.AutoField(primary_key=True, serialize=False)),
                ('type_process', models.CharField(choices=[('NO', 'Normal'), ('PO', 'Pôle'), ('PR', 'Projet')], max_length=2)),
                ('id_relatated', models.IntegerField()),
                ('nom_processus', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Regime',
            fields=[
                ('id_regime', models.AutoField(primary_key=True, serialize=False)),
                ('nom_regime', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TypeProjet',
            fields=[
                ('id_typeprojet', models.AutoField(primary_key=True, serialize=False)),
                ('nom_typeprojet', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Typesteps',
            fields=[
                ('id_typesteps', models.AutoField(primary_key=True, serialize=False)),
                ('nom_typesteps', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id_zone', models.AutoField(primary_key=True, serialize=False)),
                ('nom_zone', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Worldcities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255)),
                ('city_ascii', models.CharField(max_length=255)),
                ('lat', models.CharField(max_length=255)),
                ('longi', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('iso2', models.CharField(max_length=255)),
                ('iso3', models.CharField(max_length=255)),
                ('admin_name', models.CharField(max_length=255)),
                ('capital', models.CharField(max_length=255)),
                ('population', models.CharField(max_length=255)),
                ('zipe', models.CharField(max_length=255)),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.zone')),
            ],
        ),
        migrations.CreateModel(
            name='Stepprocess',
            fields=[
                ('id_stepprocess', models.AutoField(primary_key=True, serialize=False)),
                ('type_steps', models.CharField(max_length=50)),
                ('order_steps', models.IntegerField()),
                ('cible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('id_process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.processus')),
                ('type_steps1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.typesteps')),
            ],
        ),
        migrations.CreateModel(
            name='Projet',
            fields=[
                ('id_projet', models.AutoField(primary_key=True, serialize=False)),
                ('nom_projet', models.CharField(max_length=50)),
                ('date_debut', models.DateTimeField()),
                ('date_fin', models.DateTimeField()),
                ('id_entite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.entite')),
                ('type_projet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.typeprojet')),
            ],
        ),
        migrations.CreateModel(
            name='Montant_zone',
            fields=[
                ('id_montant_zone', models.AutoField(primary_key=True, serialize=False)),
                ('perdiem', models.IntegerField()),
                ('hebergement', models.IntegerField()),
                ('id_bareme_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.bareme_detail')),
                ('id_zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.zone')),
            ],
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id_mission', models.AutoField(primary_key=True, serialize=False)),
                ('date_demande', models.DateTimeField()),
                ('objet_mission', models.CharField(max_length=500)),
                ('depart_mission', models.DateField()),
                ('retour_mission', models.DateField()),
                ('lieu_mission', models.CharField(max_length=500)),
                ('statut_mission', models.CharField(max_length=100)),
                ('numero_mission', models.CharField(max_length=20)),
                ('destination_mission', models.CharField(max_length=50)),
                ('contexte_mission', models.CharField(max_length=2000)),
                ('objectifs_mission', models.CharField(max_length=2000)),
                ('frais_extra', models.CharField(max_length=20)),
                ('chg_extra', models.CharField(max_length=20)),
                ('frais_changes', models.CharField(max_length=50)),
                ('current_step', models.IntegerField()),
                ('relance_cible', models.CharField(max_length=50)),
                ('avion', models.CharField(choices=[('True', 'OUI'), ('False', 'NON')], max_length=5)),
                ('id_demandeur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('regime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.regime')),
                ('type_processus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.processus')),
            ],
        ),
        migrations.CreateModel(
            name='Envoye',
            fields=[
                ('id_envoye', models.AutoField(primary_key=True, serialize=False)),
                ('nom_employe', models.CharField(max_length=20)),
                ('prenom_employe', models.CharField(max_length=50)),
                ('role', models.CharField(max_length=20)),
                ('billet_avion', models.CharField(max_length=20)),
                ('statut_des_justifs', models.CharField(max_length=20)),
                ('id_employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employe', to='quickstart.employe')),
                ('id_mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='envoye', to='quickstart.mission')),
            ],
        ),
        migrations.AddField(
            model_name='entite',
            name='id_pole_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.pole'),
        ),
        migrations.CreateModel(
            name='Bareme_envoye',
            fields=[
                ('id_bareme_envoye', models.AutoField(primary_key=True, serialize=False)),
                ('hebergement', models.IntegerField()),
                ('perdiem', models.IntegerField()),
                ('total_cout', models.IntegerField()),
                ('id_bareme_detail_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.bareme_detail')),
                ('id_bareme_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.bareme')),
                ('id_envoye_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='envoye', to='quickstart.envoye')),
                ('id_mission_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.mission')),
                ('id_montant_zone_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.montant_zone')),
            ],
        ),
        migrations.AddField(
            model_name='bareme_detail',
            name='id_categorie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.categorie'),
        ),
        migrations.AddField(
            model_name='bareme',
            name='id_processus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.processus'),
        ),
        migrations.AddField(
            model_name='bareme',
            name='id_regime',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.regime'),
        ),
    ]
