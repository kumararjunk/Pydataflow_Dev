#!/usr/bin/python
import sqlite3
import os
import sys
import pathlib
import time
import subprocess
import os.path
from shutil import copyfile
from django.conf import settings
from django.core.mail import send_mail
import pymssql
from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Project, Jobflow, Jobflowdetail, Processlog
from django.db.models import Max
#from datetime import datetime
import mysql.connector
from mysql.connector import Error
from django.utils import timezone
from datetime import datetime, timezone
#from .models import User, DataSource, Spname, Tbllist
# import pyodbc
# import calendar, argparse, logging
# import MySQLdb,
#import cx_Oracle
# from collections import deque

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

#######################process log create and update############################################
#jobflow
def processlog_create_jobflow_util(jobflowdetail_id, execution_type):
    print("meta:util:processlog_create_jobflow_util: Creating the process for job flow:", jobflowdetail_id)
    jobflowdetail_d = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__
    jobflowname_id = jobflowdetail_d['jobflowname_id']

    process_id_max = Processlog.objects.aggregate(Max('process_id'))
    process_id = process_id_max['process_id__max']
    process_id = 1 if process_id is None else process_id + 1

    jobflow_id_obj = Jobflow.objects.get(id=jobflowname_id)
    jobflowdetail_id_obj = Jobflowdetail.objects.get(id=jobflowdetail_id)
    project_id_obj = Project.objects.get(id=Jobflow.objects.get(
        pk=jobflowname_id).__dict__['project_name_id'])

    p = Processlog(project_name=project_id_obj, jobflowname=jobflow_id_obj, jobflowdetail=jobflowdetail_id_obj,
                   project_job_name='Job Flow', process_id=process_id,
                   job_name='Job Flow', job_type='Job Flow',
                   object_id=0, additional_param='Job Flow',
                   execution_type=execution_type,
                   status='Executing'
                   )
    p.save()
    return process_id, p.pk

def processlog_update_pid_util(jobflow_process_log_id, pid):
    Processlog.objects.filter(pk=jobflow_process_log_id).update(pid=pid)
    return True


def processlog_update_jobflow_executed_jobnames_util(process_id, jobnames):
    processlog_id = Processlog.objects.filter(
        process_id=process_id).filter(job_type="Job Flow").values()[0]['id']
    p = Processlog.objects.get(pk=processlog_id)

    if len(p.executed_job_names) == 0:
        p.executed_job_names = jobnames
    else:
        p.executed_job_names = p.executed_job_names + ', ' + jobnames
    p.save()
    return True


# def processlog_update_jobflow_status_util(job_status, process_log_jobdetail_pk):
def processlog_update_status_util(job_status, process_log_jobdetail_pk):
    if job_status == 'Success':
        # Processlog.objects.filter(pk=process_log_jobdetail_pk).update(status=job_status, pid=0) # end time stamp is not getting updated with the above one
        p = Processlog.objects.get(pk=process_log_jobdetail_pk)
        p.status = job_status
        p.pid = 0
        p.save()

    else:
        p = Processlog.objects.get(pk=process_log_jobdetail_pk)
        p.status = job_status
        p.save()
    return True

#jobflowdetail from local
def processlog_create_jobflowdetail_util(process_id, jobflowdetail_id):
    jobflowdetail_d = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__
    jobflowname_id = jobflowdetail_d['jobflowname_id']
    project_job_name = jobflowdetail_d['project_job_name']
    job_name = jobflowdetail_d['job_name']
    job_type = jobflowdetail_d['job_type']
    object_id = jobflowdetail_d['object_id']
    additional_param = jobflowdetail_d['additional_param']

    jobflow_id_obj = Jobflow.objects.get(id=jobflowname_id)
    jobflowdetail_id_obj = Jobflowdetail.objects.get(id=jobflowdetail_id)
    project_id_obj = Project.objects.get(id=Jobflow.objects.get(pk=jobflowname_id).__dict__['project_name_id'])

    # added new, to create record if records exist or if does not exist
    p = Processlog(project_name=project_id_obj,
                   jobflowname=jobflow_id_obj, jobflowdetail=jobflowdetail_id_obj,
                   project_job_name=project_job_name, process_id=process_id,
                   job_name=job_name, job_type=job_type,
                   object_id=object_id, additional_param=additional_param,
                   # logfile=log_file,
                   status='Executing')#.save()
    p.save()
    time.sleep(.5)
    return p.pk


def processlog_update_log_file_util(process_log_pk, log_file):
    Processlog.objects.filter(pk=process_log_pk).update(logfile=log_file)
    return True


#######################end process log create and update########################################


def check_processlog_status(process_id):
    print('meta:util:check_processlog_status:checking processlog status',
          'process_id:', process_id)

    if Processlog.objects.filter(process_id=process_id).filter(status='Failed').exists():
        return False
    else:
        return True

#############end compared with script utils.py and functions are merged into meta.utils.py #############
# to run the sp script

