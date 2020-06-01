"""定义Todo的URL模式"""

from django.urls import path, re_path

from . import views

app_name = 'todo'
urlpatterns = [
    # 主页
    path('', views.todo_index, name='todo_index'),
    path('community/<int:community_pk>', views.community, name='community'),
    path('new_todo/', views.new_todo, name='new_todo'),
    path('my_todo/', views.my_todo, name='my_todo'),
    path('edit_todo/<int:todo_pk>', views.edit_todo, name='edit_todo'),
    path('new_community/', views.new_community, name='new_community'),
    path('edit_community/<int:community_pk>', views.edit_community, name='edit_community'),
    path('exit_community/<int:community_pk>', views.exit_community, name='exit_community'),
]