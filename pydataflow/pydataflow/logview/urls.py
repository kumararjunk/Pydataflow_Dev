from django.contrib import admin
from django.conf.urls import url, include

from django.urls import include, path
from rest_framework import routers

from logview import views
app_name = 'logview'

router = routers.DefaultRouter()
router.register(r'processlog', views.ProcesslogViewSet)
router.register(r'detaillog', views.DetaillogViewSet, basename='Processlog')

urlpatterns = [
    url('^admin/', admin.site.urls),
    url('^api/', include(router.urls)),
    url('processlog', views.processlog, name='processlog'),

    url('detaillog/(?P<process_id>[0-9]+)/$', views.DetaillogViewSet.as_view({'get': 'list'})),
    url('process_detail/(?P<process_id>[0-9]+)/$', views.detaillog, name='process_detail'),


    url(r'^log_detail/(?P<record_id>[0-9]+)/$', views.log_detail, name='log_detail'),
    url(r'^kill_process/(?P<process_id>[0-9]+)/(?P<record_id>[0-9]+)/(?P<pid>[0-9]+)/$', views.kill_process, name='kill_process'),

]

        # url('detaillog/(?P<process_id>[0-9]+)/$', views.DetaillogViewSet, name='detaillog'),

    # url('detaillog/$', views.DetaillogViewSet.as_view({'get': 'list'}), name='detaillog'),
    #url('^detaillog/(?P<process_id>[0-9]+)/$', views.DetaillogViewSet.as_view({'get': 'list'})),


    # url('tmp/(?P<process_id>[0-9]+)/$', views.detaillog, name='tmp'),

    # url('detaillog/(?P<process_id>[0-9]+)/$', views.DetaillogViewSet.as_view({'get': 'list'}), name='detaillog'),
    # url('detaillog/(?P<process_id>[0-9]+)/$', views.DetaillogViewSet.as_view(), name='detaillog'),
    # url('tmp/(?P<process_id>[0-9]+)/$', views.DetaillogViewSet.as_view({'get': 'list'}), name='tmp'),

