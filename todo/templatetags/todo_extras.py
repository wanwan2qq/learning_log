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