# Generated by Django 3.2.9 on 2022-03-03 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0006_alter_rights_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projet',
            name='date_debut',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='projet',
            name='date_fin',
            field=models.DateField(),
        ),
    ]
