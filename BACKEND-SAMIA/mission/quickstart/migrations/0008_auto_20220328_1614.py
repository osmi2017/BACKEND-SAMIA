# Generated by Django 3.2.9 on 2022-03-28 16:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0007_auto_20220303_2115'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id_service', models.AutoField(primary_key=True, serialize=False)),
                ('nom_service', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='employe',
            name='id_entite',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quickstart.entite'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employe',
            name='id_service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quickstart.service'),
            preserve_default=False,
        ),
    ]
