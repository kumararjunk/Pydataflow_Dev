#!/usr/bin/python

import os.path, logging, pathlib, argparse
import django
import subprocess, os, sys, calendar, sqlite3, time, cx_Oracle
from sys import argv
from shutil import copyfile
from django.conf import settings
from django.core.mail import send_mail
from collections import deque
from django.http import request, HttpRequest, HttpResponse, HttpResponseRedirect
import os, getpass
#getting the local environment path
project_path = os.path.join(os.path.abspath(os.path.dirname(__name__)))
#print("project_path:", project_path)

#getting the core path
project_path = project_path.replace("core", "")
#print("project_path after replace", project_path)

sys.path.append(project_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pydataflow.settings")
# sys.path.append(project_path)
django.setup()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.shortcuts import get_object_or_404

from django.db import models
from meta.models import Project, DataSource, Spname, Tbllist, InitialTbllist
from meta.models import Jobflow, Jobflowdetail, Script, Processlog
from django.db.models import Max
# from django.forms.models import model_to_dict


# import threading
import multiprocessing
from multiprocessing import Process, Queue, Pipe
#import MySQLdb, sqlite3, csv, time


# from meta.views import *
# from meta.utils import *
from scripts.views import worker_process_cron

#from scripts.utils import *
# import MySQLdb
# from subprocess import Popen,PIPE

#changing the direcorty to project path:
os.chdir(project_path)


##setting fake request
fake_request = HttpRequest()
fake_request.method = 'post'
fake_request.method = 'GET'
fake_request.user = getpass.getuser()
#fake_request.user = 'K390239'
# fake_request.user = 'arjunkumar'

###creating the log files
curr_date = time.strftime("%Y-%m-%d")
# curr_timestamp = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
job_execution_logfile = project_path + "logs/" + str(curr_date) + "/"

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


def log_subprocess_debug(log_file, user):

    class ContextFilter(logging.Filter):

        def filter(self, record):
            record.user = user
            return True

    logger = logging.getLogger(__name__)
    logger.addFilter(ContextFilter())
    logger.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    formatter = logging.Formatter('%(asctime)s - %(user)s - %(levelname)s -%(name)s - %(message)s')
    #log_file = '/Users/arjunkumar/Desktop/notes2/pre-prod/front_end/PyDataFlow_dev2/PyDataFlow/pydataflow/logs/2019-09-25/mlab_adhoc/tmp.txt'
    file_handler = logging.FileHandler(log_file, 'a')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger



def log_subprocess_exception(log_file, user):

    class ContextFilter(logging.Filter):

        def filter(self, record):
            record.user = user
            return True

    logger = logging.getLogger(__name__)
    logger.addFilter(ContextFilter())
    logger.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    formatter = logging.Formatter('%(asctime)s - %(user)s - %(levelname)s -%(name)s - %(message)s')
    #log_file = '/Users/arjunkumar/Desktop/notes2/pre-prod/front_end/PyDataFlow_dev2/PyDataFlow/pydataflow/logs/2019-09-25/mlab_adhoc/tmp.txt'
    file_handler = logging.FileHandler(log_file, 'a')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

    # for line in iter(pipe.readline, b''):
    #     logger.debug(line)




# def update_processlog_util(job_status, jobflowdetail_id, process_id, log_type, log_file):
#   print("meta:util:update_processlog_util", 'job_status:', job_status, 'jobflowdetail_id:', jobflowdetail_id,\
#     'process_id:', process_id, 'log_type:', log_type)

#   jobflowdetail_d = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__
#   #jobflowname = jobflowdetail_d['id']
#   jobflowname_id = jobflowdetail_d['jobflowname_id']
#   project_job_name = jobflowdetail_d['project_job_name']
#   job_name = jobflowdetail_d['job_name']
#   job_type = jobflowdetail_d['job_type']
#   object_id = jobflowdetail_d['object_id']

#   jobflow_id_obj = Jobflow.objects.get(id=jobflowname_id)
#   jobflowdetail_id_obj = Jobflowdetail.objects.get(id=jobflowdetail_id)

#   if log_type == 'All Jobs':
#     processlog_id = Processlog.objects.filter(process_id = process_id).filter(jobflowname=jobflow_id_obj)\
#     .filter(project_job_name = 'All Jobs').values()[0]['id']
#     p = Processlog.objects.get(pk=processlog_id)
#     p.status = job_status
#     p.save()
#     print('meta:util:update_processlog_util, All Jobs, process_id:', process_id, 'jobflow_id_obj:', jobflow_id_obj, 'processlog_id:', processlog_id)

#   else:
#     print('update_processlog_util updating individual jobs: object_id', object_id)
#     processlog_id = Processlog.objects.filter(process_id = process_id).filter(jobflowname=jobflow_id_obj)\
#     .filter(jobflowdetail=jobflowdetail_id_obj).filter(project_job_name = project_job_name) \
#     .filter(job_name = job_name).filter(job_type = job_type).filter(object_id = object_id).values()[0]['id']
#     p = Processlog.objects.get(pk=processlog_id)
#     p.status = job_status
#     p.logfile = log_file
#     p.save()
#   return True



# def update_flow_status(current_process_id, jobflowdetail_id):
#     #updating the status of job stream.
#     log_type = 'All Jobs'
#     if Processlog.objects.filter(process_id = current_process_id).filter(status='Fail').exists():
#         job_status = 'Fail'
#         update_processlog_util(job_status, jobflowdetail_id, current_process_id, log_type, log_file='')
#     else:
#         job_status = 'Success'
#         update_processlog_util(job_status, jobflowdetail_id, current_process_id, log_type, log_file='')






def cron_exe_jobs(request, project_id, jobflow_id, jobflowdetail_id, cron_log):
    user = request.user
    logger = log_subprocess_debug(cron_log, user)

    # threads = []
    exec_parallel_ind = {"ind": True}
    template_name = 'scripts/jobflow_detail.html'
    jobflowdetail_d = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__
    user = request.user
    jobflow = get_object_or_404(Jobflow, pk=jobflow_id)
    project = get_object_or_404(Project, pk=project_id)
    project_d = project.__dict__
    jobflow_d = Jobflow.objects.get(pk=jobflow_id).__dict__

    if project_d['is_active'] != 'Y': #checking if the project is active
        error_message = 'Project:' + project_d['project_name'] + ' is Not Active'
        logger.exception(error_message)
        #print(error_message)
        # messages.info(request, error_message)
        # return render(request, template_name, {'project': project, 'jobflow': jobflow, 'user': user })

    if jobflow_d['is_active'] != 'Y': #checking if the jobflow is active
        error_message = 'Jobflow:' + jobflow_d['jobflowname'] + ' is Not Active'
        logger.exception(error_message)
        #print(error_message)
        # messages.info(request, error_message)
        # return render(request, template_name, {'project': project, 'jobflow': jobflow, 'user': user })

    if jobflowdetail_d['is_active'] != 'Y': #checking if the jobdetail is active
        error_message = 'Job Name:' + jobflowdetail_d['job_name'] + ' is Not Active'
        logger.exception(error_message)
        #print(error_message)
        # messages.info(request, error_message)
        # return render(request, template_name, {'project': project, 'jobflow': jobflow, 'user': user })

    object_id = jobflowdetail_d['object_id']
    job_type = jobflowdetail_d['job_type']

    if job_type == 'Stored_Proc':
        spname_d = Spname.objects.get(pk=object_id).__dict__

        if spname_d['is_active'] != 'Y':
            error_message = 'Stored Proc Name:' + spname_d['report_name'] + ' is Not Active, Please check SP Details page'
            logger.exception(error_message)
            # messages.info(request, error_message)
            # return render(request, template_name, {'project': project, 'jobflow': jobflow, 'user': user })

    if job_type == 'Shell_Script':
        script_d = Script.objects.get(pk=object_id).__dict__

        if script_d['is_active'] != 'Y':
            error_message = 'Script Name:' + script_d['job_name'] + ' is Not Active, Please check Shell Scripts page'
            logger.exception(error_message)
            # messages.info(request, error_message)
            # return render(request, template_name, {'project': project, 'jobflow': jobflow, 'user': user })

    if job_type == 'Table':
        table_d = Tbllist.objects.get(pk=object_id).__dict__

        if table_d['is_active'] != 'Y':
            error_message = 'meta:exe_jobs: executing Table'
            logger.exception(error_message)
            # print('meta:exe_jobs: executing Table')
            # print("Executing Table:", job_type, id)
            # return render(request, template_name, {'project': project, 'jobflow': jobflow, 'user': user })

    current_process_id = processlog_create_jobflow_util(jobflowdetail_id)
    worker_proces = multiprocessing.Process(target=worker_process_cron, args=(user, current_process_id, job_type, jobflowdetail_id, object_id, project_d))
    # threads.append(new_process)
    # new_process.daemon = True
    worker_proces.start()

    error_message = 'Job Submited, Process id:' + str(current_process_id)
    logger.debug(error_message)

    # messages.info(request, error_message)
    #return render(request, template_name, {'project': project, 'jobflow': jobflow, 'user': user })

def execute_job_cron(project_id=0, jobflow_id=0, jobflowdetail_id=0, sch_type=0):
    project_id = int(project_id)
    jobflow_id = int(jobflow_id)
    jobflowdetail_id = int(jobflowdetail_id)
    sch_type = int(sch_type)

    request=fake_request
    project = get_object_or_404(Project, pk=project_id)
    user = request.user

    curr_date = time.strftime("%Y-%m-%d")
    cron_log = job_execution_logfile + "/" + str(project) + "/" + str(project) + '_' + str(curr_date) + '_cron.log'
    #cron_log = job_execution_logfile + "/" + str(project) + "/" + str(jobflow_id) + '_' + str(jobflowdetail_id) + '_' + str(sch_type) + '_' + "_cron.log"
    create_log_file(cron_log)

    logger = log_subprocess_debug(cron_log, user)
    #logger.debug("core:util:execute_job_cron:project_id={}, jobflow_id={}, jobflowdetail_id={}, sch_type={}".format(project_id, jobflow_id, jobflowdetail_id, sch_type))
    info_msg = "Start of Execution"
    logger.debug(info_msg)

    info_msg = "execute_job_cron:project_name:{}  ,jobflow_id: {}, jobflowdetail_id:{}, sch_type:{}".format(project, jobflow_id, jobflowdetail_id, sch_type)
    logger.debug(info_msg)

    if sch_type == 0:
        # project_jobname_all_d = {**project_d,}
        info_msg = "core.py:executing all the jobs in project:{}".format(project)
        logger.debug(info_msg)
        exe_project(fake_request, project_id)

    elif sch_type == 1:
        # flowname_d = Jobflow.objects.get(pk=jobflow_id).__dict__
        # project_jobname_all_d = {**project_d, **flowname_d}
        # print("core.py:executing all the jobs in jobflow in the project:",project, 'jobflowid:', jobflow_id)
        info_msg = "core.py:executing all the jobs in jobflow in the project:{}, jobflowid:{}".format(project, jobflow_id)
        logger.debug(info_msg)
        exe_jobflow(fake_request, project_id, jobflow_id)

    elif sch_type == 2:
        info_msg = "core.py:executing single job in the  jobflow in the project:{}, jobflowid:{}, jobflowdetail_id:{}".format(project, jobflow_id, jobflowdetail_id)
        logger.debug(info_msg)
        # execute_single_jobs_generic(fake_request, jobflow_id, jobflowdetail_id)
        cron_exe_jobs(fake_request, project_id, jobflow_id, jobflowdetail_id, cron_log)
        # exe_jobs(fake_request, project_id, jobflow_id, jobflowdetail_id)

    info_msg = "End of Execution"
    logger.debug(info_msg)



project_id = argv[1]
jobflow_id = argv[2]
jobflowdetail_id = argv[3]
sch_type = argv[4]

execute_job_cron(project_id, jobflow_id, jobflowdetail_id, sch_type)












####archival

# p = subprocess.Popen('source /appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev/bin/activate', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# for line in p.stdout.readlines():
#     print(line)
# retval = p.wait()




# def execute_sp(project_id=0, spname_id=0):
# def execute_sp(project_id=0, jobflow_id=0, jobflowdetail_id=0, sch_type=0):
#     request=fake_request
#     project = get_object_or_404(Project, pk=project_id)
#     print("info:execute_jobs, project name:",project, "spname_id:", spname_id)

#     spname_id = int(spname_id)

#     backend_log = job_execution_logfile + str(project) + "/" + "backend_job_execution.log"
#     create_log_file(backend_log)

#     if sch_type == 0:
#         project_jobname_all_d = {**project_d,}
#         print("executing all the jobs in project:",project)
#         exe_sp_all(fake_request, project_id)

#     elif sch_type == 1:
#         flowname_d = Jobflow.objects.get(pk=jobflow_id).__dict__
#         project_jobname_all_d = {**project_d, **flowname_d}

#     elif sch_type == 2:
#         jobflowdetail_d = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__
#         project_jobname_all_d = {**project_d, **jobflowdetail_d}



#     if spname_id == 0:
#         print("executing all the jobs in project:",project)
#         exe_sp_all(fake_request, project_id)

#     else:
#         spname_d = Spname.objects.get(pk=spname_id).__dict__
#         report_name = spname_d['report_name']
#         print("exectuting project",project, "report_name:",report_name)
#         exe_sp(fake_request, project_id, spname_id)

#     print("End of Execution")



# project_id = argv[1]
# spname_id = argv[2] #if len(sys.argv) >= 2 else 0
