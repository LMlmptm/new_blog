from blog import views
from django.urls import path,re_path
from django.conf.urls import url,include
from django.views.generic.base import RedirectView

urlpatterns = [
   re_path(r'^$',views.index,name='index'),#博客首页
   re_path(r'^(?P<blog_id>[0-9]+)$',views.detail,name='detail'),#每一页博客
   re_path(r'^category/(?P<category_id>[0-9]+)$',views.category,name='category'),#分类博客
   re_path(r'^tag/(?P<tag_id>[0-9]+)$',views.tag,name='tag'),#标签博客
   re_path(r'^search/$',views.search,name='search'),#搜索博客
   re_path(r'^archives/(?P<year>[0-9]+)/(?P<month>[0-9]+)$',views.archives,name='archives'),#博客归档
   re_path(r'^login$',views.login,name='login'),#登陆
   re_path(r'^register/$',views.register,name='register'),#注册
   re_path(r'^register_handle$',views.register_handle,name='register_handle'),#注册验证
   re_path(r'^login_active$',views.login_active,name='login_active'),#登陆验证
   re_path(r'^active/(?P<token>.*)$', views.Active, name='active'),  # 用户激活
   re_path(r'^logout$',views.Logout,name='logout'),#退出登陆
   re_path(r'^reply/(?P<comment_id>\d+)/$', views.reply, name='comment_reply'),#评论
   re_path(r'^myblog$',views.My_blog,name='myblog'),#我的博客
   re_path(r'^favicon\.ico$',RedirectView.as_view(url=r'static/blog/images/favicon.ico')),#小图标
   re_path(r'^myimages$',views.myimages,name='myimages'),#我的图片
   re_path(r'^update/$',views.register_form,name='update'),#注册
   re_path(r'^download/(?P<file_id>[0-9]+)$',views.File_Download,name='download'),#文件下载
   re_path(r'^file/$',views.File_Show,name='fileShow')#文件列表
]
