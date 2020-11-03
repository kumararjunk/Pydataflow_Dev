#!/usr/bin/python

import subprocess
import os.path
import os, sys, calendar, sqlite3, time, cx_Oracle
import os ,sys, logging, pathlib, argparse
import django
from sys import argv
from shutil import copyfile
# import MySQLdb
# from subprocess import Popen,PIPE
from django.conf import settings
from django.core.mail import send_mail
from collections import deque


p = subprocess.Popen('source /appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev/bin/activate', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    print(line)
retval = p.wait()


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render_to_response
from django.db.models import Q
from django.template import loader, RequestContext
from django.views import generic
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.http import request, HttpRequest, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib import messages
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin, FormView, CreateView, UpdateView, DeleteView
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView




os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pydataflow.settings")
project_path = os.path.join(os.path.abspath(os.path.dirname(__name__)))
print("project_path:", project_path)


project_path = project_path.replace("core", "")
print("project_path after replace", project_path)
# exit()

sys.path.append("/appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev/PyDataFlow/PyDataFlow/pydataflow")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pydataflow.settings")
sys.path.append(project_path)
django.setup()


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from meta.models import Project, Spname, Tbllist
from meta.views import *

os.chdir(project_path)


fake_request = HttpRequest()
fake_request.method = 'post'
fake_request.method = 'GET'
fake_request.user = 'K390239'
# fake_request.user = 'arjunkumar'

###creating the log files
curr_date = time.strftime("%Y-%m-%d")
job_execution_logfile = project_path + "logs/" + str(curr_date)


#create the log file to capture the job execution
def create_log_file(tmp_log_file_var):
    try:
        log_directory = os.path.dirname(tmp_log_file_var)
        # print("core.py create_log_file, log file path", log_directory)
        pathlib.Path(log_directory).mkdir(parents=True, exist_ok=True)
        os.remove(tmp_log_file_var)
    except OSError:
        tmp_log_file = open(tmp_log_file_var, 'w')
        tmp_log_file.write('job Log Details:' + "\n")
        tmp_log_file.close()


#
def execute_jobs(project_id=0, spname_id=0):
    spname_id = int(spname_id)
    print("Info:execute_jobs, project_id:", project_id, "spname_id:", spname_id)
    request=fake_request
    project = get_object_or_404(Project, pk=project_id)
    print("info:execute_jobs, project name:",project, "spname_id:", spname_id)

    backend_log = job_execution_logfile + "/" + str(project) + "/" + "backend_scheudler_all_report_name_backend_execution.log"
    print("All job execution summary:", backend_log)
    create_log_file(backend_log)

    if spname_id == 0:
        print("executing all the jobs in project:",project)
        exe_src_system_all(fake_request, project_id)

    else:
        spname_d = Spname.objects.get(pk=spname_id).__dict__
        report_name = spname_d['report_name']
        print("exectuting project",project, "report_name:",report_name)
        execute_tbllist(fake_request, project_id, spname_id)

    print("End of Execution")



project_id = argv[1]
spname_id = argv[2] #if len(sys.argv) >= 2 else 0



execute_jobs(project_id, spname_id)
