#!/usr/bin/python
import sys ,calendar#, sqlite3, cx_Oracle
#import MySQLdb,
import os.path
import os, subprocess, time, argparse, logging
from shutil import copyfile
# from subprocess import Popen,PIPE
from django.conf import settings
from django.core.mail import send_mail
from collections import deque
from django.shortcuts import render, get_object_or_404, render_to_response
from django.conf import settings
from crontab import CronTab
from meta.utils import sqlite_db_connection
from meta.models import Project, Spname, Jobflow, Jobflowdetail #, Tbllist
from meta.models import Script, Jobflow, Processlog, Sch
import os, getpass

import multiprocessing
from multiprocessing import Semaphore

from django.db.models import Max
import os, pathlib
import argparse, sys, logging, time, subprocess, os.path, calendar


# pre prod setup backup
def cron_set_env():
    print(os.path.abspath(os.path.dirname(__name__)))
    installation_path = os.path.abspath(os.path.dirname(__name__))
    # cd_path = "cd " + installation_path.replace("/PyDataFlow/PyDataFlow/pydataflow", ";")
    cd_path = "cd " + "/appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev2/PyDataFlow/PyDataFlow/pydataflow;"
    print('*'*100)
    source_path = " source " + installation_path.replace("/PyDataFlow/PyDataFlow/pydataflow", "") + "/bin/activate;"
    print('source_path:', source_path)
    #source_path = " source " + "/appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev2/bin/activate;"
    core_path = " cd " + installation_path + "/core;"
    python_path = installation_path.replace("/PyDataFlow/PyDataFlow/pydataflow", "/bin/python ")
    #python_path = "/appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev2" + "/bin/python "
    core_script_path = installation_path + "/core/core.py "
    activate_base_command = cd_path + source_path + core_path + python_path + core_script_path
    # print('cron_set_env', 'python_path:', python_path, type(python_path))
    return activate_base_command

####tested local
# def cron_set_env():
#     print(os.path.abspath(os.path.dirname(__name__)))
#     installation_path = os.path.abspath(os.path.dirname(__name__))
#     #cd_path = "cd " + installation_path.replace("/PyDataFlow/PyDataFlow/pydataflow", ";")
#     cd_path = "cd " + installation_path + ";"
#     #cd_path = "cd " + "/appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev2/PyDataFlow/PyDataFlow/pydataflow;"
#     source_path = " source " + installation_path.replace("/pydataflow", "") + "/bin/activate;"
#     print('installation_path:', installation_path)
#     print('source_path:', source_path)

#     #source_path = " source " + "/appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev2/bin/activate;"
#     core_path = " cd " + installation_path + "/core;"
#     python_path = installation_path.replace("/pydataflow", "/bin/python ")
#     #python_path = "/appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev2" + "/bin/python "
#     core_script_path = installation_path + "/core/core.py "
#     activate_base_command = cd_path + source_path + core_path + python_path + core_script_path
#     # print('cron_set_env', 'python_path:', python_path, type(python_path))
#     return activate_base_command


def value_check(minutes):
    if minutes == '*':
        return None

    elif '/' in minutes:
        minutes = minutes.strip()
        return "'" + str(minutes) + "'"

    elif ',' in minutes:  # mulitple selected mins i.e 3, 4, 5:
        minutes = minutes.replace(", ", ",")
        return "'" + str(minutes) + "'"

    else:
        return minutes

