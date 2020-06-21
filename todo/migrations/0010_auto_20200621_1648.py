# Generated by Django 3.0.5 on 2020-06-21 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0009_auto_20200621_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='process_status',
            field=models.CharField(choices=[('T', '待办'), ('F', '跟进'), ('C', '完成')], default='T', max_length=1, verbose_name='状态'),
        ),
        migrations.CreateModel(
            name='MeetingAgenda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agenda', models.CharField(max_length=100, verbose_name='议题')),
                ('action_plan', models.TextField(verbose_name='行动方案')),
                ('track_record', models.TextField(verbose_name='跟进记录')),
                ('status', models.CharField(choices=[('B', '新建'), ('F', '跟进中'), ('H', '暂缓'), ('C', '关闭')], default='B', max_length=1, verbose_name='状态')),
                ('proposed_date', models.DateField(verbose_name='提出时间')),
                ('deadline', models.DateField(blank=True, null=True, verbose_name='时间节点')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_modified_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('community', models.ManyToManyField(blank=True, to='todo.Community', verbose_name='圈子')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agenda_owner', to=settings.AUTH_USER_MODEL, verbose_name='负责人')),
                ('proposed_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposed_user', to=settings.AUTH_USER_MODEL, verbose_name='提议人')),
            ],
            options={
                'verbose_name': '会议议题',
                'verbose_name_plural': '会议议题',
            },
        ),
    ]