from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer




from meta.models import Processlog
from .serializers import ProcesslogdetailSerializer
from rest_framework import generics
from rest_framework import routers, serializers, viewsets
from django.shortcuts import render



def processlogdetail(request, process_id):
    return render(request, 'process_logs/process_logs_detail_test.html')

# def processlogdetail(request, process_id):
#     print('*'*100)
#     print('processlogdetail', 'process_id:', process_id)
#     return render(request, 'process_logs/process_logs_detail.html')

class ProcesslogDetailViewSet(viewsets.ModelViewSet):
    serializer_class = ProcesslogdetailSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Processlog.objects.all()
        #queryset = Processlog.objects.all().order_by('id').reverse()
        print('*'*100)
        queryset = queryset.filter(process_id=74)
        return queryset



    # def get_queryset(self, *args, **kwargs):
    #     queryset = Processlog.objects.all()
    #     print('*='*100)
    #     # print('ProcesslogViewSet:', self.kwargs, type(self.kwargs), self.args, type(self.args))
    #     pk = int(self.kwargs['pk'])
    #     process_id = Processlog.objects.filter(id = pk).values()[0]['process_id']
    #     print('process_id:', process_id, type(process_id))

    #     queryset = Processlog.objects.filter(process_id=process_id)

    #     # if process_id >= 0:
    #     #     queryset = Processlog.objects.filter(process_id=process_id)
    #     # print('queryset', queryset)

    #     return queryset

    # def get_queryset(self, *args, **kwargs):
    #     queryset = Processlog.objects.all()
    #     print('123 queryset', queryset)
    #     return queryset
        #return self.queryset.filter(airline_id=self.request.GET.get('airline_pk'))



# class ProcesslogDetailViewSet(viewsets.ModelViewSet):
#     serializer_class = ProcesslogdetailSerializer

#     def get_queryset(self, *args, **kwargs):
#         # queryset = Processlog.objects.all()
#         queryset = Processlog.objects.all().order_by('id').reverse()
        # print('queryset:', queryset)
        # print('self.kwargs', self.kwargs, self.request)
        # pk = int(self.kwargs['pk'])
        # print('pk', pk, type(pk))
        # process_id = Processlog.objects.filter(id = pk).values()[0]['process_id']
        # print('process_id', process_id, type(process_id))

        #queryset = self.queryset.filter(processlog_id=self.request.GET.get('processlog_pk'))
        #queryset = self.queryset.filter(process_id=process_id)
        # print('*'*100)
        # queryset = queryset.filter(process_id=74)
        # print('queryset 123:', queryset)
        # return queryset



    # def get_queryset(self, *args, **kwargs):
    #     queryset = Processlog.objects.all()
    #     print('*='*100)
    #     # print('ProcesslogViewSet:', self.kwargs, type(self.kwargs), self.args, type(self.args))
    #     pk = int(self.kwargs['pk'])
    #     process_id = Processlog.objects.filter(id = pk).values()[0]['process_id']
    #     print('process_id:', process_id, type(process_id))

    #     queryset = Processlog.objects.filter(process_id=process_id)

    #     # if process_id >= 0:
    #     #     queryset = Processlog.objects.filter(process_id=process_id)
    #     # print('queryset', queryset)

    #     return queryset

    # def get_queryset(self, *args, **kwargs):
    #     queryset = Processlog.objects.all()
    #     print('123 queryset', queryset)
    #     return queryset
        #return self.queryset.filter(airline_id=self.request.GET.get('airline_pk'))


# class ProcesslogDetailViewSet(viewsets.ModelViewSet):
#     serializer_class = ProcesslogdetailSerializer
#     # def get_queryset(self):
#     def get_queryset(self, *args, **kwargs):
#         queryset = Processlog.objects.all()
#         print('*='*100)
#         # print('ProcesslogViewSet:', self.kwargs, type(self.kwargs), self.args, type(self.args))
#         pk = int(self.kwargs['pk'])
#         process_id = Processlog.objects.filter(id = pk).values()[0]['process_id']
#         print('process_id:', process_id, type(process_id))

#         queryset = Processlog.objects.filter(process_id=process_id)

#         # if process_id >= 0:
#         #     queryset = Processlog.objects.filter(process_id=process_id)
#         # print('queryset', queryset)

#         return queryset
