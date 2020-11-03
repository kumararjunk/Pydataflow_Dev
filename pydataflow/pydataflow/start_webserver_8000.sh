#!/bin/sh

lsof -n -i:8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

rm -f /appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev2/PyDataFlow/PyDataFlow/pydataflow/nohup.out

cd /appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev2;

source bin/activate;
cd /appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev2/PyDataFlow/PyDataFlow/pydataflow;
python manage.py runserver 10.236.211.34:8000 &
