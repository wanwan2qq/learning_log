from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, resolve
from django.contrib import messages
from django.views.generic import ListView, DetailView, RedirectView, CreateView, UpdateView, FormView

from django.db.models import Count, Sum

# Create your views here.
from .models import Impression, GiveImpression, PickCoin
from todo.models import Community
from .form import NewImpressionForm



@login_required
def impression_index(request):
    """
    印象首页，选择要进入的圈子
    """
    user = request.user
    communities = user.member.all()

    context = {'communities': communities}
    return render(request, 'impression/impression_index.html', context)


class ImpressionMyPageListView(ListView):
    """我的印象"""
    template_name = 'impression/impression_my_page.html'
    # queryset = MeetingAgenda.objects.all()
    # paginate_by = 10
    context_object_name = 'my_impression'

    def add_extra_context(self, *args, **kwargs):
        try:
            community = Community.objects.get(pk=kwargs['community_pk'])
        except:
            raise Http404 
        members = community.member.all()
        
        # 确认当前用户是圈子成员
        check_community_member(self.request, community)

        impression_list = GiveImpression.objects.filter(user__in=members).values(
            'impression__id', 'impression__impression','user', 'user__username', 
            'user__first_name').annotate(Sum('picks')).order_by('-picks__sum', 'user')
        my_picks = PickCoin.objects.get(user=self.request.user)
        members_impression = []
        impressions = Impression.objects.filter(preset=True)

        for member in members:
            m_impression = impression_list.filter(user=member.id).first()
            if m_impression:
                members_impression.append(m_impression)
            else:
                m_impression = {
                    'impression__impression': '暂无',
                    'user': member.id,
                    'user__username': member.username,
                    'user__first_name': member.first_name,
                    'picks__sum': 0,
                    }
                members_impression.append(m_impression)

        self.extra_context = {
            'community': community,
            'members': members,
            'impression_list': impression_list,
            'my_picks': my_picks,
            'members_impression': members_impression,
            'impressions': impressions,
            }

    def get(self, request, *args, **kwargs):
        self.add_extra_context(self, *args, **kwargs)

        self.object_list = self.extra_context['impression_list'].filter(user=request.user.id)
        # self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

class ImpressionMemberPageListView(ImpressionMyPageListView):
    """圈子成员的印象"""
    template_name = 'impression/impression_member_page.html'
    context_object_name = 'member_impression'

    def get(self, request, *args, **kwargs):
        "重写get函数，增加查看用户的信息"
        self.add_extra_context(self, *args, **kwargs)

        try:
            user = User.objects.get(pk=kwargs['member_pk'])
        except:
            raise Http404

        self.extra_context['user'] = user

        self.object_list = self.extra_context['impression_list'].filter(user=kwargs['member_pk'])
        # self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

class ImpressionPickListView(ListView):
    """印象明细"""
    model = GiveImpression
    template_name = 'impression/impression_pick_list.html'
    context_object_name = 'impression_pick_list'

    def get_queryset(self):
        member = self.kwargs.get('member_pk')
        impression = self.kwargs.get('impression_pk')
        # month = self.kwargs.get('month')
        return super(ListView, self).get_queryset().filter(user=member).filter(impression=impression)

class AddImpressionCreateView(CreateView):
    """添加印象"""
    template_name = 'impression/add_impression.html'
    model = GiveImpression
    fields = ['remarks','picks']

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
        my_picks = PickCoin.objects.get(user=self.request.user)
        member = User.objects.get(pk=kwargs['member_pk'])
        impression = Impression.objects.get(pk=kwargs['impression_pk'])
        
        self.extra_context = {
            'url': url,
            'community': community,
            'member': member,
            'my_picks': my_picks,
            'impression': impression,
        }
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        重写post，form_valid增加新参数request, community
        """
        form = self.get_form()
        success_kwargs = {
            'community_pk': kwargs['community_pk'],
            'member_pk': kwargs['member_pk'],
        }
        self.success_url = reverse('impression:member_impression', kwargs=success_kwargs)
        try:
            community = Community.objects.get(pk=kwargs['community_pk'])
        except:
            raise Http404

        if form.is_valid():
            return self.form_valid(form, request, kwargs['impression_pk'], kwargs['member_pk'])
        else:
            return self.form_invalid(form)

    def form_valid(self, form, request, impression_pk, member_pk):
        """自动添加圈子、提议人、提议时间"""
        self.object = form.save(commit=False)
        self.object.impression = Impression.objects.get(pk=impression_pk)
        self.object.user = User.objects.get(pk=member_pk)
        self.object.praise_user = request.user
        
        #更新用户coin
        pick_coin = PickCoin.objects.get(user=request.user)
        if pick_coin.pick_coin_num >= self.object.picks:
            pick_coin.pick_coin_num = pick_coin.pick_coin_num - self.object.picks
            pick_coin.save()
            # 成功提示
            messages.add_message(request, messages.SUCCESS, '印象添加成功', extra_tags='success')
        else:
            # 失败提示
            messages.add_message(request, messages.ERROR, 'Pick币不足', extra_tags='error')
            return self.form_invalid(form)

        return super().form_valid(form)


class NewImpressionCreateView(CreateView):
    template_name = 'impression/new_impression.html'
    form_class = NewImpressionForm

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
        my_picks = PickCoin.objects.get(user=self.request.user)
        member = User.objects.get(pk=kwargs['member_pk'])
        
        self.extra_context = {
            'url': url,
            'community': community,
            'member': member,
            'my_picks': my_picks,
        }
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        重写post，form_valid增加新参数request, community
        """
        form = self.get_form()
    
        try:
            community = Community.objects.get(pk=kwargs['community_pk'])
        except:
            raise Http404

        if form.is_valid():
            return self.form_valid(form, request, **kwargs)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, request, **kwargs):
        """添加自定义印象，补充打印象双方信息，更新coin笔"""
        
        self.object = form.save(commit=False)
        self.object.preset = False

        new_impression = Impression.objects.filter(impression=self.object.impression).first()

        if not new_impression:
            self.object = form.save()
            new_impression = self.object
        
        success_kwargs = {
            'community_pk': kwargs['community_pk'],
            'member_pk': kwargs['member_pk'],
            'impression_pk': new_impression.pk,
        }
        self.success_url = reverse('impression:add_impression', kwargs=success_kwargs)

        return HttpResponseRedirect(self.get_success_url())


def check_community_member(request, community):
    """确认当前用户是圈子成员"""
    if request.user not in community.member.all():
        raise Http404 