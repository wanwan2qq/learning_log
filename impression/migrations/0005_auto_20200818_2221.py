# Generated by Django 3.0.5 on 2020-08-18 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('impression', '0004_auto_20200818_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='pickcoin',
            name='key_user',
            field=models.BooleanField(default=False, verbose_name='组长'),
        ),
        migrations.DeleteModel(
            name='KeyUser',
        ),
    ]