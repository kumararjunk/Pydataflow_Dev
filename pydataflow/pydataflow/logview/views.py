from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import generics
from django.shortcuts import redirect
#import os
from django.conf import settings

#from django.http import HttpResponseRedirect
# from rest_framework import filters

from meta.models import Processlog
from django.shortcuts import render
from rest_framework.response import Response
from django.conf.urls import url, include
from django.contrib.auth.models import User

from rest_framework import routers, serializers, viewsets
from .serializers import JobflowSerializer, ProcesslogSerializer, DetaillogSerializer

from meta.models import Processlog, Jobflow, Jobflowdetail

# import psutil
import signal, os
from os import kill
import time

from itertools import chain


##log first page summary view
def processlog(request):
    return render(request, 'logview/process_logs.html')

def get_processlog_options():
    return "options", {

        "jobflow": [{'label': obj.jobflowname, 'value': obj.pk} for obj in Jobflow.objects.all()],
        "jobflowdetail": [{'label': obj.project_job_name, 'value': obj.pk} for obj in Jobflowdetail.objects.all()]
    }

class ProcesslogViewSet(viewsets.ModelViewSet):
    queryset = Processlog.objects.filter(job_type="Job Flow").order_by('id').reverse()
    serializer_class = ProcesslogSerializer

    def get_options(self):
        return get_processlog_options()

    class Meta:
        datatables_extra_json = ('get_options', )


##log second page job log  view

def detaillog(request, process_id):
    return render(request, 'logview/process_detail_logs.html', {'process_id': process_id })

class DetaillogViewSet(viewsets.ModelViewSet):
   # queryset = Processlog.objects.all()
   serializer_class = DetaillogSerializer

   def get_queryset(self):
    process_id = self.kwargs['process_id']
    return Processlog.objects.filter(process_id=process_id).exclude(job_name='Job Flow').order_by('id')#.reverse()

def check_pid_status(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True




##log 3rd page jobdetailed log


# def log_detail(request, record_id):
#     encoding = 'utf-8'
#     # file_check = 0
#     file_check = Processlog.objects.filter(id = record_id).values()[0]['logfile']
#     print('log_detail file name:', file_check)

#     if not file_check:
#         error_message = 'Logfile Not Found'
#         return JsonResponse({'Error Message': error_message})

#     else:
#         logfile = Processlog.objects.filter(id = record_id).values()[0]['logfile']
#         tmp_logfile = logfile + '_tmp'

#         clean_log_file = open(tmp_logfile, "w")

#         with open(logfile, "rb") as handle:
#             for line in handle:
#                 if b'\x01' in line:
#                     continue
#                 clean_log_file.write(str(line, encoding))
#         clean_log_file.close()

#         f = open(tmp_logfile, 'r')
#         file_content = f.read()
#         f.close()
#         # return HttpResponse(file_content, content_type="text/plain")
#         # return render(request, 'logview/tmp.html',
#         return render(request, 'logview/process_detail_detail_logs.html',
#                         {'file_content': file_content},
#                         # context_instance=RequestContext(request)
#                         )


# from prod

def log_detail(request, record_id):
    encoding = 'utf-8'
    # file_check = 0
    file_check = Processlog.objects.filter(id = record_id).values()[0]['logfile']
    print('log_detail file name:', file_check)

    if not file_check:
        error_message = 'Logfile Not Found'
        return JsonResponse({'Error Message': error_message})

    else:
        logfile = Processlog.objects.filter(id = record_id).values()[0]['logfile']
        tmp_logfile = logfile + '_tmp'

        clean_log_file = open(tmp_logfile, "w")

        with open(logfile, "rb") as handle:
            for line in handle:
                if b'\x01' in line:
                    continue
                clean_log_file.write(str(line, encoding))
        clean_log_file.close()

        f = open(tmp_logfile, 'r')
        file_content = f.read()
        f.close()
        # return HttpResponse(file_content, content_type="text/plain")
        # return render(request, 'logview/tmp.html',
        return render(request, 'logview/azkaban_tmp.html',
                        {'file_content': file_content},
                        # context_instance=RequestContext(request)
                        )









def kill_util(pid):
    print('kill_util pid:', pid)
    if pid != 0:
        if check_pid_status(pid):
            os.kill(pid, signal.SIGTERM) #or signal.SIGKILL
            print('Process exist and trying to kill it')

    return True

def kill_process(request, process_id, record_id, pid):
    pid, process_id = int(pid), int(process_id)
    processlog_id_list = Processlog.objects.filter(process_id = process_id).filter(status='Executing').order_by('id').values_list('id', flat=True).distinct()[::1]
    process_log_job_type = Processlog.objects.get(pk=record_id)

    if process_log_job_type.job_name == 'Job Flow':
        jobflow = Jobflow.objects.get(id=process_log_job_type.jobflowname_id)
        print('Trying to kill Job Flow:', jobflow.jobflowname)

        processlog_id_list = Processlog.objects.filter(process_id = process_id).filter(status='Executing').order_by('id').values_list('id', flat=True).distinct()[::1]
        for id in processlog_id_list:
            p = Processlog.objects.get(pk=id)
            pid = p.pid
            print('job flow each job id:', pid)
            kill_util(pid)
            p.status = 'Killed'
            p.pid = 0
            p.save()
        return redirect('logview:processlog')

    else:
        kill_util(pid)
        p = Processlog.objects.get(pk=record_id)
        p.status = 'Killed'
        p.pid = 0
        p.save()
        processlog_jobflow_id = Processlog.objects.filter(process_id = process_id).filter(job_name='Job Flow').values_list('id', flat=True).distinct()[::1]
        for jobflow_id in processlog_jobflow_id:
            p = Processlog.objects.get(pk=jobflow_id)
            p.status = 'Killed'
            p.pid = 0
            p.save()

    return redirect('logview:process_detail', process_id=process_id)
    #return render(request, 'process_logs/process_detail_logs.html', {'process_id': process_id })


###### kill with psutil
# def kill_util(pid):
#     if psutil.pid_exists(pid):
#         print('Trying to kill the process pid:', pid)
#         parent = psutil.Process(pid)

#         for child in parent.children(recursive=True):
#             print('child pid', child)
#             child.kill()
#             os.kill(pid, signal.SIGTERM)
#     time.sleep(.25)
#     return True

