from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, resolve
from django.contrib import messages
from django.views.generic import ListView, DetailView, RedirectView, CreateView, UpdateView

from datetime import timedelta

# Create your views here.
from .models import Todo, Community, Priority, InterestingSentences, MeetingAgenda
from .forms import TodoForm, CommunityForm, MeetingAgendaForm

@login_required
def todo_index(request):
    """圈子里的任务"""
    member = User.objects.get(id=request.user.id)
    communities = member.member.all()  # 第二个member是community模型User字段的一个别名
    community = member.member.first()
    week = timezone.now().isocalendar()[1]
    now = timezone.now()
    now_add_4 = timezone.now() + timedelta(hours=4)
    sentence = InterestingSentences.objects.order_by("?").first()
    try:
        members = community.member.all()
        today_todos = community.todo_set.filter(start_time__date=timezone.now().date())
        follow_todos = community.todo_set.filter(
            start_time__date__lt=timezone.now().date()).filter(status=False).filter(process_status='F')
        previous_todos = community.todo_set.filter(
            start_time__date__lt=timezone.now().date()).filter(status=False).filter(process_status='T')
        week_todos = community.todo_set.filter(start_time__week=week).filter(is_week_todo=True)
    except AttributeError:
        members = []
        today_todos = []
        follow_todos = []
        previous_todos = []
        week_todos = []

    context = {
        'today_todos': today_todos, 
        'follow_todos': follow_todos,
        'previous_todos': previous_todos, 
        'communities': communities,
        'community': community, 
        'members': members,
        'week_todos': week_todos,
        'week': week,
        'now': now,
        'now_add_4': now_add_4,
        'sentence': sentence,
        }
    return render(request, 'todo/todo_index.html', context)

@login_required
def community(request, community_pk):
    """圈子里的任务"""
    member = User.objects.get(id=request.user.id)
    communities = member.member.all()
    week = timezone.now().isocalendar()[1]
    now = timezone.now()
    now_add_4 = timezone.now() + timedelta(hours=4)
    sentence = InterestingSentences.objects.order_by("?").first()
    try:
        community = member.member.get(pk=community_pk) # 从当前用户的圈子中找到指定的圈子
        members = community.member.all()
        today_todos = community.todo_set.filter(start_time__date=timezone.now().date())
        follow_todos = community.todo_set.filter(
            start_time__date__lt=timezone.now().date()).filter(status=False).filter(process_status='F')
        previous_todos = community.todo_set.filter(
            start_time__date__lt=timezone.now().date()).filter(status=False).filter(process_status='T')
        week_todos = community.todo_set.filter(start_time__week=week).filter(is_week_todo=True)
    except:
        raise Http404 

    context = {
        'today_todos': today_todos, 
        'follow_todos': follow_todos,
        'previous_todos': previous_todos, 
        'communities': communities,
        'community': community, 
        'members': members,
        'week_todos': week_todos,
        'week': week,
        'now': now,
        'now_add_4': now_add_4,
        'sentence': sentence,
        }
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
            new_todo.status = False
            new_todo.save()
            if not new_todo.start_time:
                new_todo.start_time = new_todo.created_time
            if new_todo.process_status == 'C' and (not new_todo.finish_time):
                new_todo.finish_time = new_todo.last_modified_time
                new_todo.status = True
            elif not new_todo.process_status != 'C':
                new_todo.finish_time = None
                new_todo.status = False
            new_todo.save()
            # 模型中有多对多的字段时，需要对表单使用save_m2m()方法保存一下
            form.save_m2m()

            messages.add_message(request, messages.SUCCESS, '任务添加成功！', extra_tags='success')
            if 'submit_back' in request.POST:
                return HttpResponseRedirect(reverse('todo:todo_index'))
            elif 'submit_add' in request.POST:
                return HttpResponseRedirect(reverse('todo:new_todo'))

    context = {'form': form}
    return render(request, 'todo/new_todo.html', context)

