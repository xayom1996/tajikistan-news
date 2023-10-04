"""hhtest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url, include
from django.urls import include, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from insta import views
from insta.views import Create, VideoCreate, CreateOctagon, news, quote
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', Create.as_view(), name='home'),
    re_path(r'news', news, name='news'),
    re_path(r'^octagon/$', CreateOctagon.as_view(), name='octagon'),
    re_path(r'^quote/$', quote, name='quote'),
    re_path(r'^octagon/newoctagon/$', views.newoctagon, name='newoctagon'),
    re_path(r'^newpost/$', views.newpost, name='newpost'),
    re_path(r'^video/$', VideoCreate.as_view(), name='video'),
    re_path(r'^newvideo/$', views.newvideo, name='newvideo'),
    re_path(r'^api/', include(router.urls)),
    re_path(r'^api/v1/posts/$', views.post_collection),
    # url(r'^api/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
