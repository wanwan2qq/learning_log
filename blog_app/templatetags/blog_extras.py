from django import template
from django.db.models.aggregates import Count

from ..models import Post, Category, Tag

register = template.Library()

@register.inclusion_tag('blog_app/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, user, num=5):
    return {
        'recent_post_list': Post.objects.filter(author_id=user).order_by('-created_time')[:num],
    }

@register.inclusion_tag('blog_app/inclusions/_hot_posts.html', takes_context=True)
def show_hot_posts(context, num=10):
    return {
        'recent_post_list': Post.objects.order_by('-views')[:num],
    }


@register.inclusion_tag('blog_app/inclusions/_archives.html', takes_context=True)
def show_archives(context, user):
    # 相当于：select year, month, count(id) as num_posts from post group by year, month
    data_list = Post.objects.filter(author_id=user).values('created_time__year', 'created_time__month').annotate(num_posts=Count('id')).order_by()
    return {
        'date_list': data_list,
        'post_author': user,
    }

@register.inclusion_tag('blog_app/inclusions/_categories.html', takes_context=True)
def show_categories(context, user):
    # 代码中的 Count 方法为我们做了这个事，它接收一个和 Categoty 相关联的模型参数名（这里是 Post，通过 ForeignKey 关联的），
    # 然后它便会统计 Category 记录的集合中每条记录下的与之关联的 Post 记录的行数，也就是文章数，最后把这个值保存到 num_posts 属性中。
    # __gt: great than 大于
    category_list = Category.objects.filter(post__author=user).annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
        'post_author': user,
    }

@register.inclusion_tag('blog_app/inclusions/_tags.html', takes_context=True)
def show_tags(context, user):
    tag_list = Tag.objects.filter(post__author=user).annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
        'post_author': user,
    }