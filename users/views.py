from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .forms import BasicInfoForm

# Create your views here.

def logout_view(request):
    """注销用户"""
    logout(request)
    return HttpResponseRedirect(reverse('blog_app:index'))

def register(request):
    """注册新用户"""
    if request.method != 'POST':
        # 显示空的注册表单
        form = UserCreationForm()
    else:
        # 处理填写好的表单
        form =UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # 让用户自动登录，再重定向到主页
            authenticated_user = authenticate(username=new_user.username,
                password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('todo:todo_index'))

    context = {'form': form}
    return render(request, 'users/register.html', context)

def basic_info(request):
    """
    修改基本信息
    """
    
    if request.method != 'POST':
        # 显示当前用户的基本信息
        form = BasicInfoForm(instance=request.user)
    else:
        # 处理填写好的表单
        form = BasicInfoForm(instance=request.user, data=request.POST)
        if form.is_valid:
            try:
                form.save()
                return HttpResponseRedirect(reverse('todo:todo_index'))
            except ValueError:
                print(form)
    
    context = {'form': form}
    return render(request, 'users/basic_info.html', context)