def exe_sp_util(execution_type, process_id, **project_spname_all_d):
    project_name = project_spname_all_d['project_name']
    report_name = project_spname_all_d['report_name']
    sp_name = project_spname_all_d['sp_name']
    result_table = project_spname_all_d['result_table']
    start_dt = project_spname_all_d['start_dt']
    end_dt = project_spname_all_d['end_dt']
    med_center = project_spname_all_d['med_center']
    jobflowdetail_id = project_spname_all_d['jobflowdetail_id']
    jobflowname = project_spname_all_d['job_name']

    process_log_pk = processlog_create_jobflowdetail_util(
        process_id, jobflowdetail_id)
    sp_template = os.path.join(os.path.abspath(
        os.path.dirname(__name__)), "core/sp_template.txt")

    in_sp_template = open(sp_template, 'r')
    filedata = in_sp_template.read()
    newdata = filedata.replace("EXECUTE", "EXECUTE")

    curr_date = time.strftime("%Y-%m-%d")
    log_dir = os.path.join(os.path.abspath(os.path.dirname(__name__)), "logs/")

    tmp_template = log_dir + str(curr_date) + "/" + str(project_name) + \
        "/" + "sp_template_out_" + report_name + ".txt"

    log_directory = os.path.dirname(tmp_template)
    pathlib.Path(log_directory).mkdir(parents=True, exist_ok=True)

    if os.path.exists(tmp_template):
        os.remove(tmp_template)
        copyfile(sp_template, tmp_template)
        out_f = open(tmp_template, 'w')
        out_f.write(newdata + "\n")
        in_sp_template.close()
        out_f.close()
    else:
        copyfile(sp_template, tmp_template)
        out_f = open(tmp_template, 'w')
        out_f.write(newdata + "\n")
        in_sp_template.close()
        out_f.close()

    #replace_dict = {'Report_name': report_name, 'sp_name': sp_name, 'start_dt': start_dt, 'end_dt': end_dt, 'med_center': med_center, 'log_dir': log_directory}
    replace_dict = {'Report_name': report_name, 'sp_name': sp_name,
                    'start_dt': start_dt, 'end_dt': end_dt, 'log_dir': log_directory}

    if replace_dict['start_dt'] == 'NULL' and replace_dict['end_dt'] == 'NULL':
        #print('case 1')
        line_index = 22
        lines = None
        with open(tmp_template, 'r') as file_handler:
            lines = file_handler.readlines()

        lines.insert(
            line_index, "EXECUTE nc_group_rltg.sp_name(start_dt,end_dt,null,:rsltout)")

        with open(tmp_template, 'w') as file_handler:
            file_handler.writelines(lines)

    elif replace_dict['start_dt'] == 'NULL' and replace_dict['end_dt'] != 'NULL':
        #print('case 2')
        line_index = 22
        lines = None
        with open(tmp_template, 'r') as file_handler:
            lines = file_handler.readlines()

        # lines.insert(line_index, "EXECUTE nc_group_rltg.sp_name(to_date('start_dt','MM-DD-YYYY'),end_dt,null,:rsltout)")
        lines.insert(
            line_index, "EXECUTE nc_group_rltg.sp_name(start_dt,to_date('end_dt','MM-DD-YYYY'),null,:rsltout)")

        with open(tmp_template, 'w') as file_handler:
            file_handler.writelines(lines)

    elif replace_dict['start_dt'] != 'NULL' and replace_dict['end_dt'] == 'NULL':
        #print('case 3')
        line_index = 22
        lines = None
        with open(tmp_template, 'r') as file_handler:
            lines = file_handler.readlines()

        # lines.insert(line_index, "EXECUTE nc_group_rltg.sp_name(start_dt,to_date('end_dt','MM-DD-YYYY'),null,:rsltout)")
        lines.insert(
            line_index, "EXECUTE nc_group_rltg.sp_name(to_date('start_dt','MM-DD-YYYY'),end_dt,null,:rsltout)")

        with open(tmp_template, 'w') as file_handler:
            file_handler.writelines(lines)

    else:
        #print('case 4')
        line_index = 22
        lines = None
        with open(tmp_template, 'r') as file_handler:
            lines = file_handler.readlines()

        lines.insert(
            line_index, "EXECUTE nc_group_rltg.sp_name(to_date('start_dt','MM-DD-YYYY'),to_date('end_dt','MM-DD-YYYY'),null,:rsltout)")

        with open(tmp_template, 'w') as file_handler:
            file_handler.writelines(lines)

    for keys, values in replace_dict.items():
        sp_template = tmp_template
        tmp_template_read = open(sp_template, 'r')
        filedata = tmp_template_read.read()

        newdata = filedata.replace(keys, values)
        tmp_template = tmp_template
        out_f = open(tmp_template, 'w')
        out_f.write(newdata + "\n")
        in_sp_template.close()
        out_f.close()

    log_file = create_log_file(
        process_id, process_log_pk, jobflowname, **project_spname_all_d)
    processlog_update_log_file_util(process_log_pk, log_file)

    # uncomment below command
    exe_sp_shell_script_rc = exe_sp_shell_script(
        process_log_pk, process_id, tmp_template, log_file, **project_spname_all_d)
    #exe_sp_shell_script_rc = 0
    time.sleep(.15)

    Jobflowdetail_d = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__

    if exe_sp_shell_script_rc == 0:
        job_status = 'Success'
        processlog_update_status_util(job_status, process_log_pk)
        if execution_type == 'S':
            print('Success', 'job_status', job_status, 'process_id',
                  process_id, 'Jobflowdetail_d', Jobflowdetail_d)
            email_notification_job(
                msg=job_status, process_id=process_id, **Jobflowdetail_d)
            return 0
    else:
        job_status = 'Failed'
        processlog_update_status_util(job_status, process_log_pk)
        # if execution_type == 'single_job':
        #msg = 'Execution Failed for process id:' + str(process_id)

        print('Failed', 'job_status', job_status, 'process_id',
              process_id, 'Jobflowdetail_d', Jobflowdetail_d)
        email_notification_job(
            msg=job_status, process_id=process_id, **Jobflowdetail_d)
        return 9


