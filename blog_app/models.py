from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.html import strip_tags

from markdown import Markdown
from mdeditor.fields import MDTextField

# Create your models here.

class Category(models.Model):
    """
    博客文章的分类，每个文章对应一个分类
    django 内置的全部类型可查看文档：
    https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-types
    """

    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, verbose_name='创建人', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    博客文章的标签，一个文章可以拥有多个标签
    """

    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, verbose_name='创建人', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Post(models.Model):
    """
    博客文章表
    包含字段：
    文章标题 - title
    正文 - body
    创建时间 - created_time
    修改时间 - modified_time
    摘要 - excerpt
    分类 - category
    标签 - tags
    作者 - author
    """

    title =  models.CharField('标题', max_length=70)
    body = MDTextField('正文')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')

    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField('摘要', max_length=200, blank=True)

    # 关于ForeignKey、ManyToManyField类型可参考官方文档：
    # https://docs.djangoproject.com/en/2.2/topics/db/models/#relationships
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

    # django.contrib.auth 是 django 内置的应用，专门用于处理网站用户的注册、登录等流程
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    # 记录阅读量
    views = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        # 排序属性，避免在视图函数中频繁指定排序
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    # *args, **kwargs是什么意思？可以接受任意多个变量？
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        # 首先实例化一个 Markdown 类，用于渲染 body 的文本。
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。
        md = Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前 54 个字符赋给 excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_app:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])