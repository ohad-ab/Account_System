# Generated by Django 4.2.3 on 2023-07-20 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_chat_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='chats',
            field=models.ManyToManyField(blank=True, to='accounts.chat_users'),
        ),
    ]