@login_required
def edit_todo(request, todo_pk):
    """修改任务"""

    todo = Todo.objects.get(id=todo_pk)

    # 修改的任务不属于登录用户时，禁止访问
    check_todo_owner(request, todo)
    
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
            edit_todo = form.save()
            if not edit_todo.start_time:
                edit_todo.start_time = edit_todo.created_time
            if edit_todo.process_status == 'C' and (not edit_todo.finish_time):
                edit_todo.finish_time = edit_todo.last_modified_time
                edit_todo.status = True
            elif not edit_todo.process_status != 'C':
                edit_todo.finish_time = None
                edit_todo.status = False
            edit_todo.save()
            # 模型中有多对多的字段时，需要对表单使用save_m2m()方法保存一下
            # form.save_m2m()
            messages.add_message(request, messages.SUCCESS, '任务修改成功！', extra_tags='success')
            return HttpResponseRedirect(reverse('todo:my_todo'))

    context = {'form': form, 'todo': todo}
    return render(request, 'todo/edit_todo.html', context)

class TodoDetailView(DetailView):
    """任务详情"""
    model = Todo
    template_name = 'todo/see_todo.html'
    context_object_name = 'todo'

    def get(self, request, *args, **kwargs):
        try:
            self.extra_context = {'url': request.META["HTTP_REFERER"]}
        except KeyError:
            self.extra_context = {'url': ""}
        return super().get(request, *args, **kwargs)

@login_required
def my_todo(request):
    """我的任务"""

    member = User.objects.get(id=request.user.id)
    communities = member.member.all()
    T_todos = Todo.objects.filter(owner=member).filter(status=False).filter(process_status='T').order_by('-priority', '-last_modified_time')
    F_todos = Todo.objects.filter(owner=member).filter(status=False).filter(process_status='F').order_by('-priority', '-last_modified_time')
    follow_todos = member.todo_follower.all().filter(status=False).order_by('-priority', '-last_modified_time')
    finish_todos = Todo.objects.filter(owner=member).filter(status=True).order_by('-last_modified_time')[:20]

    context = {
        'T_todos': T_todos, 
        'F_todos': F_todos, 
        'follow_todos': follow_todos,
        'finish_todos': finish_todos, 
        'communities': communities,
        }
    return render(request, 'todo/my_todo.html', context)

@login_required
def new_community(request):
    """
    新建圈子
    """

    if request.method != 'POST':
        form = CommunityForm()
    else:
        form = CommunityForm(data=request.POST)
        if form.is_valid():
            new_community = form.save(commit=False)
            new_community.owner = request.user
            new_community.save()
            form.save_m2m()
            new_community.member.add(request.user)
            
            messages.add_message(request, messages.SUCCESS, '圈子新建成功！', extra_tags='success')
            return HttpResponseRedirect(reverse('todo:todo_index'))

    context = {'form': form}
    return render(request, 'todo/new_community.html', context)

@login_required
def edit_community(request, community_pk):
    """
    修改圈子
    """
    community = Community.objects.get(pk=community_pk)

    # 只有圈主可以修改圈子，非圈主返回404
    check_community_owner(request, community)

    if request.method != 'POST':
        form = CommunityForm(instance=community)
    else:
        form = CommunityForm(instance=community, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('todo:todo_index'))

    context = {'form': form, 'community': community}
    return render(request, 'todo/edit_community.html', context)

@login_required
def exit_community(request, community_pk):
    """
    退出圈子
    """
    community = Community.objects.get(pk=community_pk)
    community.member.remove(request.user)
    return HttpResponseRedirect(reverse('todo:todo_index'))

@login_required
def follow(request, todo_pk):
    """关注任务"""
    todo = Todo.objects.get(pk=todo_pk)
    todo.follower.add(request.user)
    url = request.META["HTTP_REFERER"]
    return HttpResponseRedirect(url)

@login_required
def unfollow(request, todo_pk):
    """关注任务"""
    todo = Todo.objects.get(pk=todo_pk)
    todo.follower.remove(request.user)
    url = request.META["HTTP_REFERER"]
    return HttpResponseRedirect(url)


