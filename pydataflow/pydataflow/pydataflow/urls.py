"""etl_control URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
# from django.conf.urls import url
from django.views.generic import RedirectView

from common import views as common_views

# from meta import views as meta_views

# kill $(ps -ef | grep 8080| awk '{print $2}')

urlpatterns = [

    # url(r'^music/', include('music.urls')),
    # url(r'^', include('music.urls')),
    # url(r'^music/', include('music.urls', namespace='music')),

    #allauth urls
    url('^', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('allauth.urls')),

    path('admin/', admin.site.urls),

    # url(r'^$', common_views.home, name='home'),
    url(r'^', include('common.urls')),
    # url(r'^$', common_views.login_user, name='login_user'),
    url(r'^common/', include(('common.urls', 'common'), namespace='common')),

    url(r'^', include('scripts.urls')),
    url(r'^scripts/', include('scripts.urls')),


    url(r'^', include('books.urls')),
    url(r'^books/', include('books.urls')),

    url(r'^', include('meta.urls')),
    url(r'^meta/', include('meta.urls')),

    url(r'^', include('book_meta.urls')),
    url(r'^book_meta/', include('book_meta.urls')),


    url(r'^', include('logview.urls')),
    url(r'^logview/', include('logview.urls')),

    # url(r'^', include('logview2.urls')),
    # url(r'^logview2/', include('logview2.urls')),


    # url(r"^meta/", include("meta.urls", namespace="meta")), #required for profile/family

    # url(r"^metadata/", include("metadata.urls", namespace="metadata")), #required for new metadata
    # url(r'^metadata/', include('metadata.urls')),
    # url(r'^', include('metadata.urls')),

    url(r'^sch/', include('sch.urls')),
    url(r'^', include('sch.urls')),
    url(r'^sch/', include('sch.urls', namespace='sch')),

    # url(r'^', include('common.urls')),
    # url(r'^music/', include('music.urls')),
    # url(r'^', include('music.urls')),
    # url(r'^music/', include('music.urls', namespace='music')),

    # path('', RedirectView.as_view(pattern_name='person_changelist'), name='hr'),
    # path('hr/', include('hr.urls')),


    # url(r'^tutorial/', include('tutorial.urls')),
    # url(r'^', include('tutorial.urls')),



]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
