"""定义Todo的URL模式"""

from django.urls import path, re_path
from django.views.generic.base import RedirectView

from . import views

app_name = 'todo'
urlpatterns = [
    # 主页
    path('', views.todo_index, name='todo_index'),
    path('community/<int:community_pk>', views.community, name='community'),

    # 任务相关
    path('my_todo/', views.my_todo, name='my_todo'),
    path('new_todo/', views.new_todo, name='new_todo'),
    path('edit_todo/<int:todo_pk>', views.edit_todo, name='edit_todo'),
    path('see_todo/<int:pk>', views.TodoDetailView.as_view(), name='see_todo'),

    # 圈子相关
    path('new_community/', views.new_community, name='new_community'),
    path('edit_community/<int:community_pk>', views.edit_community, name='edit_community'),
    path('exit_community/<int:community_pk>', views.exit_community, name='exit_community'),

    # 关注
    path('follow/<int:todo_pk>', views.follow, name='follow'),
    path('unfollow/<int:todo_pk>', views.unfollow, name='unfollow'),

    # 议题相关
    path('meeting_agenda_list/<int:community_pk>', views.MeetingAgendaListView.as_view(), name='meeting_agenda_list'),
    path('meeting_agenda_detail/<int:community_pk>/<int:agenda_pk>', views.MeetingAgendaDetailView.as_view(), name='meeting_agenda_detail'),
    path('new_meeting_agenda/<int:community_pk>', views.MeetingAgendaCreateView.as_view(), name='new_meeting_agenda'),
    path('edit_meeting_agenda/<int:community_pk>/<int:agenda_pk>', views.MeetingAgendaUpdateView.as_view(), name='edit_meeting_agenda'),
    path('edit_track_record/<int:community_pk>/<int:agenda_pk>', views.TrackRecordUpdateView.as_view(), name='edit_track_record'),
]