def exe_sp_shell_script(process_log_pk, process_id, tmp_template, tmp_log_file_var, **project_spname_all_d):
    report_name = project_spname_all_d['report_name']
    result_table = project_spname_all_d['result_table']
    print('project_spname_all_d', project_spname_all_d['job_name'])

    try:
        log_file = open(tmp_log_file_var, "w")
        project_path = os.path.abspath(os.path.dirname(__name__))
        core_script_path = os.path.join(
            os.path.abspath(os.path.dirname(__name__)), "core/")
        process = subprocess.Popen(["sh", core_script_path + "execute_sp.sh",
                                    tmp_template, report_name, result_table], stdout=log_file)
        # only for test process = subprocess.Popen(["sh", core_script_path + "test.sh", tmp_template, report_name, result_table], stdout=log_file)
        processlog_update_pid_util(process_log_pk, process.pid)

        # processlog_update_jobflow_executed_jobnames_util(
        #     process_id, project_spname_all_d['job_name'])
        # process.wait()
        job_name_sp_name_report_name = project_spname_all_d['job_name'] + ', ' + \
            project_spname_all_d['report_name'] + \
            ', ' + project_spname_all_d['sp_name']
        processlog_update_jobflow_executed_jobnames_util(
            process_id, job_name_sp_name_report_name)
        process.wait()

        if process.returncode == 0:
            print(
                "meta:util:exe_sp_shell_script:Info:exe_sp_shell_script:executing check_report_status:")
            check_report_status(tmp_log_file_var, process_id,
                                **project_spname_all_d)
            log_file.close()
            return 0
        else:
            log_file.close()
            #print('process.returncode:', process.returncode)
            return 1
    except OSError:
        print("meta:util:exe_sp_shell_script:Fatal error:exe_sp_shell_script: unable to execute the script for report:{} ".format(report_name))
        return 9


def check_report_status(filename, process_id, **project_spname_all_d):
    print("meta:util:check_report_status:filename:", filename,
          'project_spname_all_d', project_spname_all_d)
    report_name = project_spname_all_d['report_name']
    curr_date = time.strftime("%Y-%m-%d")
    project_name = project_spname_all_d['project_name']
    project_path = os.path.join(os.path.abspath(os.path.dirname(__name__)))
    summary_file = project_path + "/logs/" + curr_date + "/" + \
        project_name + "/" + "summary_" + curr_date + ".txt"
    # print("Info:check_report_status:",project_path,project_name,curr_date, report_name,summary_file )

    if not os.path.exists(summary_file):
        with open(summary_file, 'w'):
            pass

    Jobflowdetail_d = Jobflowdetail.objects.get(
        pk=project_spname_all_d['jobflowdetail_id']).__dict__

    print("meta:util:check_report_status:Info:checking the end of file for ERROR OR ORA-")
    if check_log_file_tail(filename, 50, report_name, project_name):
        print("meta:util:check_report_statusFatal Error:check_report_status:create_log_file:Storted Proc Execution Failed:", report_name)
        # print("meta:util:check_report_statusFatal Error:check_report_status:create_log_file:error key word is found in the files:")
        f = open(summary_file, 'a')
        f.write('failed|' + project_name + "|" + report_name + '\n')
        f.close()
        #email_notification(msg = 'Execution Failed', **project_spname_all_d)

        email_notification_job(
            msg='Warning', process_id=process_id, **Jobflowdetail_d)

    else:
        print("meta:util:check_report_statusSuccess:check_report_status:Storted Proc Executed Successfully:", report_name)
        f = open(summary_file, 'a')
        f.write('success|' + project_name + "|" + report_name + '\n')
        f.close()
        #email_notification(msg = 'Executed Successfully', **project_spname_all_d)


