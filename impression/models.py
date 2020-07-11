from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Impression(models.Model):
    """
    印象标签，包含预置标签和自定义标签
    """
    impression = models.CharField('印象', max_length=100)
    preset = models.BooleanField('系统预置')
    
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '印象标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.impression


class GiveImpression(models.Model):
    """
    给他人点赞，描述对他人的印象
    """
    impression = models.ForeignKey(Impression, verbose_name='印象', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    remarks = models.CharField('备注', max_length=100)
    picks = models.DecimalField('pick数', max_digits=6, decimal_places=0)
    praise_user = models.ForeignKey(User,related_name='praise_user', verbose_name='点赞用户', on_delete=models.CASCADE)
    
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '印象'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.impression.impression


class PickCoin(models.Model):
    """
    个人Pick币数量
    """
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    pick_coin_num = models.DecimalField('pick币', max_digits=6, decimal_places=0)

    class Meta:
        verbose_name = 'Pick币数量'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.user, self.pick_coin_num)

class KeyUser(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    enable = models.BooleanField('启用', default=True)

    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '关键用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username

