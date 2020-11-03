#!/usr/bin/python

import os.path, logging, pathlib, argparse, datetime
from datetime import datetime
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

# , log_subprocess_exception
from sch.utils import cron_exe_jobs, cron_exe_jobflow#, exe_project_cron
from sch.utils import log_subprocess_debug, create_log_file

#from scripts.utils import *
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
curr_timestamp = datetime.now()
job_execution_logfile = project_path + "/" "logs/" + str(curr_date) + "/"

#create the log file to capture the job execution

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
    create_log_file(cron_log)

    logger = log_subprocess_debug(cron_log, user)
    info_msg = "Start of Execution:Timestamp" + str(curr_timestamp)
    logger.debug(info_msg)

    info_msg = "execute_job_cron:project_name:{}  ,jobflow_id: {}, jobflowdetail_id:{}, sch_type:{}".format(project, jobflow_id, jobflowdetail_id, sch_type)
    logger.debug(info_msg)

    # checking if project is active
    project_d = Project.objects.get(pk=project_id).__dict__
    if project_d['is_active'] != 'Y': #checking if the jobflow is active
            error_message = 'Project:' + project_d['project_name'] + ' is Not Active'
            #messages.info(request, error_message)
            logger.debug(error_message)
            return 0

    ## not required only jobs or jobflow can be executed, project can't be executed.
    # if sch_type == 0:
    #     info_msg = "core.py:executing all the jobs in project:{}".format(project)
    #     logger.debug(info_msg)
    #     exe_project_cron(fake_request, project_id)

    if sch_type == 1:
        info_msg = "core.py:executing all the jobs in jobflow in the project:{}, jobflowid:{}".format(project, jobflow_id)
        logger.debug(info_msg)

        jobflow_d = Jobflow.objects.get(pk=jobflow_id).__dict__
        if jobflow_d['is_active'] != 'Y': #checking if the jobflow is active
            error_message = 'Jobflow:' + jobflow_d['jobflowname'] + ' is Not Active'
            #messages.info(request, error_message)
            print('error_message:', error_message)
            return 0

        cron_exe_jobflow(fake_request, project_id, jobflow_id, cron_log)

    elif sch_type == 2:
        info_msg = "core.py:executing single job in the  jobflow in the project:{}, jobflowid:{}, jobflowdetail_id:{}".format(project, jobflow_id, jobflowdetail_id)
        logger.debug(info_msg)

        jobflowdetail_d = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__

        if jobflowdetail_d['is_active'] != 'Y': #checking if the jobdetail is active
            error_message = 'Job Name:' + jobflowdetail_d['job_name'] + ' is Not Active'
            print('error_message:', error_message)
            return 0
        cron_exe_jobs(fake_request, project_id, jobflow_id, jobflowdetail_id, cron_log)

    info_msg = "End of Execution"
    logger.debug(info_msg)



project_id = argv[1]
jobflow_id = argv[2]
jobflowdetail_id = argv[3]
sch_type = argv[4]

execute_job_cron(project_id, jobflow_id, jobflowdetail_id, sch_type)