def check_log_file_tail(filename, nl, report_name, project_name):
    print('meta:util:check_log_file_tail',
          'checking for error in the data file:')
    curr_date = time.strftime("%Y-%m-%d")
    with open(filename) as f:
        data = f.readlines()
        lines = ''.join(data[-nl:])
        data_file = os.path.join(os.path.abspath(os.path.dirname(
            __name__)), "logs/" + curr_date + "/" + project_name + "/" + report_name + "_data.txt")
        num_lines = sum(1 for line in open(data_file))

        if "ERROR" in lines:
            return True
        elif "ORA-" in lines:
            return True
        else:
            try:
                os.remove(data_file)
            except:
                print("Error while deleting log file ", data_file)
            return False


def create_log_file(process_id, process_log_pk, jobflowname, **script_d):
    # print("scripts:util:create_log_file:script_d:", script_d)
    project_id = script_d['project_name_id']
    project = get_object_or_404(Project, pk=project_id)
    project_d = Project.objects.get(pk=project_id).__dict__
    project_name = project_d['project_name']

    job_name, job_id = script_d['job_name'], script_d['id']

    curr_timestamp = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    log_file = str(process_id) + "_" + str(process_log_pk) + \
        "_" + jobflowname + "_" + str(curr_timestamp) + ".log"

    curr_date = time.strftime("%Y-%m-%d")

    project_path = os.path.join(os.path.abspath(os.path.dirname(__name__)))
    log_path = project_path + "/logs/" + str(curr_date) + "/" + project_name
    log_file_path = log_path + "/" + log_file

    pathlib.Path(log_path).mkdir(parents=True, exist_ok=True)
    print('scripts:util:create_log_file:Created logfile:', log_file_path)
    return log_file_path


####################email notification####################

def email_notification_logrunning_job(msg=None, process_id=0, **Jobflowdetail_d):
    env = settings.CLUSTER_NAME
    from_email = settings.FROM_EMAIL

    jobflow_d = Jobflow.objects.get(
        pk=Jobflowdetail_d['jobflowname_id']).__dict__
    job_flow_name = jobflow_d['jobflowname']
    project_d = Project.objects.get(pk=jobflow_d['project_name_id']).__dict__
    project_name = project_d['project_name']
    job_name = Jobflowdetail_d['job_name']
    start_time = Processlog.objects.filter(process_id=process_id).filter(
        job_name=job_name).values_list('start_time', flat=True).distinct()[::1]
    start_time = str(utc_to_local(start_time[0]))[0:19]
    end_time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

    subject = 'Job is running more than 3 hours' + ':  ' + str(env) + '  ' + 'Project Name:' + str(
        project_name) + '  ' + 'Job flow name:' + str(job_flow_name) + '  ' + 'Job Name:' + str(job_name) + '  ' + 'Process id:' + str(process_id)
    topic = 'Issue: Job is running more than 3 hours'

    if project_d['failure_email_ind']:
        recipient_list = [r.strip()
                          for r in project_d['success_email'].split(',')]
    else:
        recipient_list = [r.strip()
                          for r in project_d['failure_email'].split(',')]

    message = '''\n
               Hi Support Team, \n

               {env} \n
               {topic} \n
               Process id: {process_id} \n
               Job Name: {job_name} \n
               Job Flow Name: {job_flow_name} \n
               Project Name: {project_name} \n
               Job Start Date and Time: {start_time}\n
               Job End Date and Time: {end_time}\n
               \n
               '''.format(env=env, topic=topic, project_name=project_name, process_id=process_id, job_flow_name=job_flow_name, job_name=job_name, start_time=start_time, end_time=end_time)
    send_mail_func(subject, message, from_email, recipient_list)


def email_notification_jobflow(msg=None, failed_killed_jobnames=None, process_id=0, jobflow_id=None):
    env = settings.CLUSTER_NAME
    from_email = settings.FROM_EMAIL

    jobflow_name_d = Jobflow.objects.get(pk=jobflow_id).__dict__
    project_d = Project.objects.get(
        pk=jobflow_name_d['project_name_id']).__dict__

    project_name = project_d['project_name']
    job_flow_name = jobflow_name_d['jobflowname']

    start_time = Processlog.objects.filter(process_id=process_id).filter(
        job_name='Job Flow').values_list('start_time', flat=True).distinct()[::1]
    start_time = str(utc_to_local(start_time[0]))[0:19]
    end_time = Processlog.objects.filter(process_id=process_id).filter(
        job_name='Job Flow').values_list('end_time', flat=True).distinct()[::1]
    end_time = str(utc_to_local(end_time[0]))[0:19]

    subject = msg + ':  ' + str(env) + '  ' + 'Project Name:' + str(project_name) + '  ' + \
        'Job flow name:' + str(job_flow_name) + '  ' + \
        'Process id:' + str(process_id)

    if msg == 'Success':
        topic = 'Jobflow Completed Successfully'

    elif msg == 'Failed':
        topic = 'Issue: Failed to execute jobflow'

    elif msg == 'Killed':
        topic = 'Issue: Jobflow is Killed'

    elif msg == 'Long running Job':
        topic = 'Issue: Jobflow is running more than' + '3 hours'

    elif msg == 'In-Complete Run':
        topic = 'Issue: All the jobs did not executed from the Jobflow '

    if msg == 'Success':
        recipient_list = [r.strip()
                          for r in project_d['success_email'].split(',')]

    else:
        if project_d['failure_email_ind']:
            recipient_list = [r.strip()
                              for r in project_d['success_email'].split(',')]
        else:
            recipient_list = [r.strip()
                              for r in project_d['failure_email'].split(',')]

    message = '''\n
               Hi Support Team, \n

               {env} \n
               {topic} \n
               Process id: {process_id} \n
               Job Name: {job_name} \n
               Job Flow Name: {job_flow_name} \n
               Project Name: {project_name} \n
               Job Start Date and Time: {start_time}\n
               Job End Date and Time: {end_time}\n
               \n
               '''.format(env=env, topic=topic, process_id=process_id, project_name=project_name, job_flow_name=job_flow_name, job_name=failed_killed_jobnames, start_time=start_time, end_time=end_time)

    send_mail_func(subject, message, from_email, recipient_list)


