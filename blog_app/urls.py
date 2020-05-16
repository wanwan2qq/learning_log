
from django.urls import path, re_path

from .import views

app_name = 'blog_app'
urlpatterns = [
    # 类视图url规则
    path('', views.IndexView.as_view(), name='index'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>/<int:user>/', views.ArchiveView.as_view(), name='archive'),
    path('categories/<int:pk>/<int:user>/', views.CategoryView.as_view(), name='category'),
    path('tags/<int:pk>/<int:user>/', views.TagView.as_view(), name='tag'),
    path('archives_day/<int:year>/<int:month>/<int:day>/<int:user>', views.ArchiveDayView.as_view(), name='archive_day'),
    path('author/<int:author>', views.AuthorView.as_view(), name='author'),
    # path('search/', views.search, name='search'),
    path('my_blog/', views.MyBlogView.as_view(), name='my_blog'),
    path('new_post/', views.new_post, name='new_post'),
    path('edit_post/<int:post_pk>', views.edit_post, name='edit_post'),
    path('new_cate/', views.new_cate, name="new_cate"),
    path('new_tag/', views.new_tag, name="new_tag"),
]



"""
    # 视图函数url规则
    path('', views.index, name='index'),
    path('posts/<int:pk>', views.detail, name='detail'),
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('categories/<int:pk>', views.category, name='category'),
    path('tags/<int:pk>', views.tag, name='tag'),
    path('archives_day/<int:year>/<int:month>/<int:day>', views.archive_day, name='archive_day'),
    path('author/<int:author>', views.author, name='author'),
"""