class CronManager:

    def __init__(self):
        self.cron = CronTab(user=getpass.getuser())
        # self.cron = CronTab(user='K390239') # self.cron = CronTab(user='arjunkumar') # self.name = getpass.getuser() # self.user = getpass.getuser()

    def remove_cron(self, name, user, command, comment, environment=None):
        """To Remove cron task by report name"""
        cron_job = self.cron.new(command=command, user=user, comment=comment)
        print("Info:sch_util:CronManager:remove_cron:Removing the project/job from scheudle:",comment)

        cron = CronTab(user=getpass.getuser())
        # cron = CronTab(user='K390239')  # # cron = CronTab(user='arjunkumar')
        for job in cron:
            # if job.comment in comment:
            if comment in job.comment:
                print("match found and removing the comment",comment)
                cron.remove(job)
                cron.write()
                print("Info:sch_util:CronManager:remove_cron:CronManager:Removed the project/job from scheudle:",job)
                return True

    def add_cron(self, name, user, command, comment, minutes, hour, days, months, weekdays,environment=None):
        """ Add a daily cron task"""
        cron_job = self.cron.new(command=command, user=user, comment=comment)
        #print("Info:sch_util:add_cron:", "minutes:", minutes, "hour:", hour, "days:", days, "months:",months, "weekdays:", weekdays, "command", command)

        cmd = "cron_job.setall(" + str(value_check(minutes)) + ', ' + \
                str(value_check(hour))  + ', ' + str(value_check(days)) + ', ' +\
                str(value_check(months))  + ', ' + str(value_check(weekdays)) + \
                ")"
        # print(cmd)
        exec(cmd)
        cron_job.enable()
        self.cron.write()
        if self.cron.render():
            print(self.cron.render())
            return True


def remove_sch_generic_util(record_id):
    sch_d = Sch.objects.get(pk=record_id).__dict__
    sch_type = sch_d['sch_type']
    etl_sch_time = sch_d['etl_sch_time']
    etl_sch_time_list = etl_sch_time.split(':')
    minutes, hour, days, months, weekdays = etl_sch_time_list

    project_id = sch_d['project_name_id']
    project_d = Project.objects.get(pk=project_id).__dict__
    project_name = project_d['project_name']

    jobflow_id = sch_d['jobflowname_id']
    jobflow_d = Jobflow.objects.get(pk=jobflow_id).__dict__

    jobflowdetail_id = sch_d['jobflowdetail_id']
    jobflowdetail_d = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__

    rc = ''
    try:
        activate_base_command = cron_set_env()
        cm = CronManager()
        if sch_type == 1:
            execution_comm = activate_base_command + str(project_id) + " " + str(jobflow_id) + " " + str(0) + " " + str(sch_type)
            rc = cm.remove_cron(name=getpass.getuser(), user=getpass.getuser(), command=execution_comm,
                   comment='Project:' + project_name + " " + 'Jobflowname:' + jobflow_d['jobflowname'] + " Scheudle type:" + str(sch_type) + " Job Name: " + 'Job Flow' + " etl_scheudle:" +  str(etl_sch_time_list) ,
                   environment=None)
            comment='Project:' + project_name + " " + 'Jobflowname:' + jobflow_d['jobflowname'] + " Scheudle type:" + str(sch_type) + " Job Name: " + 'Job Flow' + " etl_scheudle:" +  str(etl_sch_time_list)

        elif sch_type == 2:
            execution_comm = activate_base_command + str(project_id) + " " + str(jobflow_id) + " " + str(jobflowdetail_id) + " " + str(sch_type)
            rc = cm.remove_cron(name=getpass.getuser(), user=getpass.getuser(), command=execution_comm,
                   comment='Project:' + project_name + " " + 'Jobflowname:' + jobflow_d['jobflowname'] + " Scheudle type:" + str(sch_type) + " Job Name: " + jobflowdetail_d['project_job_name'] + " etl_scheudle:" + str(etl_sch_time_list) ,
                    environment=None)



        print("Info:sch_util:remove_sch_generic_util:Removed project from scheudle:", project_name,"etl_sch_time:", etl_sch_time)

        if rc:
            sch_delete = Sch(id=record_id)
            sch_delete.delete()
        else:
            sch_delete = Sch(id=record_id)
            sch_delete.delete()

    except Exception as e:
        raise e

    finally:
        pass
        # sch_delete.save()


