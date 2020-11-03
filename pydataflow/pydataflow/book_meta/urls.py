from django.conf.urls import include, url
# from django.conf.urls import patterns
from django.conf.urls import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

# from meta import views as meta_views
app_name = 'book_meta'

# # http://127.0.0.1:8000/accounts/password/reset/ not working

urlpatterns = [

    # url(r'^sp_detail2/(\d+)/$', views.sp_detail, name='sp_detail'),
    url(r'^sp_list/(\d+)/$', views.sp_list, name='sp_list'),
    # # url(r'^sp/$', views.sp_list, name='sp_list'),
    url(r'^sp/create/$', views.sp_create, name='sp_create'),
    url(r'^sp/(?P<pk>\d+)/update/$', views.sp_update, name='sp_update'),
    url(r'^sp/(?P<pk>\d+)/delete/$', views.sp_delete, name='sp_delete'),

    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^books/$', views.book_list, name='book_list'),
    url(r'^books/create/$', views.book_create, name='book_create'),
    url(r'^books/(?P<pk>\d+)/update/$', views.book_update, name='book_update'),
    url(r'^books/(?P<pk>\d+)/delete/$', views.book_delete, name='book_delete'),


]
