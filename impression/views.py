from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, resolve
from django.contrib import messages
from django.views.generic import ListView, DetailView, RedirectView, CreateView, UpdateView

from django.db.models import Count, Sum

# Create your views here.
from .models import Impression, GiveImpression, PickCoin, KeyUser
from todo.models import Community



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
    success_url = '/impression/impression_my_page.html'
    model = GiveImpression
    fields = ['impression','remarks','picks','user','praise_user']

def check_community_member(request, community):
    """确认当前用户是圈子成员"""
    if request.user not in community.member.all():
        raise Http404 