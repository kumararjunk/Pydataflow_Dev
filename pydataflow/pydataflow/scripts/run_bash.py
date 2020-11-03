import argparse, os ,sys, logging, pathlib, time, subprocess, os.path, calendar


def log_subprocess_debug(pipe, log_file, user):

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


logfile='/appdata/middleware/sqlserver_migration/scripts/log.txt'



pass_arg=[]
# pass_arg[0] = "/appdata/middleware/sqlserver_migration/scripts/sqoop_sql_server_generic_etl_mgmt.sh"
# pass_arg[1] = "rl_stage"
# pass_arg[2] = "slide_track"

pass_arg = ["/appdata/middleware/sqlserver_migration/scripts/sqoop_sql_server_generic_etl_mgmt.sh", "rl_stage", "slide_track"]



print(pass_arg[0])

def exe_script_util(pass_arg):
    subprocess.check_call(pass_arg)


# exe_script_util(pass_arg)

log_file = "/appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev2/PyDataFlow/PyDataFlow/pydataflow/logs/2019-10-30/cytology_rl_stage/221_slide_track_80_2019-10-30-14:37:01.log"
script_d = "123"


def test():
    with open(log_file, "w") as att_file:
        att_file.write(script_d + "\n")

test()



