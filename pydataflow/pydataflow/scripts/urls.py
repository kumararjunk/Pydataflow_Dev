from django.conf.urls import include, url
# from django.conf.urls import patterns
from django.conf.urls import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

# from meta import views as meta_views
app_name = 'scripts'

# # http://127.0.0.1:8000/accounts/password/reset/ not working

urlpatterns = [



    url(r'^select_obj/(?P<jobflow_id>[0-9]+)/$', views.select_obj, name='select_obj'),

    url(r'^select_obj_type/(?P<jobflow_id>[0-9]+)/$', views.select_obj_type, name='select_obj_type'),

    #url(r'^jobflowdetailupd/(?P<jobflow_id>[0-9]+)/$', views.jobflowdetailupd.as_view(), name='jobflowdetailupd'),
    url(r'^jobflowdetailupdate/(?P<jobflow_id>[0-9]+)/(?P<jobflowdetail_id>[0-9]+)/$', views.jobflowdetailUpdate.as_view(), name='jobflowdetailUpdate'),


    url(r'^jobflowdetail/(?P<jobflow_id>[0-9]+)/$', views.jobflowdetail_detail, name='jobflowdetail'),

    #jobflow
    url(r'^del_jobflow/(?P<jobflow_id>[0-9]+)/$', views.jobflow_delete, name='del_jobflow'),
    url(r'^jobflow_upd/(?P<jobflow_id>[0-9]+)/$', views.JobflowUpdate.as_view(), name='jobflow_update'),

    url(r'^create_jobflow/(?P<project_id>[0-9]+)/$', views.create_jobflow, name='create_jobflow'),
    url(r'^jobflow_index/(?P<project_id>[0-9]+)/$', views.jobflow_index, name='jobflow_index'),

 # script  4 urls # # #     # delete main view     # Spname  spname_id


    #url(r'^exe_single_script/(?P<jobflow_id>[0-9]+)/(?P<jobflowdetail_id>[0-9]+)/$', views.exe_single_script, name='exe_single_script'),
    #url(r'^jobflowdetailupdate/(?P<jobflow_id>[0-9]+)/(?P<jobflowdetail_id>[0-9]+)/$', views.jobflowdetailUpdate.as_view(), name='jobflowdetailUpdate'),


    url(r'^del_script/(?P<project_id>[0-9]+)/del_sp/(?P<script_id>[0-9]+)/$', views.del_script, name='del_script'),
    url(r'^del_script_view/(?P<project_id>[0-9]+)/del_script_view/$', views.del_script_view, name='del_script_view'),

    # # reverse url to detail page
    url(r'^scripts_upd/(?P<project_id>[0-9]+)/(?P<script_id>[0-9]+)/$', views.scriptupdate.as_view(), name='scripts_upd'),
    url(r'^scripts_add/(?P<project_id>[0-9]+)/$', views.scripts_add, name='scripts_add'),
    url(r'^scripts_detail/(\d+)/$', views.scripts_detail, name='scripts_detail'),

]
