# Generated by Django 3.2.9 on 2022-04-14 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0045_alter_justifs_id_envoye_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='envoye',
            name='justifier',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='envoye',
            name='validation_justier',
            field=models.BooleanField(default=False),
        ),
    ]
