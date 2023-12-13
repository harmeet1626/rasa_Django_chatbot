# Generated by Django 4.2.7 on 2023-12-13 12:40

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rasa_chat_app', '0010_chats_type_alter_chatroom_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 13, 12, 40, 48, 429853)),
        ),
        migrations.AlterField(
            model_name='chats',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 13, 12, 40, 48, 430241)),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 13, 12, 40, 48, 430665)),
        ),
        migrations.CreateModel(
            name='Bookings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuisine', models.CharField(max_length=255)),
                ('people_num', models.IntegerField()),
                ('outdoor_seating', models.BooleanField(default=False)),
                ('Booking_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(default=datetime.datetime(2023, 12, 13, 12, 40, 48, 431077))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'bookings',
            },
        ),
    ]
