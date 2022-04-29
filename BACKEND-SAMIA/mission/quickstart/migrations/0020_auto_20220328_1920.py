# Generated by Django 3.2.9 on 2022-03-28 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0019_rename_service1_service2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employe',
            name='compte_actif',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='employe',
            name='id_service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.service'),
        ),
        migrations.AlterField(
            model_name='employe',
            name='verrou_employe',
            field=models.BooleanField(),
        ),
        migrations.DeleteModel(
            name='Service2',
        ),
    ]