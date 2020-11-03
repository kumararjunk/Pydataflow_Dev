# from django.conf.urls import patterns, include, url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
from common import views as common_views
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login


from django.urls import path
from django.conf.urls import *
from . import views


urlpatterns = [


    ##to redirect to login page
    url(r'^admin/', admin.site.urls),
    url(r'^about_us/$', common_views.about_us, name='about_us'),
    url(r'^$', views.login_redirect, name='login_redirect'),
    url('update_domain/', common_views.update_domain, name='update_domain'),

    url(r'^profile_main_view/$', common_views.profile_main_view, name='profile_main_view'),
    url(r'^project_access_request/$', common_views.project_access_request, name='project_access_request'),
    url(r'^project_access_req_validate/$', common_views.project_access_req_validate, name='project_access_req_validate'),

    url(r'^my_project_access_status/$', views.my_project_access_status, name='my_project_access_status'),

    url(r'^project_access_status_detail/(?P<project_id>[0-9]+)/$', views.project_access_status_detail, name='project_access_status_detail'),
    url(r'^project_access_req_view/$', views.project_access_req_view, name='project_access_req_view'),
    url(r'^project_access_req_view_detail/(?P<project_id>[0-9]+)/$', views.project_access_req_view_detail, name='project_access_req_view_detail'),
    url(r'^project_access_status_update/(?P<project_id>[0-9]+)/(?P<access_id>[0-9]+)/(?P<is_approve>[0-9]+)/$', views.project_access_status_update, name='project_access_status_update'),


    # url(r'^project/(?P<filter_by>[a-zA_Z]+)/$', views.project_filter, name='project_filter'),
    # url(r'^project_list_view/$', views.current_project_list_view, name='project_list'),

]


    ###url(r'^project_access_status/(?P<project_id>[0-9]+)/$', views.project_access_status, name='project_access_status'),
    ### url(r'^project_access_view_update/(?P<project_id>[0-9]+)/$', views.Project_accessview_update.as_view(), name='Project_accessview_update'),

###
    ### url(r'^project_access_status/$', common_views.project_access_status, name='project_access_status'),

    #tested url above
    #### url(r'^profile_main_view/$', views.profile_main_view, name='profile_main_view'),

    ###url(r'^project_list_view1/$', views.current_project_list_view1, name='project_list1'),
