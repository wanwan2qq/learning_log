"""定义Todo的URL模式"""

from django.urls import path, re_path
from django.views.generic.base import RedirectView

from . import views

app_name = 'impression'
urlpatterns = [
    # 主页
    path('', views.impression_index, name='impression_index'),

]