# Generated by Django 3.0.5 on 2020-07-08 15:41

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0011_auto_20200621_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingagenda',
            name='action_plan',
            field=mdeditor.fields.MDTextField(verbose_name='行动方案'),
        ),
        migrations.AlterField(
            model_name='meetingagenda',
            name='track_record',
            field=mdeditor.fields.MDTextField(blank=True, verbose_name='跟进记录'),
        ),
    ]
