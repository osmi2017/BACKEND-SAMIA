# Generated by Django 3.2.9 on 2022-05-04 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('quickstart', '0056_remove_rapport_id_modificateur'),
    ]

    operations = [
        migrations.AddField(
            model_name='config_rapport',
            name='Validateur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='auth.group'),
        ),
    ]