def email_notification_job(msg=None, process_id=0, **Jobflowdetail_d):
    env = settings.CLUSTER_NAME
    from_email = settings.FROM_EMAIL

    jobflow_d = Jobflow.objects.get(
        pk=Jobflowdetail_d['jobflowname_id']).__dict__
    job_flow_name = jobflow_d['jobflowname']
    project_d = Project.objects.get(pk=jobflow_d['project_name_id']).__dict__
    project_name = project_d['project_name']
    job_name = Jobflowdetail_d['job_name']

    start_time = Processlog.objects.filter(process_id=process_id).filter(
        job_name=job_name).values_list('start_time', flat=True).distinct()[::1]
    start_time = str(utc_to_local(start_time[0]))[0:19]
    end_time = Processlog.objects.filter(process_id=process_id).filter(
        job_name=job_name).values_list('end_time', flat=True).distinct()[::1]
    end_time = str(utc_to_local(end_time[0]))[0:19]

    subject = msg + ':  ' + str(env) + '  ' + 'Project Name:' + str(project_name) + '  ' + 'Job flow name:' + str(
        job_flow_name) + '  ' + 'Job Name:' + str(job_name) + '  ' + 'Process id:' + str(process_id)

    if msg == 'Success':
        topic = 'Job Completed Successfully'

    elif msg == 'Failed':
        topic = 'Issue: Failed to execute job'

    elif msg == 'Killed':
        topic = 'Issue: Job is Killed'

    elif msg == 'Warning':
        topic = 'Issue: Error in executing the sp or it generated less then 10 records'

    if msg == 'Success':
        recipient_list = [r.strip()
                          for r in project_d['success_email'].split(',')]

    else:
        if project_d['failure_email_ind']:
            recipient_list = [r.strip()
                              for r in project_d['success_email'].split(',')]
        else:
            recipient_list = [r.strip()
                              for r in project_d['failure_email'].split(',')]

    message = '''\n
               Hi Support Team, \n

               {env} \n
               {topic} \n
               Process id: {process_id} \n
               Job Name: {job_name} \n
               Job Flow Name: {job_flow_name} \n
               Project Name: {project_name} \n
               Job Start Date and Time: {start_time}\n
               Job End Date and Time: {end_time}\n
               \n
               '''.format(env=env, topic=topic, process_id=process_id, project_name=project_name, job_flow_name=job_flow_name, job_name=job_name, start_time=start_time, end_time=end_time)
    send_mail_func(subject, message, from_email, recipient_list)


def send_mail_func(subject, message, from_email, recipient_list):
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False, auth_user=None, auth_password=None, connection=None,
        html_message=None)

####################end email notification####################



def export_env_variable(project_id):
    print('meta:util:export_env_variable', 'project_id', project_id)
    # import os, sys
    sqlite_conn = sqlite_db_connection()
    cur_sqlite = sqlite_conn.cursor()
    get_env_variable_stmt = (
        "select env_variable_name,env_variable_value from meta_Env_variables_projects where project_name_id={};".format(project_id))

    cur_sqlite.execute(get_env_variable_stmt)
    env_variable_list = list(cur_sqlite.fetchall())

    for env_name, env_name_value in env_variable_list:
        if env_name in os.environ:
            print('Existing env variable:', env_name, os.environ[env_name])
        # if env_name not in os.environ:
        try:
            os.environ[env_name] = env_name_value
        except Exception as e:
            print('Failed to set the env variable:', sys.argv[0])
            raise e
            # sys.exit(1)

        if env_name in os.environ:
            print('Success: in seting the env:',
                  env_name, os.environ[env_name])
    project = get_object_or_404(Project, pk=project_id)
    project_d = Project.objects.get(pk=project_id).__dict__
    print("project_d", project_d)
    # conn = cx_Oracle.connect('NC_RLTGRPT_EXT/Report16@(description=(address=(protocol=tcp)(host=scan-nzepc01f01db001x.nndc.kp.org)(port=1571))(connect_data=(service_name=PRODNCM_USR.nndc.kp.org)))')
    # var = conn.version.split(",")
    # curs = conn.cursor()
    # print("Info:get_oracle_sp_status:Importing data from Oracle DB....")


