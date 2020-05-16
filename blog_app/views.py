from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

#from django.http import HttpResponse
import re

from .models import Post, Category, Tag
from .forms import PostForm, CateForm, TagForm

from markdown import markdown, Markdown
from markdown.extensions.toc import TocExtension
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger, PaginationMixin
# Create your views here.

class IndexView(PaginationMixin, ListView):

    # model: 将 model 指定为 Post，告诉 django 我要获取的模型是 Post。
    # template_name: 指定这个视图渲染的模板。
    # context_object_name: 指定获取的模型列表数据保存的变量名，这个变量会被传递给模板。
    model = Post
    template_name = 'blog_app/index.html'
    context_object_name = 'post_list'

    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 10

@method_decorator(login_required, name='dispatch')
class MyBlogView(IndexView):

    template_name = 'blog_app/my_blog.html'

    def get_queryset(self):
        author = self.request.user
        return super(MyBlogView, self).get_queryset().filter(author=author)

class CategoryView(IndexView):

    # 与Index共用页面，继承IndexView
    # 使用了 self.kwargs.get('pk') 来获取从 URL 捕获的分类 id 值
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        user = self.kwargs.get('user')
        return super(CategoryView, self).get_queryset().filter(category=cate).filter(author=user)

class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        user = self.kwargs.get('user')
        return super(ArchiveView, self).get_queryset().filter(created_time__year=year,
            created_time__month=month).filter(author=user)

class ArchiveDayView(IndexView):

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        user = self.kwargs.get('user')
        return super(ArchiveDayView, self).get_queryset().filter(created_time__year=year,
            created_time__month=month, created_time__day=day).filter(author=user)

class TagView(IndexView):

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        user = self.kwargs.get('user')
        return super(TagView, self).get_queryset().filter(tags=tag).filter(author=user)

class AuthorView(IndexView):

    def get_queryset(self):
        author = self.kwargs.get('author')
        return super(AuthorView, self).get_queryset().filter(author=author)

class PostDetailView(DetailView):

    model = Post
    template_name = 'blog_app/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        print(request.user)
        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super().get_object(queryset=None)
        md = Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify)
        ])
        post.body = md.convert(post.body)

        m =re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''

        return post

def search(request):
    # 首先我们使用 request.GET.get('q') 获取到用户提交的搜索关键词
    # 用户通过表单 get 方法提交的数据 Django 为我们保存在 request.GET 里，
    # 这是一个类似于 Python 字典的对象，所以我们使用 get 方法从字典里取出键 q 对应的值，即用户的搜索关键词
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog_app:index')

    # 从 from django.db.models 中引入了一个新的东西：Q 对象。
    # Q 对象用于包装查询表达式，其作用是为了提供复杂的查询逻辑。
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog_app/index.html', {'post_list': post_list})

@login_required
def new_post(request):
    """发布文章"""
    
    # 判断客户端是移动端还是PC端
    flag = check_agents_mobile_or_pc(request)

    if request.method != 'POST':
        # 未提交数据，创建一个空表单
        form = PostForm()

        form.fields['category'].queryset = Category.objects.filter(creator=request.user)
        form.fields['tags'].queryset = Tag.objects.filter(creator=request.user)

    else:
        # POST提交的数据，对数据进行处理
        form = PostForm(data=request.POST)
        if form.is_valid(): 
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return HttpResponseRedirect(reverse('blog_app:my_blog'))

    context = {'form': form, 'flag': flag}
    return render(request, 'blog_app/new_post.html', context)

@login_required
def edit_post(request, post_pk):
    """发布文章"""
    post = Post.objects.get(pk=post_pk)

    # 修改的条目关联的主题不是登录用户时，禁止访问
    check_topic_owner(request, post)
    # 判断客户端是移动端还是PC端
    flag = check_agents_mobile_or_pc(request)

    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = PostForm(instance=post)

        form.fields['category'].queryset = Category.objects.filter(creator=request.user)
        form.fields['tags'].queryset = Tag.objects.filter(creator=request.user)

    else:
        # POST提交的数据，对数据进行处理
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid(): 
            form.save()
            return HttpResponseRedirect(reverse('blog_app:my_blog'))

    context = {'form': form, 'flag': flag, 'post': post}
    return render(request, 'blog_app/edit_post.html', context)

@login_required
def new_cate(request):
    """新增类别"""

    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = CateForm()
    else:
        # POST提交的数据，对数据进行处理
        form = CateForm(data=request.POST)
        if form.is_valid(): 
            new_cate = form.save(commit=False)
            new_cate.creator = request.user
            new_cate.save()
            return HttpResponseRedirect(reverse('blog_app:new_post'))

    context = {'form': form}
    return render(request, 'blog_app/new_cate.html', context)

@login_required
def new_tag(request):
    """新增类别"""

    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = TagForm()
    else:
        # POST提交的数据，对数据进行处理
        form = TagForm(data=request.POST)
        if form.is_valid(): 
            new_tag = form.save(commit=False)
            new_tag.creator = request.user
            new_tag.save()
            return HttpResponseRedirect(reverse('blog_app:new_post'))

    context = {'form': form}
    return render(request, 'blog_app/new_tag.html', context)


def check_agents_mobile_or_pc(request):
    USER_AGENT = request.META["HTTP_USER_AGENT"]
    agents = ["Android", "iPhone",
            "SymbianOS", "Windows Phone",
            "iPad", "iPod"]
    flag = True
    for agent in agents:
        if agent in USER_AGENT:
            flag = False
            break
    return(flag)

def check_topic_owner(request, post):
    """确认请求的主题属于当前用户"""
    if post.author != request.user:
        raise Http404 

""" 函数视图
def index(request):
    # 博客首页

    post_list = Post.objects.all()

    context = {'post_list': post_list}
    return render(request, 'blog_app/index.html', context)

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 阅读量 +1
    post.increase_views()

    md = Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify)
    ])
    post.body = md.convert(post.body)

    m =re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    context = {'post': post}
    return render(request, 'blog_app/detail.html', context)

def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
        created_time__month=month)
    
    context = {'post_list': post_list}
    return render(request, 'blog_app/index.html', context)

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)

    context = {'post_list': post_list}
    return render(request, 'blog_app/index.html', context)

def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t)

    context = {'post_list': post_list}
    return render(request, 'blog_app/index.html', context)

def archive_day(request, year, month, day):
    post_list = Post.objects.filter(created_time__year=year,
        created_time__month=month,
        created_time__day=day)
    
    context = {'post_list': post_list}
    return render(request, 'blog_app/index.html', context)

def author(request, author):
    post_list = Post.objects.filter(author=author)
    
    context = {'post_list': post_list}
    return render(request, 'blog_app/index.html', context)

""" 