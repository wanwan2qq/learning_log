"""learning_log URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

# from . import settings

# 解决admin样式加载不出来问题
# from django.conf import settings
# from django.conf.urls.static import static


urlpatterns = [
    path('jet/', include('jet.urls', 'jet')), # Django JET URLS
    path('admin/', admin.site.urls),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('', include(('learning_logs.urls', 'learning_logs'), namespace='learning_logs')),

    # 静态文件收集后，admin的静态文件从项目的STATIC_ROOT指向目录下读取
    # path(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    # path(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
