# Generated by Django 4.2.3 on 2023-07-12 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_is_logged'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_logged',
        ),
    ]
