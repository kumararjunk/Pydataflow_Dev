#!/bin/sh

cd /appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev
source bin/activate;

pip freeze

comm='/appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev/bin/python /appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev/PyDataFlow/PyDataFlow/pydataflow/core/core.py 1 0'

$comm


# export PYTHONPATH=/appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev/PyDataFlow/PyDataFlow/pydataflow/pydataflow

# export DJANGO_SETTINGS_MODULE=settings

# export DJANGO_SETTINGS_MODULE=pydataflow.settings
# /appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev/bin/python /appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev/PyDataFlow/PyDataFlow/pydataflow/pydataflow/settings.py
# export DJANGO_SETTINGS_MODULE=pydataflow.settings

# echo $DJANGO_SETTINGS_MODULE

# comm='/appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev/bin/python /appdata/middleware/td2ex-dev-staging/front_end/pydataflow_dev/PyDataFlow/PyDataFlow/pydataflow/core/core.py 1 0'