def create_etl_sch_util(project_id, jobflow_id=0, jobflowdetail_id=0, sch_type=0, etl_time='* * * * *'):
    project = get_object_or_404(Project, pk=project_id)
    jobflow = get_object_or_404(Jobflow, pk=jobflow_id)

    if sch_type == 1:
        job_type= 'Job Flow'
        #creating dummy jobflowdetail
        jobflowdetail_id = Jobflowdetail.objects.filter(jobflowname=jobflow_id).values()[0]['id']
        jobflowdetail = get_object_or_404(Jobflowdetail, pk=jobflowdetail_id)
    else:
        job_type = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__['job_type']
        jobflowdetail = get_object_or_404(Jobflowdetail, pk=jobflowdetail_id)

    job_name = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__['job_name']

    try:
        sch = Sch(project_name=project, jobflowname=jobflow, jobflowdetail=jobflowdetail,
                job_type=job_type, sch_type=sch_type, etl_sch_time=etl_time
                )
        sch.save()
        sch.delete_cron_url = '/sch_delete_cron/' + str(sch.pk)

        if sch.job_type == 'Job Flow':
            sch.job_name = 'Job Flow'
        else:
            sch.job_name = job_name
        sch.save()

        return sch.pk

    except Exception as e:
        print("Info:sch:create_etl_sch_util:Unable to update the etl_scheudle of project:", project, "jobflow_id:", jobflow_id, 'jobflowdetail_id:', jobflowdetail_id, 'sch_type', sch_type, "etl_time:", etl_time)
        return False
        raise e
    finally:
        sch.save()
        time.sleep(.2)

def scheudle_project_util(project_id, jobflow_id=0, jobflowdetail_id=0, sch_type=0, sch_pk=0):
    sch_etl_sch_time_d = Sch.objects.get(pk=sch_pk).__dict__
    project_d = Project.objects.get(pk=project_id).__dict__
    jobflow_d = Jobflow.objects.get(pk=jobflow_id).__dict__
    project_name = project_d['project_name']

    if sch_type ==2:
        jobflowdetail_d = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__

    etl_sch_time = sch_etl_sch_time_d['etl_sch_time']
    etl_sch_time_list = etl_sch_time.split(':')
    minutes, hour, days, months, weekdays = etl_sch_time_list
    minutes, hour, days, months, weekdays = minutes.strip(), hour.strip(), days.strip(), months.strip(), weekdays.strip()
    print("Info:sch_util:scheudle_project_util:scheudeling the project @ below frequency","minutes:",minutes, "hour:",hour, "days:",days, "months:",months, "weekdays:",weekdays)

    activate_base_command = cron_set_env()
    print('*'*100)
    print('activate_base_command:', activate_base_command)
    execution_comm = activate_base_command + str(project_id) + " " + str(jobflow_id) + " " + str(jobflowdetail_id) + " " + str(sch_type)

    cm = CronManager()
    if sch_type == 1:
        cm.add_cron(name=getpass.getuser(), user=getpass.getuser(),
                    command=execution_comm,minutes=minutes,hour=hour,
                    days=days, months=months, weekdays=weekdays,
                    comment='Project:' + project_name + " " + 'Jobflowname:' + jobflow_d['jobflowname'] + " Scheudle type:" + str(sch_type) + " Job Name: " + 'Job Flow' + " etl_scheudle:" +  str(etl_sch_time_list) ,
                    environment=None)
    elif sch_type == 2:
        cm.add_cron(name=getpass.getuser(), user=getpass.getuser(),
                    command=execution_comm,minutes=minutes,hour=hour,
                    days=days, months=months, weekdays=weekdays,
                    comment='Project:' + project_name + " " + 'Jobflowname:' + jobflow_d['jobflowname'] + " Scheudle type:" + str(sch_type) + " Job Name: " + jobflowdetail_d['project_job_name'] + " etl_scheudle:" + str(etl_sch_time_list) ,
                    environment=None)



########################execute job flow util #########################
#################function for cron:##################################

