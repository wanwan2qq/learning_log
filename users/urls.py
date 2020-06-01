"""为应用程序user定义URL模式"""

from django.urls import path, re_path
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy

from . import views

urlpatterns = [
    # 登录页面
    path('login/', LoginView.as_view(template_name='users/login.html'),
        name='login'),

    # 注销
    path('logout/', views.logout_view, name='logout'),

    # 注册页面
    path('register/', views.register, name='register'),

    # 基本信息
    path('basic_info/', views.basic_info, name='basic_info'),

    # 修改密码
    path('password_change/', 
        PasswordChangeView.as_view(
            template_name='users/password_change.html',
            success_url = reverse_lazy('todo:todo_index')), 
        name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
]
