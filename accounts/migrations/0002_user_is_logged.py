# Generated by Django 4.2.3 on 2023-07-12 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_logged',
            field=models.BooleanField(default=False),
        ),
    ]
