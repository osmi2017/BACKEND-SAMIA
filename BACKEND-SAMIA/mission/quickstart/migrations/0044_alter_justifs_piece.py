# Generated by Django 3.2.9 on 2022-04-14 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0043_alter_justifs_id_comptable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='justifs',
            name='piece',
            field=models.FileField(default='justifs/img.png', upload_to='justifs'),
        ),
    ]
