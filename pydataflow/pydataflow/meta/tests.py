from django.test import TestCase


# Create your tests here.


# command to run in backgroud
# cd /appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev; source /appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev/bin/activate; cd /appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev/PyDataFlow/PyDataFlow/pydataflow;nohup sh -xv /appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev/PyDataFlow/PyDataFlow/pydataflow/start_webserver_8081.sh; ls;pwd;


#old server:
# /appdata/middleware/td2ex-dev-staging/stored_proc/test/bin/python manage.py runserver 10.236.216.154:8080


# lsof -n -i:8081 | grep LISTEN | awk '{print $2}' | xargs kill -9


# ps -ef|grep oracle|cut -d ' ' -f3 |awk '{print $1}' | xargs kill -9



