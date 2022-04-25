# Generated by Django 3.2.9 on 2022-04-14 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quickstart', '0042_justifs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='justifs',
            name='id_comptable',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='id_comptable', to=settings.AUTH_USER_MODEL),
        ),
    ]