###### double check the logger if there are not in meta then add and deletes from here
def create_log_file_cron(process_id, **script_d):
    # print("sch:view:create_log_file_cron:script_d:", script_d)
    project_id = script_d['project_name_id']
    #project = get_object_or_404(Project, pk=project_id)
    project_d = Project.objects.get(pk=project_id).__dict__
    project_name = project_d['project_name']

    job_name, job_id = script_d['job_name'], script_d['id']

    curr_timestamp = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    log_file = str(process_id) + "_" + job_name + "_" + str(job_id) + "_" + str(curr_timestamp) + ".log"

    curr_date = time.strftime("%Y-%m-%d")

    project_path = os.path.join(os.path.abspath(os.path.dirname(__name__)))
    log_path = project_path + "/logs/" + str(curr_date) + "/" + project_name
    log_file_path = log_path + "/" + log_file

    pathlib.Path(log_path).mkdir(parents=True, exist_ok=True)
    print('sch:view:create_log_file_cron:Created logfile:', log_file_path)
    return log_file_path

def create_log_file(tmp_log_file_var):
    try:
        log_directory = os.path.dirname(tmp_log_file_var)
        # print("core.py create_log_file, log file path", log_directory)
        pathlib.Path(log_directory).mkdir(parents=True, exist_ok=True)
        # os.remove(tmp_log_file_var)
    except OSError:
        tmp_log_file = open(tmp_log_file_var, 'w')
        tmp_log_file.write('job Log Details:' + "\n")
        tmp_log_file.close()

def log_subprocess_pipe(pipe, log_file, user):

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

    for line in iter(pipe.readline, b''):
        logger.debug(line)

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

#####################
####### execute job flow ####
from meta.utils import processlog_create_jobflow_util#, processlog_update_jobflow_status_util
from meta.utils import processlog_update_pid_util
from meta.utils import email_notification_jobflow, processlog_update_status_util
from meta.utils import processlog_create_jobflowdetail_util, processlog_update_log_file_util
from meta.views import exe_jobs_worker_process, check_flow_status_send_email, exe_jobflow_process
from meta.views import exe_jobs_worker_process_bridge
from meta.views import child_process_monitor, child_process_monitor, child_process#, get_job_flow_max_limit

####### execute job flow ####
def cron_exe_jobflow(request, project_id, jobflow_id, cron_log):
    print('sch:utils:cron_exe_jobflow_cron:', 'project_id:', project_id, 'jobflow_id:', jobflow_id)
    user = request.user
    logger = log_subprocess_debug(cron_log, user)
    # project = get_object_or_404(Project, pk=project_id)
    project_d = Project.objects.get(pk=project_id).__dict__
    jobflow_d = Jobflow.objects.get(pk=jobflow_id).__dict__

    if project_d['is_active'] != 'Y': #checking if the project is active
        error_message = 'Project:' + project_d['project_name'] + ' is Not Active'
        # print(error_message)
        logger.exception(error_message)


    if jobflow_d['is_active'] != 'Y': #checking if the project is active
        error_message = 'Jobflow:' + jobflow_d['jobflowname'] + ' is Not Active'
        # print(error_message)
        logger.exception(error_message)

    jobflowdetail_id = Jobflowdetail.objects.filter(jobflowname=jobflow_id).filter(is_active='Y').values()[0]['id']
    # process_id = processlog_create_jobflow_util(jobflowdetail_id)
    #process_id, jobflow_process_log_id = processlog_create_jobflow_util(jobflowdetail_id)
    process_id, jobflow_process_log_id = processlog_create_jobflow_util(jobflowdetail_id, 'M')

    error_message = 'Job Submited, for Process id:' + str(process_id) + ' ' + 'jobflow_id:' + str(jobflow_id)

    # jobflow_cron_worker_process = multiprocessing.Process(target=exe_jobflow_process, args=(user, process_id,jobflow_id, project_d))
    jobflow_cron_worker_process = multiprocessing.Process(target=exe_jobflow_process, args=(request, user, process_id, jobflow_id, project_id, project_d))
    jobflow_cron_worker_process.start()

    jobflow_cron_worker_process.join()
    time.sleep(.25)