class MeetingAgendaListView(ListView):
    """议题列表"""
    template_name = 'todo/meeting_agenda_list.html'
    queryset = MeetingAgenda.objects.all()
    # paginate_by = 10
    context_object_name = 'meeting_agenda'

    def get(self, request, *args, **kwargs):
        try:
            community = Community.objects.get(pk=kwargs['community_pk'])
        except:
            raise Http404 
        members = community.member.all()
        

        # 确认当前用户是圈子成员
        check_community_member(request, community)

        self.extra_context = {
            'community': community,
            'members': members,
            }
        self.object_list = MeetingAgenda.objects.filter(community=community).order_by('-created_time')
        context = self.get_context_data()
        return self.render_to_response(context)

class MeetingAgendaDetailView(DetailView):
    """议题详情"""
    model = MeetingAgenda
    template_name = 'todo/meeting_agenda_detail.html'
    context_object_name = 'agenda'
    slug_field = 'community'
    slug_url_kwarg = 'community_pk'
    pk_url_kwarg = 'agenda_pk'
    query_pk_and_slug = True

    def get(self, request, *args, **kwargs):
        try:
            self.extra_context = {'url': request.META["HTTP_REFERER"]}
        except KeyError:
            self.extra_context = {'url': ""}
        return super().get(request, *args, **kwargs)

class MeetingAgendaCreateView(CreateView):
    """新建议题"""
    # initial = MeetingAgenda
    template_name = 'todo/new_meeting_agenda.html'
    form_class = MeetingAgendaForm

    def get(self, request, *args, **kwargs):
        """增加圈子和url变量"""
        try:
            community = Community.objects.get(pk=kwargs['community_pk'])
        except:
            raise Http404
        try:
            url = request.META["HTTP_REFERER"]
        except KeyError:
            url = ""

        self.extra_context = {
            'community': community,
            'url': url,
        }
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        重写post，form_valid增加新参数request, community
        """
        form = self.get_form()
        self.success_url = reverse('todo:meeting_agenda_list', kwargs=kwargs)
        try:
            community = Community.objects.get(pk=kwargs['community_pk'])
        except:
            raise Http404

        if form.is_valid():
            return self.form_valid(form, request, community)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, request, community):
        """自动添加圈子、提议人、提议时间"""
        self.object = form.save(commit=False)
        self.object.community = community
        self.object.proposed_date = timezone.now().date()
        self.object.proposed_user = request.user
        # 成功提示
        messages.add_message(request, messages.SUCCESS, '新议题创建成功！', extra_tags='success')
        return super().form_valid(form)

class MeetingAgendaUpdateView(UpdateView):
    """修改议题"""
    model = MeetingAgenda
    form_class = MeetingAgendaForm
    template_name = 'todo/edit_meeting_agenda.html'
    # success_url = '/todo'
    context_object_name = 'agenda'
    slug_field = 'community'
    slug_url_kwarg = 'community_pk'
    pk_url_kwarg = 'agenda_pk'
    query_pk_and_slug = True

    def get(self, request, *args, **kwargs):
        try:
            self.extra_context = {'url': request.META["HTTP_REFERER"]}
        except KeyError:
            self.extra_context = {'url': ""}
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        重写post，form_valid增加新参数request, community
        """
        form = self.get_form()
        self.success_url = reverse('todo:meeting_agenda_list', kwargs={'community_pk': kwargs['community_pk']})

        # 成功提示
        messages.add_message(request, messages.SUCCESS, '议题修改成功！', extra_tags='success')
        return super().post(request, *args, **kwargs)

class TrackRecordUpdateView(MeetingAgendaUpdateView):
    """修改议题的跟进记录"""

    fields = ['track_record']
    form_class = None


# 辅助函数：1）确认任务所属；2）确认圈子所属
def check_todo_owner(request, todo):
    """确认任务属于当前用户"""
    if todo.owner != request.user:
        raise Http404 

def check_community_owner(request, community):
    """确认圈子属于当前用户"""
    if community.owner != request.user:
        raise Http404 

def check_community_member(request, community):
    """确认当前用户是圈子成员"""
    if request.user not in community.member.all():
        raise Http404 