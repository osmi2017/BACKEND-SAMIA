# Generated by Django 3.2.9 on 2022-04-29 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quickstart', '0054_auto_20220429_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rapport',
            name='id_validateur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='id_validateur', to=settings.AUTH_USER_MODEL),
        ),
    ]
