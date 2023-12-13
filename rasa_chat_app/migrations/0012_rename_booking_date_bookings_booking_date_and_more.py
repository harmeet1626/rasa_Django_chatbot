# Generated by Django 4.2.7 on 2023-12-13 12:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rasa_chat_app', '0011_alter_chatroom_created_at_alter_chats_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookings',
            old_name='Booking_date',
            new_name='booking_date',
        ),
        migrations.AlterField(
            model_name='bookings',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 13, 12, 47, 50, 939643)),
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 13, 12, 47, 50, 937987)),
        ),
        migrations.AlterField(
            model_name='chats',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 13, 12, 47, 50, 938469)),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 13, 12, 47, 50, 939159)),
        ),
    ]
