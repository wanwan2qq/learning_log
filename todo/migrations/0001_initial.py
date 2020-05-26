# Generated by Django 3.0.5 on 2020-05-19 23:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='圈子')),
                ('member', models.ManyToManyField(blank=True, related_name='member', to=settings.AUTH_USER_MODEL, verbose_name='成员')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL, verbose_name='圈主')),
            ],
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='优先级')),
            ],
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('todo', models.CharField(max_length=100, verbose_name='待办任务')),
                ('text', mdeditor.fields.MDTextField(verbose_name='备注')),
                ('status', models.BooleanField()),
                ('start_time', models.DateTimeField(verbose_name='开始时间')),
                ('finish_time', models.DateTimeField(blank=True, verbose_name='完成时间')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_modified_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('community', models.ManyToManyField(blank=True, to='todo.Community', verbose_name='圈子')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='主人')),
                ('priority', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.Priority', verbose_name='优先级')),
            ],
        ),
    ]