####################dsn connection ####################

def test_mysql_conn(**dsn_conn_dict):
    print('meta:util:test_mysql_conn:Trying to create mysql connection')
    db_host = dsn_conn_dict['db_host']
    db_user = dsn_conn_dict['db_user']
    db_pw = dsn_conn_dict['db_pw']
    db_name = dsn_conn_dict['db_name']
    is_connected_ind = False
    try:
        connection = mysql.connector.connect(host=db_host,
                                             database=db_name,
                                             user=db_user,
                                             password=db_pw)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("Connected to MySQL database... MySQL Server version on ",
                  db_Info, "you are connected to", record)
            is_connected_ind = True
            return 'mysql', 'success', connection

    except Error as e:
        print("Error while connecting to MySQL", e)
        return 'mysql', 'failure', e
    finally:
        # closing database connection.
        # print('executing finaly statement')
        if is_connected_ind:
            if connection.is_connected():
                cursor.close()
                connection.close()
                # print("MySQL connection is closed")

# pymssql


def test_sqlserver_conn(**dsn_conn_dict):
    print('meta:util:test_sqlserver_conn:Trying to create Sqlserver connection util:dsn_conn_dict', dsn_conn_dict)
    db_host = dsn_conn_dict['db_host']
    db_user = dsn_conn_dict['db_user']
    db_pw = dsn_conn_dict['db_pw']
    db_name = dsn_conn_dict['db_name']
    port_no = dsn_conn_dict['db_port_no']

    is_connected_ind = False
    try:
        connection = pymssql.connect(host=db_host,
                                     database=db_name,
                                     port=port_no,
                                     user=db_user,
                                     password=db_pw,
                                     autocommit=True)
        cursor = connection.cursor()

        if cursor.connection:
            print("sql server connection test")
            cursor.execute("select @@version;")
            db_Info = cursor.fetchone()

            cursor.execute("SELECT DB_NAME() AS [Current Database];")
            dbname = cursor.fetchone()
            print("Connected to Sql Server database... Sql Server version on ",
                  db_Info, "you are connected to", dbname)
            is_connected_ind = True
            return 'sqlserver', 'success', connection

    # except Error as e :
    except Exception as e:
        print("Error while connecting to SQL Server", e)
        return 'sqlserver', 'failure', e
    finally:
        # closing database connection.
        # print('executing finaly statement')
        if is_connected_ind:
            if cursor.connection:
                cursor.close()
                connection.close()
                print("sqlserver connection is closed")


def test_dsn_generic(**dsn_conn_dict):
    print('meta:util:test_dsn_generic:dsn_conn_dict:', dsn_conn_dict)
    db_type = dsn_conn_dict['db_type']

    if db_type == 'mysql':
        print('db_type == mysql')
        dsn_conn = test_mysql_conn(**dsn_conn_dict)

    elif db_type == 'sqlserver':
        print('db_type == sqlserver')
        dsn_conn = test_sqlserver_conn(**dsn_conn_dict)

    elif db_type == 'oracle':
        print('db_type == oracle')
        dsn_conn = 'oracle'

    elif db_type == 'teradata':
        print('db_type == teradata')
        dsn_conn = 'teradata'

    # return dsn_conn

    try:
        # dsn_conn_cursor = dsn_conn.cursor()
        # print('Testing the dsn, connection:', dsn_conn)
        # return dsn_conn_cursor
        # dsn_conn_cursor.close()
        return dsn_conn

    except Error as e:
        print("Error in creating rdbms connection, using the user credentials from the DSN:", db_name, e)
        return None
    finally:
        print("")
        # dsn_conn.close()
        # dsn_conn_cursor.close()

# get data from dsn


