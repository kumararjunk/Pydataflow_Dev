from django.conf.urls import include, url
# from django.conf.urls import patterns
from django.conf.urls import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

from django.contrib import admin
from rest_framework import routers
from meta import views

router = routers.DefaultRouter()

router.register(r'projecjobflowdetailtobjects',
                views.ProjectJobflowdetailViewSet)
router.register(r'projecspnameobjects', views.ProjectSpnameViewSet)

# router.register(r'processlog', views.ProcesslogViewSet)
# router.register(r'detaillog', views.DetaillogViewSet, basename='Processlog')


# router.register(r'projecthistorytobjects', views.ProjectHistorylViewSet)

# from meta import views as meta_views
app_name = 'meta'

# # http://127.0.0.1:8000/accounts/password/reset/ not working

urlpatterns = [
    # url('project_history', views.project_history, name='project_history'),
    # url('projecthistorytobjects', views.projecthistorytobjects, name='projecthistorytobjects'),

    # url(r'^test/$', views.test, name='test'),


    url('^admin/', admin.site.urls),
    url('^api/', include(router.urls)),

    url('advance_search', views.advance_search, name='advance_search'),
    url('projecjobflowdetailtobjects', views.projecjobflowdetailtobjects,
        name='projecjobflowdetailtobjects'),
    url('projecspnameobjects', views.projecspnameobjects,
        name='projecspnameobjects'),


    # exe_jobflow_restart:
    url(r'^exe_jobflow_rerun/(?P<process_id>[0-9]+)/(?P<record_id>[0-9]+)/$',
        views.exe_jobflow_rerun, name='rerun'),

    # execute all the jobflow in the project:
    url(r'^exe_jobflow/(?P<project_id>[0-9]+)/(?P<jobflow_id>[0-9]+)/$',
        views.exe_jobflow, name='exe_jobflow'),

    # exe_single_jobs_generic --> exe_jobs
    url(r'^exe_jobs/(?P<project_id>[0-9]+)/(?P<jobflow_id>[0-9]+)/(?P<jobflowdetail_id>[0-9]+)/$',
        views.exe_jobs, name='exe_jobs'),



    # choose dsn and imp_object_view and delete tables
    url(r'^meta/(?P<project_id>[0-9]+)/select_src_tables/$',
        views.select_src_tables, name='select_src_tables'),
    url(r'^project/(?P<project_id>[0-9]+)/select_dsn/$',
        views.select_dsn, name='select_dsn'),
    url(r'^project/(?P<project_id>[0-9]+)/DsnTest/$',
        views.DsnTest, name='DsnTest'),

    # # # ###import & export from exported objects tables view 4 views
    url(r'^imp_sp/(?P<project_id>[0-9]+)/imp_sp/$',
        views.imp_sp, name='imp_sp'),
    url(r'^imp_sp_view/(?P<project_id>[0-9]+)/imp_sp_view/$',
        views.imp_sp_view, name='imp_sp_view'),
    url(r'^exp_sp/(?P<project_id>[0-9]+)/exp_sp/(?P<spname_id>[0-9]+)/$',
        views.exp_sp, name='exp_sp'),
    url(r'^exp_sp_view/(?P<project_id>[0-9]+)/exp_sp_view/$',
        views.exp_sp_view, name='exp_sp_view'),

    # Datasource 2 urls
    url(r'^del_dsn/(?P<project_id>[0-9]+)/(?P<datasource_id>[0-9]+)/$',
        views.del_dsn, name='del_dsn'),
    url(r'^del_dsn_view/(?P<project_id>[0-9]+)/$',
        views.del_dsn_view, name='del_dsn_view'),

    url(r'^dsn_bulk_upd/(?P<project_id>[0-9]+)/dsn_bulk_upd/$',
        views.DsnBulkUpdate.as_view(), name='dsn_bulk_update'),
    url(r'^dsn_upd/(?P<datasource_id>[0-9]+)/$',
        views.DsnUpdate.as_view(), name='dsn-update'),
    url(r'^dsn_add/(?P<project_id>[0-9]+)/$', views.dsn_add, name='dsn_add'),
    url(r'^dsn_view/(?P<project_id>[0-9]+)/dsn_view/$',
        views.DsnView, name='dsn_view'),

    # table  4 urls # # #     # delete main view     # Spname  spname_id
    url(r'^del_sp/(?P<project_id>[0-9]+)/del_sp/(?P<spname_id>[0-9]+)/$',
        views.del_sp, name='del_sp'),
    url(r'^del_sp_view/(?P<project_id>[0-9]+)/del_sp_view/$',
        views.del_sp_view, name='del_sp_view'),

    # sp bulk update####ProjectDataSourceUpdated # #     # ProjectSPBulkUpdated
    url(r'^sp_bulk_upd/(?P<project_id>[0-9]+)/$',
        views.ProjectSPBulkUpdated.as_view(), name='project-spbulk-update'),
    # reverse url to detail page
    url(r'^sp_upd/(?P<spname_id>[0-9]+)/$',
        views.SpUpdate.as_view(), name='sp_upd'),

    url(r'^sp_add/(?P<project_id>[0-9]+)/$', views.sp_add, name='sp_add'),
    url(r'^sp_detail/(\d+)/$', views.sp_detail, name='sp_detail'),

    # Projectenv variable update
    url(r'env_variables_project/(?P<project_id>[0-9]+)/$',
        views.ProjectEnvUpdated.as_view(), name='project-env-update'),

    #     ##project 3 urls
    url(r'^project_del/(?P<project_id>[0-9]+)/$',
        views.project_delete, name='project_delete'),
    url(r'^project_upd/(?P<pk>[0-9]+)/$',
        views.ProjectUpdate.as_view(), name='project_update'),
    url(r'^project_create/$', views.project_create, name='project_create'),

    url(r'^index/$', views.index, name='index'),
]


