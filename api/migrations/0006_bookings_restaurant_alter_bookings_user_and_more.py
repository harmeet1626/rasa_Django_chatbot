# Generated by Django 4.2.7 on 2023-12-18 07:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0005_restaurants'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='restaurant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bookings',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.restaurants'),
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='chats',
            name='chatroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chats', to='api.chatroom'),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='chat',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='api.chats'),
        ),
    ]
