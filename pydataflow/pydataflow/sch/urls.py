from django.conf.urls import include, url

# from django.conf.urls import patterns,
# from django.conf.urls import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from django.urls import path

from sch import views
app_name = 'sch'

from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'schedule', views.ScheduleViewSet)


urlpatterns = [
    url('^admin/', admin.site.urls),
    url('^api/', include(router.urls)),

###main function to create the cron and update the table
    url(r'^sch_delete_cron/(?P<record_id>[0-9]+)/$', views.sch_delete_cron, name='sch_delete_cron'),

    # url(r'^project/(?P<project_id>[0-9]+)/(?P<jobflow_id>[0-9]+)/(?P<jobflowdetail_id>[0-9]+)/(?P<sch_type>[0-9]+)/sch_remove_cron/$', views.sch_remove_cron, name='sch_remove_cron'),

    url(r'^project/(?P<project_id>[0-9]+)/(?P<jobflow_id>[0-9]+)/(?P<jobflowdetail_id>[0-9]+)/(?P<sch_type>[0-9]+)/sch_create_cron/$', views.sch_create_cron, name='sch_create_cron'),

    # # #scheudling project
    url(r'^project/(?P<project_id>[0-9]+)/(?P<jobflow_id>[0-9]+)/(?P<jobflowdetail_id>[0-9]+)/(?P<sch_type>[0-9]+)/sch_wizard_generic/$', views.sch_wizard_generic, name='sch_wizard_generic'),
    #url(r'^project/(?P<project_id>[0-9]+)/(?P<jobflow_id>[0-9]+)/sch_main_view/$', views.sch_main_view, name='sch_main_view'),

    url(r'schedule', views.schedule, name='schedule'),


]




# "ajax": "/api/schedule/?format=datatables",
