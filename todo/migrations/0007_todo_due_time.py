# Generated by Django 3.0.5 on 2020-06-14 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_auto_20200606_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='due_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='截止时间'),
        ),
    ]
