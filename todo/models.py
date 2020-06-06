from django.db import models
from django.contrib.auth.models import User

from mdeditor.fields import MDTextField

# Create your models here.

class Community(models.Model):
    """
    圈子模型
    两个字段都关联了User对象，需要通过related_name区分
    """

    name = models.CharField('圈子', max_length=100)
    member = models.ManyToManyField(User, related_name='member', related_query_name="member", verbose_name='成员', blank=True)
    owner = models.ForeignKey(User, related_name='owner', verbose_name='圈主', on_delete=models.CASCADE)

    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time =models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '圈子'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

"""
class CommunityOwner(models.Model):

    owner = models.ForeignKey(User, verbose_name='圈主', on_delete=models.CASCADE)
    community = models.ForeignKey(Community, verbose_name='圈子', on_delete=models.CASCADE)
"""


class Priority(models.Model):
    """优先级模型"""

    name = models.CharField('优先级', max_length=100)

    class Meta:
        verbose_name = '优先级'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Todo(models.Model):
    """待办任务模型"""

    todo = models.CharField('待办任务', max_length=100)
    text = MDTextField('备注', blank=True)
    
    owner = models.ForeignKey(User, verbose_name='主人', on_delete=models.CASCADE)
    community = models.ManyToManyField(Community, verbose_name='圈子', blank=True)

    is_week_todo = models.BooleanField('周重点')

    status = models.BooleanField('已完成')
    priority = models.ForeignKey(Priority, verbose_name='优先级', on_delete=models.CASCADE)

    start_time = models.DateTimeField('开始时间', blank=True, null=True)
    finish_time =models.DateTimeField('完成时间', blank=True, null=True)

    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time =models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '待办任务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.todo


class InterestingSentences(models.Model):
    """有趣的句子"""

    sentence = models.TextField('有趣的句子')
    auther = models.CharField('作者', max_length=100)

    class Meta:
        verbose_name = '有趣的句子'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sentence + " —— " + self.auther