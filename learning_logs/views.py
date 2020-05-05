from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# 尝试将md格式转换成html - 后台转换，有些格式有问题，暂时不用
from markdown import markdown
# import mistune

# Create your views here.
def index(request):
    """学习笔记的主页"""
    try:
        topics = Topic.objects.filter(owner=request.user)
    except TypeError:
        context = {}
    else:
        entries = Entry.objects.filter(topic__in=topics).order_by('-date_added')[:5]
        context = {'entries': entries}
    return render(request, 'learning_logs/index.html', context)

def check_topic_owner(request, topic):
    """确认请求的主题属于当前用户"""
    if topic.owner != request.user:
        raise Http404    

@login_required
def topics(request):
    """显示所有的主题"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    topics_v = topics.values()
    for topic in topics_v:
        entries = Entry.objects.filter(topic=topic['id'])
        topic['entries_num'] = len(list(entries))
    context = {'topics': topics_v}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """显示单个主题及其所有的条目"""
    topic = Topic.objects.get(id=topic_id)
    # 确认请求的主题属于当前用户
    check_topic_owner(request, topic)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据： 创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

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

@login_required
def new_entry(request, topic_id):
    """在特定的主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)
    # 修改的条目关联的主题不是登录用户时，禁止访问
    check_topic_owner(request, topic)
    # 判断客户端是移动端还是PC端
    flag = check_agents_mobile_or_pc(request)
    if request.method != 'POST':
        # 未提交数据，创建一个空表单
        form = EntryForm()
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid() and (topic.owner == request.user): # 19-4 保护页面
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', 
                args=[topic_id]))

    context = {'topic': topic, 'form': form, 'flag': flag}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """编辑既有条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # 确认请求的主题属于当前用户
    check_topic_owner(request, topic)
    # 判断客户端是移动端还是PC端
    flag = check_agents_mobile_or_pc(request)
    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form, 'flag': flag}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def see_entry(request, entry_id):
    """查看既有条目"""
    entry = Entry.objects.get(id=entry_id).text
    entry_id = Entry.objects.get(id=entry_id).id
    topic = Entry.objects.get(id=entry_id).topic
    time = Entry.objects.get(id=entry_id).date_added
    # 确认请求的主题属于当前用户
    check_topic_owner(request, topic)
    context = {'entry': entry, 'topic': topic, 'time': time, 'entry_id': entry_id}
    return render(request, 'learning_logs/see_entry_front.html', context)