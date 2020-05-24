from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

# Create your views here.
from .models import Todo, Community, Priority
from .forms import TodoForm

@login_required
def todo_index(request):
    """圈子里的任务"""
    member = User.objects.get(id=request.user.id)
    communities = member.member.all()  # 第二个member是community模型User字段的一个别名
    community = member.member.first()
    try:
        members = community.member.all()
        today_todos = community.todo_set.filter(created_time__date=timezone.now().date())
        previous_todos = community.todo_set.filter(created_time__date__lt=timezone.now().date()).filter(status=False)
    except AttributeError:
        members = []
        today_todos = []
        previous_todos = []



    context = {
        'today_todos': today_todos, 
        'previous_todos': previous_todos, 
        'communities': communities,
        'community': community, 
        'members': members}
    return render(request, 'todo/todo_index.html', context)

@login_required
def community(request, community_pk):
    """圈子里的任务"""
    member = User.objects.get(id=request.user.id)
    communities = member.member.all()
    community = member.member.get(pk=community_pk)
    members = community.member.all()
    today_todos = community.todo_set.filter(created_time__date=timezone.now().date())
    previous_todos = community.todo_set.filter(created_time__date__lt=timezone.now().date()).filter(status=False)

    context = {
        'today_todos': today_todos, 
        'previous_todos': previous_todos, 
        'communities': communities,
        'community': community, 
        'members': members}
    return render(request, 'todo/todo_index.html', context)


@login_required
def new_todo(request):
    """发布任务"""
    
    # 判断客户端是移动端还是PC端
    # flag = check_agents_mobile_or_pc(request)
    member = User.objects.get(id=request.user.id)

    if request.method != 'POST':
        # 未提交数据，创建一个空表单
        form = TodoForm()

        form.fields['community'].queryset = member.member.all()

    else:
        # POST提交的数据，对数据进行处理
        form = TodoForm(data=request.POST)
        if form.is_valid(): 
            new_todo = form.save(commit=False)
            new_todo.owner = request.user
            new_todo.save()
            # 模型中有多对多的字段时，需要对表单使用save_m2m()方法保存一下
            form.save_m2m()
            return HttpResponseRedirect(reverse('todo:todo_index'))

    context = {'form': form}
    return render(request, 'todo/new_todo.html', context)

@login_required
def edit_todo(request, todo_pk):
    """发布任务"""

    todo = Todo.objects.get(id=todo_pk)
    
    # 判断客户端是移动端还是PC端
    # flag = check_agents_mobile_or_pc(request)
    member = User.objects.get(id=request.user.id)

    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = TodoForm(instance=todo)

        form.fields['community'].queryset = member.member.all()

    else:
        # POST提交的数据，对数据进行处理
        form = TodoForm(instance=todo, data=request.POST)
        if form.is_valid(): 
            form.save()
            # 模型中有多对多的字段时，需要对表单使用save_m2m()方法保存一下
            # form.save_m2m()
            return HttpResponseRedirect(reverse('todo:my_todo'))

    context = {'form': form, 'todo': todo}
    return render(request, 'todo/edit_todo.html', context)

def my_todo(request):
    """我的任务"""

    member = User.objects.get(id=request.user.id)
    communities = member.member.all()
    todos = Todo.objects.filter(owner=member).filter(status=False).order_by('-priority', '-last_modified_time')
    finish_todos = Todo.objects.filter(owner=member).filter(status=True).order_by('-last_modified_time')[:20]

    context = {
        'todos': todos, 
        'finish_todos': finish_todos, 
        'communities': communities,
        }
    return render(request, 'todo/my_todo.html', context)
    
