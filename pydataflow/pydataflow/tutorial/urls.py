from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf.urls import url, include

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
# router.register(r'prlogs', views.ProcesslogViewSet, basename='Processlog')


router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'plogdetail', views.ProcesslogDetailViewSet, basename='Processlog')

urlpatterns = router.urls

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

   url(r'plogdetail/(?P<process_id>[0-9]+)/$', views.ProcesslogDetailViewSet.as_view({'get': 'list'}), name='ProcesslogDetailViewSet'),

   url('processlogdetail/(?P<process_id>[0-9]+)/$', views.processlogdetail, name='processlogdetail'),

]

urlpatterns += router.urls


# url(r'purchases/(?P<process_id>[0-9]+)/$', views.ProcesslogViewSet.as_view({'get': 'list'}), name='ProcesslogViewSet'),



#url('^purchases/(?P<username>.+)/$', ProcesslogViewSet.as_view()),
# url('^purchases/', ProcesslogViewSet.as_view()),
#url(r'^purchases/', views.ProcesslogViewSet.as_view({'get': 'list'}), name='ProcesslogViewSet'),
