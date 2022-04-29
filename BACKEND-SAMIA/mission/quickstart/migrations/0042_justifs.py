# Generated by Django 3.2.9 on 2022-04-14 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quickstart', '0041_alter_paiement_montant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Justifs',
            fields=[
                ('id_justif', models.AutoField(primary_key=True, serialize=False)),
                ('piece', models.FileField(upload_to='justifs')),
                ('Type_piece', models.CharField(max_length=50)),
                ('Libelle', models.CharField(max_length=250)),
                ('Montant', models.IntegerField()),
                ('commentaire', models.CharField(blank=True, max_length=250, null=True)),
                ('id_comptable', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='id_comptable', to=settings.AUTH_USER_MODEL)),
                ('id_envoye_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='quickstart.envoye')),
            ],
        ),
    ]