def get_sqlserver_conn(**dsn_conn_dict):
    print('meta:util:get_sqlserver_conn:dsn_conn_dict:', dsn_conn_dict)
    user = dsn_conn_dict['user_id']
    # print("Trying to create mysql connection", dsn_conn_dict)
    db_host = dsn_conn_dict['db_host']
    db_user = dsn_conn_dict['db_user']
    db_pw = dsn_conn_dict['db_pw']
    db_name = dsn_conn_dict['db_name']
    dsn_name_id = dsn_conn_dict['id']
    db_object_type = dsn_conn_dict['db_object_type']
    port_no = dsn_conn_dict['db_port_no']
    project_name_id = dsn_conn_dict['project_name_id']
    # print("db_object_type db_object_type db_object_type", db_object_type, type(db_object_type))

    is_connected_ind = False

    try:
        connection = pymssql.connect(host=db_host,
                                     database=db_name,
                                     port=port_no,
                                     user=db_user,
                                     password=db_pw,
                                     autocommit=True)
        cursor = connection.cursor()

        if cursor.connection:
            cursor = connection.cursor()
            # add the details for stored proc

            sql_get_tbl_names = ("select distinct {} as user_id, {} as project_name,a.name as table_name, 'T' as table_type,'False' as is_selected, {} as dsn_name_id from sys.tables a;".format(
                user, project_name_id, dsn_name_id))

            cursor.execute(sql_get_tbl_names)
            tbl_lists = cursor.fetchall()
            # all_tbl_lists = [list(i) for i in tbl_lists]
            if db_object_type == 'T':
                all_tbl_lists = [list(i)
                                 for i in tbl_lists if list(i)[3] == 'T']
            elif db_object_type == 'V':
                all_tbl_lists = [list(i)
                                 for i in tbl_lists if list(i)[3] == 'V']
            elif db_object_type == 'S':
                all_tbl_lists = [list(i)
                                 for i in tbl_lists if list(i)[3] == 'S']

            # , tbl_lists
            print('Successfully Connected to Sql Server database...,retrieved the tablename from sql server, inserting below table list')

            sqlite_conn = sqlite_db_connection()
            sqlite_cursor = sqlite_conn.cursor()

            db_object_type = "'" + db_object_type + "'"
            sqlite_cursor.execute("DELETE FROM meta_InitialTbllist where user_id = {} and project_name_id = {} and dsn_name_id = {} and table_type = {};".format(
                user, project_name_id, dsn_name_id, db_object_type))
            sqlite_conn.commit()

            insert_statement = (
                "INSERT INTO meta_InitialTbllist (user_id,project_name_id,table_names,table_type,is_selected,dsn_name_id) VALUES (?,?,?,?,?,?);")

            sqlite_cursor.executemany(insert_statement, all_tbl_lists)
            sqlite_conn.commit()
            sqlite_conn.close()
            is_connected_ind = True
            return 'mysql', 'success', connection

    except Error as e:
        print("Error while connecting to MySQL", e)
        return 'mysql', 'failure', e
    finally:
        # closing database connection.
        # print('executing finaly statement')
        if is_connected_ind:
            if cursor.connection:
                cursor.close()
                connection.close()
                print("sqlserver connection is closed")


def get_data_mysql_conn(**dsn_conn_dict):
    print('meta:util:get_data_mysql_conn:dsn_conn_dict:', dsn_conn_dict)
    user = dsn_conn_dict['user_id']
    # print("Trying to create mysql connection", dsn_conn_dict)
    db_host = dsn_conn_dict['db_host']
    db_user = dsn_conn_dict['db_user']
    db_pw = dsn_conn_dict['db_pw']
    db_name = dsn_conn_dict['db_name']
    dsn_name_id = dsn_conn_dict['id']
    db_object_type = dsn_conn_dict['db_object_type']
    project_name_id = dsn_conn_dict['project_name_id']
    is_connected_ind = False

    try:
        connection = mysql.connector.connect(host=db_host,
                                             database=db_name,
                                             user=db_user,
                                             password=db_pw)
        if connection.is_connected():
            cursor = connection.cursor()
            # add the details for stored proc
            db_name = "'" + db_name + "'"
            sql_get_tbl_names = ("SELECT distinct {} as user_id, {} as project_name, table_name, \
                                CASE WHEN table_type like '%TABLE%' THEN 'T' ELSE 'V' END AS table_type, \
                                'False' as is_selected, {} as dsn_name_id FROM information_schema.tables AS t, \
                                (SELECT @i:=0) AS foo where t.table_schema= {} ;"
                                 .format(user, project_name_id, dsn_name_id, db_name))
            cursor.execute(sql_get_tbl_names)
            tbl_lists = cursor.fetchall()

            # all_tbl_lists = [list(i) for i in tbl_lists]
            if db_object_type == 'T':
                all_tbl_lists = [list(i)
                                 for i in tbl_lists if list(i)[3] == 'T']
            elif db_object_type == 'V':
                all_tbl_lists = [list(i)
                                 for i in tbl_lists if list(i)[3] == 'V']
            elif db_object_type == 'S':
                all_tbl_lists = [list(i)
                                 for i in tbl_lists if list(i)[3] == 'S']

            # , tbl_lists
            print('Successfully Connected to MySQL database... MySQL Server,retrieved the tablename from mysql, inserting below table list')

            sqlite_conn = sqlite_db_connection()
            sqlite_cursor = sqlite_conn.cursor()

            db_object_type = "'" + db_object_type + "'"
            # print("DELETE FROM meta_InitialTbllist where user_id = {} and project_name_id = {} and dsn_name_id = {} and table_type= {};".format(user, project_name_id, dsn_name_id, db_object_type))

            sqlite_cursor.execute("DELETE FROM meta_InitialTbllist where user_id = {} and project_name_id = {} and dsn_name_id = {} and table_type= {};".format(
                user, project_name_id, dsn_name_id, db_object_type))
            sqlite_conn.commit()

            insert_statement = (
                "INSERT INTO meta_InitialTbllist (user_id,project_name_id,table_names,table_type,is_selected,dsn_name_id) VALUES (?,?,?,?,?,?);")

            sqlite_cursor.executemany(insert_statement, all_tbl_lists)
            sqlite_conn.commit()
            sqlite_conn.close()
            is_connected_ind = True
            return 'mysql', 'success', connection

    except Error as e:
        print("Error while connecting to MySQL", e)
        return 'mysql', 'failure', e
    finally:
        # closing database connection.
        if is_connected_ind:
            if connection.is_connected():
                cursor.close()
                connection.close()
                # print("MySQL connection is closed")

