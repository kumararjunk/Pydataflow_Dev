keep only create_log_file from meta.utils and remove it from script.utils




changed meta.forms ProjectSpForm added self.fields to show the DATE format and NULL

from meta.models import Processlog

p = Processlog.objects.get(pk=38413)
p.status

p.status = 'Killed'
p.save()






p = Processlog.objects.get(pk=38477)
p.status = 'Failed'
p.save()


p = Processlog.objects.get(pk=38548)
p.status = 'Failed1'
p.save()



Model update without accessing.
Article.objects.filter(pk=1).update(title="New Title")

# test 3066

/appdata/middleware/td2ex-dev-staging/front_end/pydataflow_local/PyDataFlow/PyDataFlow

# from meta.models import Person
# Person.objects.bulk_create([Person(name='Arjun'), Person(name='Kumar')])
# kill $(ps -ef | grep 8080| awk '{print $2}')
# lsof -P | grep ':8000' | awk '{print $2}' | xargs kill -9

# rilis_server_host="10.236.192.51:49172"
# rilis_server_user=K390239
# rilis_server_pw=K390239sql
# rilis_database=tat

# from subprocess import Popen,PIPE
# DATABASE_TYPES = ['oracle', 'sqlserver', 'teradata', 'mysql']
# IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# mysql_conn_dict = {'db_host': "127.0.0.1", 'db_user': "azkaban", 'db_pw': "BigData1@", 'db_name': "azkaban"}


#!/bin/sh

find . -name '*.pyc' -delete

find /Users/arjunkumar/Desktop/notes2/pre-prod/front_end/PyDataFlow_Local/PyDataFlow/pydataflow_local -name '*.pyc' -delete
find /Users/arjunkumar/Desktop/notes2/pre-prod/front_end/PyDataFlow_Local/PyDataFlow/pydataflow -name '*.pyc' -delete



find . -name '*pydataflow.log'


lsof -n -i:8000 | grep LISTEN | awk '{print $2}' | xargs kill -9



import sqlite3
conn = sqlite3.connect('/appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev2/PyDataFlow/PyDataFlow/pydataflow/db.sqlite3', isolation_level=None)
conn.execute("VACUUM")
conn.close()





import sqlite3
conn = sqlite3.connect('/appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev2/PyDataFlow/PyDataFlow/pydataflow/db.sqlite3', isolation_level=None)
conn.execute("VACUUM")
conn.close()





cd /appdata/middleware/td2ex-dev-staging/front_end/pydataflow_local;
source bin/activate;

cd /appdata/middleware/td2ex-dev-staging/front_end/pydataflow_local/PyDataFlow/PyDataFlow/pydataflow/
python manage.py runserver ttgbk-pp-hadp-3.ttgtpmg.net:8000 &


## get all the objects from sqlite db
SELECT name FROM sqlite_master
WHERE type ='table' AND name NOT LIKE 'sqlite_%';



firstdict = {'cat' : 'animal', 'blue' : 'colour', 'sun' : 'star', 'name': 'bob', 'shape': 'circle'}
seconddict = {'cat' : 'pet', 'blue' : 'colour', 'earth' : 'star', 'name': 'steve', 'shape': 'square'}


def compare(first, second):
    sharedKeys = set(first.keys()).intersection(second.keys())
    for key in sharedKeys:
        if first[key] != second[key]:
            print('Key: {}, Value 1: {}, Value 2: {}'.format(key, first[key], second[key]))

compare(firstdict, seconddict)
#Key: cat, Value 1: animal, Value 2: pet


user,timestamp_change, object_type, object_id,field_name, before_change, after_change
1 , 2020-01-01, Project, 1, project_name, p1, p2 | revert back



===

rltg adding in report fulfillers

Order Placed:
10-28-2020 16:19:34
Request Number:
REQ0065695
RITM0066143