# exe_sp_util


# execute all sp
# url(r'^exe_sp_all/(?P<project_id>[0-9]+)/$', views.exe_sp_all, name='exe_sp_all'),

# get sp status
# url(r'^sp_exec_status/(?P<project_id>[0-9]+)/$', views.sp_exec_status, name='sp_exec_status'),


###url(r'^project/(?P<jobflowdetail_id>[0-9]+)/(?P<process_id>[0-9]+)/processlog_update/$', views.processlog_update, name='processlog_update'),
####url(r'^project/processlog_update/$', views.processlog_update, name='processlog_update'),
#url(r'^project/(?P<jobflowdetail_id>[0-9]+)/processlog_create/$', views.processlog_create, name='processlog_create'),
#### url(r'^project/processlog_test/$', views.processlog_test, name='processlog_test'),


# can be deleated below url
# url(r'^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
# url(r'^project/(?P<datasource_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),


# url(r'^project/(?P<project_id>[0-9]+)/select_dsn/$', views.select_dsn, name='select_dsn'),
# url(r'^project/(?P<project_id>[0-9]+)/select_dsn1/$', views.select_dsn1, name='select_dsn1')
# url(r'^profile_setting1/(?P<project_id>[0-9]+)/profile_setting1/$', views.profile_setting1, name='profile_setting1'),

# url(r'^index1/$', views.index1, name='index1'),
# path('person/json/', views.person_json, name='person_json'),
# path('person/json2/', views.person_json2, name='person_json2'),

# url(r'^person/json2/(\d+)/$', views.person_json2, name='person_json2'),


# path('person_filter_json/json2/(?P<id>[0-9]+)/$', views.person_filter_json, name='person_filter_json'),
#path(r'^person_filter_json/json/(?P<id>[0-9]+)/$', views.person_filter_json, name='person_filter_json'),

# url(r'^table_detail2/(\d+)/$', views.table_detail2, name='table_detail2'),

# url(r'^table_detail/(\d+)/$', views.table_detail, name='table_detail'),
