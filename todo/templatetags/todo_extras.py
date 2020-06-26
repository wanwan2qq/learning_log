from django import template
from django.db.models.aggregates import Count
from django.contrib.auth.models import User

from ..models import Todo, Community

register = template.Library()

@register.inclusion_tag('todo/inclusions/_my_community.html', takes_context=True)
def show_my_community(context, user):
    member = User.objects.get(id=user.id)
    return {
        'my_community': member.member.all(),
    }

@register.inclusion_tag('todo/inclusions/_todo_list.html', takes_context=True)
def todo_list(context, todo_list, member, user):
    return {
        'todo_list': todo_list,
        'member': member,
        'user': user,
    }

@register.inclusion_tag('todo/inclusions/_my_todo_list.html', takes_context=True)
def my_todo_list(context, todo_list, user):
    return {
        'todo_list': todo_list,
        'user': user
    }

@register.inclusion_tag('todo/inclusions/_meeting_agenda_list.html', takes_context=True)
def meeting_agenda_list(context, meeting_agenda, community, status=None):
    return {
        'meeting_agenda': meeting_agenda,
        'status': status,
        'community': community,
    }