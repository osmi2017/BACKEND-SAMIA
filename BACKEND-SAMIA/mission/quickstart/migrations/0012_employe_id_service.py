# Generated by Django 3.2.9 on 2022-03-28 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0011_remove_employe_id_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='employe',
            name='id_service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quickstart.service'),
        ),
    ]
