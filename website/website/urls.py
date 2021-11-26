"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,re_path
from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from blog.feed import LatestEntriesFeed
from blog import views as vw
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from blog.models import Entry
from blog.views import register_handle
info_dict={
    'queryset':Entry.objects.all(),
    'date_field':'modified_time',
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/',include('tinymce.urls')),
    path('latest/feed/',LatestEntriesFeed()),
    # path('login/',include('blog.urls','blog'),namespace='login'),
    # path('register/',include('blog.urls','blog'),namespace='register'),
    path('comments/',include('django_comments.urls')),
    path('',include(('blog.urls','blog'),namespace='blog')),
    path(r'sitemap/.xml',sitemap,{'sitemaps':{'blog':GenericSitemap(info_dict=info_dict,priority=0.6)}}),#站点目录

]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
#static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

handler404=vw.Not_page_found_404
handler403=vw.Not_page_found_403
handler500=vw.Page_error_500

