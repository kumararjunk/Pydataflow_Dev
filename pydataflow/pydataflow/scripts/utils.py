#from datetime import datetime
import time
import subprocess
import logging
from meta.models import Jobflowdetail
from meta.utils import processlog_create_jobflowdetail_util, processlog_update_log_file_util
from meta.utils import processlog_update_status_util, processlog_update_pid_util
from meta.utils import processlog_update_jobflow_executed_jobnames_util
from meta.utils import email_notification_job
from meta.utils import create_log_file


def log_subprocess_debug(pipe, log_file, user):

    class ContextFilter(logging.Filter):

        def filter(self, record):
            record.user = user
            return True

    logger = logging.getLogger(__name__)
    logger.addFilter(ContextFilter())
    logger.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    formatter = logging.Formatter(
        '%(asctime)s - %(user)s - %(levelname)s -%(name)s - %(message)s')
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
    formatter = logging.Formatter(
        '%(asctime)s - %(user)s - %(levelname)s -%(name)s - %(message)s')
    #log_file = '/Users/arjunkumar/Desktop/notes2/pre-prod/front_end/PyDataFlow_dev2/PyDataFlow/pydataflow/logs/2019-09-25/mlab_adhoc/tmp.txt'
    file_handler = logging.FileHandler(log_file, 'a')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

    # for line in iter(pipe.readline, b''):
    #     logger.debug(line)


def exe_script_util(execution_type, user, process_id, jobflowdetail_id, **script_d):
    print('script:uitl:exe_script_util')
    script_path_name = script_d['script_path_name']
    script_to_execute = []
    Jobflowdetail_d = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__
    jobflowname = Jobflowdetail_d['job_name']

    additional_param = script_d['additional_param'] if len(
        Jobflowdetail_d['additional_param']) == 0 else Jobflowdetail_d['additional_param']

    if len(additional_param) > 0:
        script_to_execute.append(script_path_name + ' ' + additional_param)
    else:
        script_to_execute.append(script_path_name)

    process_log_pk = processlog_create_jobflowdetail_util(
        process_id, jobflowdetail_id)
    time.sleep(.5)

    log_file = create_log_file(
        process_id, process_log_pk, jobflowname, **script_d)
    processlog_update_log_file_util(process_log_pk, log_file)
    time.sleep(.5)
    processlog_update_jobflow_executed_jobnames_util(process_id, jobflowname)

    try:
        print('scripts:util:exe_script_util:process_id:Info:Executing the shell Script name  with parameter:{}, log file:{} '.format(
            script_path_name, log_file))
        process = subprocess.Popen(script_to_execute, executable='/bin/sh',
                                   shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        processlog_update_pid_util(process_log_pk, process.pid)
        print(process.stderr, log_file, user)

        log_subprocess_debug(process.stderr, log_file, user)
        process.wait()

        print('script execution return code:', process.returncode,
              'execution_type:', execution_type)

        if process.returncode == 0:
            print("scripts:util:exe_script_util:process_id:Success in executing the the script:{}, with params:{} for detail, Please refer to logfile:{} ".format(
                script_path_name, additional_param, log_file))
            job_status = 'Success'
            ## script_update_processlog_util(job_status, jobflowdetail_id, process_id, log_type, log_file)
            processlog_update_status_util(job_status, process_log_pk)
            if execution_type == 'S':
                msg = 'Success'
                email_notification_job(msg, process_id, **Jobflowdetail_d)

            return 0

        elif process.returncode == -9 or process.returncode == -15 or process.returncode == -127:
            msg = 'Killed'
            processlog_update_status_util(msg, process_log_pk)
            email_notification_job(msg, process_id, **Jobflowdetail_d)
            # job status is set in kill_process util
            return 9

        else:
            ## log_subprocess_debug(process.stdout, log_file, user)
            logger = log_subprocess_exception(log_file, user)
            logger.exception("scripts:util:exe_script_util:process_id: Warning::Unable to execute the script:{}, with params:{} ".format(
                script_path_name, additional_param))
            logger.exception(
                "process.returncode:{}".format(process.returncode))

            job_status = 'Failed'
            processlog_update_status_util(job_status, process_log_pk)
            # if execution_type == 'single_job':
            msg = job_status
            email_notification_job(msg, process_id, **Jobflowdetail_d)
            # "Fatal error:Unable to execute the script:{}, with params:{} for detail, Please refer to logfile:{} ".format(script_path_name, additional_param, log_file)
            return 9

    except OSError:
        logger = log_subprocess_exception(log_file, user)
        logger.exception("scripts:util:exe_script_util:process_id: Fatal error:Unable to execute the script:{}, with params:{} for detail, Please refer to logfile:{} ".format(
            script_path_name, additional_param, log_file))
        print("scripts:util:exe_script_util:process_id: Fatal error:Unable to execute the script:{}, with params:{} for detail, Please refer to logfile:{} ".format(
            script_path_name, additional_param, log_file))
        return 9


# import os
# import os.path
# import subprocess
# from django.core.mail import send_mail


# from meta.models import Processlog, Project
#from meta.models import Jobflow
# import MySQLdb, sqlite3, cx_Oracle
# User,
# import pyodbc


# def create_log_file(process_id, process_log_pk, jobflowname, **script_d):
#     project_id = script_d['project_name_id']
#     project_d = Project.objects.get(pk=project_id).__dict__
#     project_name = project_d['project_name']
#     ###job_name, job_id = script_d['job_name'], script_d['id']
#     job_id = script_d['id']

#     curr_timestamp = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
#     log_file = str(process_id) + "_" + str(process_log_pk) + \
#         "_" + jobflowname + "_" + str(curr_timestamp) + ".log"

#     curr_date = time.strftime("%Y-%m-%d")

#     project_path = os.path.join(os.path.abspath(os.path.dirname(__name__)))
#     log_path = project_path + "/logs/" + str(curr_date) + "/" + project_name
#     log_file_path = log_path + "/" + log_file

#     pathlib.Path(log_path).mkdir(parents=True, exist_ok=True)
#     ### print('scripts:util:create_log_file:Created logfile:', log_file_path)
#     return log_file_path
