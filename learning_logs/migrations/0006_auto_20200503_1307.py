# Generated by Django 3.0.5 on 2020-05-03 13:07

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0005_topic_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='text',
            field=mdeditor.fields.MDTextField(),
        ),
    ]