####### end execute job flow ####
#####execute single jobs
def cron_exe_jobs(request, project_id, jobflow_id, jobflowdetail_id, cron_log):
    user = request.user
    logger = log_subprocess_debug(cron_log, user)
    jobflowdetail_d = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__
    user = request.user
    project = get_object_or_404(Project, pk=project_id)
    project_d = project.__dict__
    jobflow_d = Jobflow.objects.get(pk=jobflow_id).__dict__

    cron_is_active_response = cron_is_active(request, cron_log, project_d, jobflow_d, jobflowdetail_d)
    object_id = jobflowdetail_d['object_id']
    job_type = jobflowdetail_d['job_type']

    if cron_is_active_response == 0:
        # process_id = processlog_create_jobflow_util(jobflowdetail_id)
        #process_id, jobflow_process_log_id = processlog_create_jobflow_util(jobflowdetail_id)
        process_id, jobflow_process_log_id = processlog_create_jobflow_util(jobflowdetail_id, 'S')
        info_msg = 'Job Submited, Process id:' + str(process_id) + ' Project Name ' + project_d['project_name']  + ' Jobflow Name ' + jobflow_d['jobflowname']  + ' job_name ' + jobflowdetail_d['job_name']
        logger.debug(info_msg)
        #worker_process = multiprocessing.Process(target=exe_jobs_worker_process, args=(user, process_id, job_type, jobflowdetail_id, object_id, project_d))
        worker_process = multiprocessing.Process(target=exe_jobs_worker_process_bridge, args=(user, process_id, jobflow_process_log_id, job_type, jobflowdetail_id, object_id, project_d))
        worker_process.start()
        time.sleep(.15)
        processlog_update_pid_util(jobflow_process_log_id, worker_process.pid)

        worker_process.join()
        time.sleep(.15)

        ###work on the return code from cron
        # if Processlog.objects.filter(process_id = process_id).filter(jobflowname=jobflow_id).filter(status='Failed').exists():
        #     return 9
        # else:
        #     return 0

    else:
        # error_message = 'project/jobflow/job detail is active' + ' ' + project_d['project_name']  + ' ' + jobflow_d['jobflowname']  + ' ' + jobflowdetail_d['job_name']
        # logger.exception(error_message)
        return 1

def cron_is_active(request, cron_log, project_d, jobflow_d, jobflowdetail_d):
    user = request.user
    logger = log_subprocess_debug(cron_log, user)

    if project_d['is_active'] != 'Y': #checking if the project is active
        error_message = 'Project:' + project_d['project_name'] + ' is Not Active'
        logger.exception(error_message)
        return 1
        #print(error_message)
        # messages.info(request, error_message)
        # return render(request, template_name, {'project': project, 'jobflow': jobflow, 'user': user })

    if jobflow_d['is_active'] != 'Y': #checking if the jobflow is active
        error_message = 'Jobflow:' + jobflow_d['jobflowname'] + ' is Not Active'
        logger.exception(error_message)
        return 1
        #print(error_message)
        # messages.info(request, error_message)
        # return render(request, template_name, {'project': project, 'jobflow': jobflow, 'user': user })

    if jobflowdetail_d['is_active'] != 'Y': #checking if the jobdetail is active
        error_message = 'Job Name:' + jobflowdetail_d['job_name'] + ' is Not Active'
        logger.exception(error_message)
        return 1
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
            return 1
            # messages.info(request, error_message)
            # return render(request, template_name, {'project': project, 'jobflow': jobflow, 'user': user })

    if job_type == 'Shell_Script':
        script_d = Script.objects.get(pk=object_id).__dict__

        if script_d['is_active'] != 'Y':
            error_message = 'Script Name:' + script_d['job_name'] + ' is Not Active, Please check Shell Scripts page'
            logger.exception(error_message)
            return 1
            # messages.info(request, error_message)
            # return render(request, template_name, {'project': project, 'jobflow': jobflow, 'user': user })

    if job_type == 'Table':
        table_d = Tbllist.objects.get(pk=object_id).__dict__

        if table_d['is_active'] != 'Y':
            error_message = 'meta:exe_jobs: executing Table'
            logger.exception(error_message)
            return 1
            # print('meta:exe_jobs: executing Table')
            # print("Executing Table:", job_type, id)
            # return render(request, template_name, {'project': project, 'jobflow': jobflow, 'user': user })
    return 0

#####end execute single jobs

