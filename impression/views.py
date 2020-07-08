from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, resolve
from django.contrib import messages
from django.views.generic import ListView, DetailView, RedirectView, CreateView, UpdateView

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
    context_object_name = 'meeting_agenda'

    def get(self, request, *args, **kwargs):
        try:
            community = Community.objects.get(pk=kwargs['community_pk'])
        except:
            raise Http404 
        members = community.member.all()
        
        # 确认当前用户是圈子成员
        check_community_member(request, community)

        impression_list = GiveImpression.objects.filter(user__in=members).order_by('-created_time')
        my_impression = GiveImpression.objects.filter(user=request.user).order_by('-created_time')

        self.extra_context = {
            'community': community,
            'members': members,
            }
        self.object_list = GiveImpression.objects.filter(community=community).order_by('-created_time')
        context = self.get_context_data()
        return self.render_to_response(context)


def check_community_member(request, community):
    """确认当前用户是圈子成员"""
    if request.user not in community.member.all():
        raise Http404 