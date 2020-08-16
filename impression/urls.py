"""定义Todo的URL模式"""

from django.urls import path, re_path
from django.views.generic.base import RedirectView

from . import views

app_name = 'impression'
urlpatterns = [
    
    path('', views.impression_index, name='impression_index'),
    path('my_impression/<int:community_pk>', views.ImpressionMyPageListView.as_view(), name='my_impression'),
    path('member_impression/<int:community_pk>/<int:member_pk>', views.ImpressionMemberPageListView.as_view(), name='member_impression'),
    path('impression_pick_list/<int:member_pk>/<int:impression_pk>', views.ImpressionPickListView.as_view(), name='impression_pick_list'),
    path('add_impression/<int:member_pk>/<int:impression_pk>', views.AddImpressionCreateView.as_view(), name='add_impression')
]