# refresh_tbl_list_util


def get_data_using_dsn_generic_util(**dsn_details):
    print('meta:util:get_data_using_dsn_generic_util:dsn_details:', dsn_details)
    # print('msg from refresh_tbl_list_util refresh_tbl_list_util')
    user = dsn_details['user_id']
    project_name = dsn_details['project_name_id']
    db_type = dsn_details['db_type']

    if db_type == 'mysql':
        # print('db_type == mysql')
        dsn_conn = get_data_mysql_conn(**dsn_details)

    elif db_type == 'sqlserver':
        # print('db_type == sqlserver')
        dsn_conn = get_sqlserver_conn(**dsn_details)

    # dsn_conn = get_dsn_generic(**dsn_details)

    if dsn_conn[1] == 'success':
        print('msg from refresh_tbl_list_util refresh_tbl_list_util', dsn_conn)

    return None

# load initial tables:


def load_tbllist_util(**dsn_details):
    print('meta:util:load_tbllist_util:dsn_details:', dsn_details)
    user = dsn_details['user_id']
    project_name = dsn_details['project_name_id']
    db_type = dsn_details['db_type']

    if db_type == 'mysql':
        dsn_conn = get_data_mysql_conn(**dsn_details)

    elif db_type == 'sqlserver':
        dsn_conn = get_sqlserver_conn(**dsn_details)

    # dsn_conn = get_dsn_generic(**dsn_details)

    if dsn_conn[1] == 'success':
        print('msg from refresh_tbl_list_util refresh_tbl_list_util', dsn_conn)

    return None

#############running command #######


def run_cmd(args_list):
    print('meta:util:run_cmd:Running system command: {0}'.format(
        ' '.join(args_list)))
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (output, errors) = proc.communicate()
    if proc.returncode:
        raise RuntimeError(
            'Error running command: %s. Return code: %d, Error: %s' % (
                ' '.join(args_list), proc.returncode, errors))
    return (output, errors)

##########db connection #######


def set_oracle_ld_path():
    if 'LD_LIBRARY_PATH' not in os.environ:
        os.environ['LD_LIBRARY_PATH'] = '/appdata/middleware/oracle_instant_client/instantclient_12_2'
        print("Info:set_oracle_ld_path:set oracle path '/appdata/middleware/oracle_instant_client/instantclient_12_2'")

    elif 'LD_LIBRARY_PATH' in os.environ:
        print('Success:', os.environ['LD_LIBRARY_PATH'])
        print("Info:execute_single_sp_util:Success in setting oracle_ld_path:")
    else:
        print(
            "Fatal:execute_single_sp_util:Not able to set the oracle LD_LIBRARY_PATH path:")
        sys.exit(1)


def sqlite_db_connection():
    try:
        sqlite_db = os.path.join(os.path.abspath(
            os.path.dirname(__name__)), "db.sqlite3")
        sqlite_conn = sqlite3.connect(sqlite_db)
        # conn = sqlite3.connect(db_file)
        return sqlite_conn
    except Error as e:
        print(e)

    return None

######Get data from oracle and sqlite db and refresh the status#######





######################################################end of dsn connection######################################################



# def processlog_update_jobflow_status_util(job_status, jobflow_process_log_id):
#     # Processlog.objects.filter(pk=jobflow_process_log_id).update(status=job_status, pid=0)
#     p = Processlog.objects.get(pk=jobflow_process_log_id)
#     p.status = job_status
#     p.pid = 0
#     p.save()
#     return True


# def processlog_update_jobflow_pid_util(process_id, jobflow_id, pid):
#     jobflow_id_obj = Jobflow.objects.get(id=jobflow_id)
#     processlog_id = Processlog.objects.filter(process_id=process_id).filter(jobflowname=jobflow_id_obj)\
#         .values()[0]['id']
#     print("meta:util:processlog_update_jobflow_pid_util updating the process pid",
#           'process_id:', process_id, 'pid', pid)

#     p = Processlog.objects.get(pk=processlog_id)
#     p.pid = pid
#     p.save()

#     return True


# def processlog_update_status_util(job_status, process_log_jobdetail_pk):
#     p = Processlog.objects.get(pk=process_log_jobdetail_pk)
#     if p.status == 'Executing':
#         p.status = job_status
#         p.pid = 0
#     else:
#         p.status = job_status

#     p.save()
#     return True

