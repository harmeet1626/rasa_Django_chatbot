# Generated by Django 4.2.7 on 2023-12-11 06:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rasa_chat_app', '0004_alter_chatroom_created_at_alter_chats_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 11, 6, 40, 18, 332225)),
        ),
        migrations.AlterField(
            model_name='chats',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 11, 6, 40, 18, 333045)),
        ),
        migrations.AlterField(
            model_name='chats',
            name='question',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 11, 6, 40, 18, 332627)),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='document_url',
            field=models.FileField(default='', upload_to='static/documents'),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='chatroom',
            table='Chatroom',
        ),
        migrations.AlterModelTable(
            name='chats',
            table='Chats',
        ),
        migrations.AlterModelTable(
            name='tickets',
            table='Tickets',
        ),
    ]