# Generated by Django 4.2.7 on 2023-12-28 06:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0007_alter_bookings_restaurant_alter_bookings_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tickets',
            name='chat',
        ),
        migrations.AddField(
            model_name='tickets',
            name='booking_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.bookings'),
        ),
        migrations.AddField(
            model_name='tickets',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]