# Generated by Django 3.0.5 on 2020-08-18 21:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('impression', '0003_giveimpression_praise_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='impression.PickCoin', verbose_name='用户'),
        ),
        migrations.AlterField(
            model_name='pickcoin',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]