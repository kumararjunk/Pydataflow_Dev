# # from __future__ import unicode_literals
import os
import pytz
from django.utils.timezone import activate
from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.db import models
#from django.urls import reverse
from multiselectfield import MultiSelectField
# from multiselect.fields import ManyToManyField
from django.utils import timezone


# to capture the history
# from simple_history.models import HistoricalRecords

# import django_tables2 as tables

# import table

DATABASE_TYPES = (('oracle', 'oracle'), ('sqlserver', 'sqlserver'),
                  ('teradata', 'teradata'), ('mysql', 'mysql'), )


Y_N = [("Y", "Y"), ("N", "N")]

DATABASE_OBJECT_TYPES = [("Table", "Table"), ("Stored_Proc",
                                              "Stored_Proc"), ("Shell_Script", "Shell_Script")]
JOB_TYPES = (
    ('Stored_Proc', 'Stored_Proc'),
    ('Table', 'Table'),
    ('Shell_Script', 'Shell_Script'),
)


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    project_name = models.CharField(max_length=50, unique=True)
    success_email = models.CharField(
        max_length=500, default='arjun.kumar@kp.org')
    failure_email_ind = models.BooleanField(default=False)
    failure_email = models.CharField(
        max_length=500, default='arjun.kumar@kp.org')
    is_active = models.CharField(max_length=1, choices=Y_N, default='Y')
    ## max_num_of_threads = models.SmallIntegerField(blank=False, null=False, default = 5)
    ## history = HistoricalRecords()

    def __str__(self):
        return self.project_name

    class Meta:
        ordering = ['project_name']


ROLE_TYPE = [("Master", "Master: Full Access"), ("Developer",
                                                 "Developer: Add/Edit jobs"), ("Operator", "Operator:Only Execute jobs")]


class Project_access(models.Model):
    project_name = models.ForeignKey(
        Project, on_delete=models.CASCADE, default=1)
    project_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='project_owner', default=1)
    project_owner_email = models.EmailField(blank=True, unique=False)
    requester = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='requester', default=1)
    requester_email = models.EmailField(blank=True, unique=False)
    notes = models.CharField(
        max_length=500, default='Need access to the project to make change and execute jobs')
    role = models.CharField(max_length=10, choices=ROLE_TYPE, default='Master')
    status = models.CharField(max_length=50, default='Pending')
    access = models.BooleanField(default=False)

    def __str__(self):
        return self.project_name

    # class Meta:
    ##     ordering = ('project_name')


class DataSource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    project_name = models.ForeignKey(
        Project, on_delete=models.CASCADE, default=1)
    dsn_name = models.CharField(max_length=50)
    db_host = models.CharField(max_length=100, default='127.0.0.1')
    db_user = models.CharField(max_length=50, blank=False)
    db_pw = models.CharField(max_length=50, blank=False)
    db_name = models.CharField(max_length=50, default='test_db')
    db_type = models.CharField(
        max_length=25, choices=DATABASE_TYPES, default='oracle')
    db_param = models.CharField(max_length=500, blank=True)
    db_port_no = models.IntegerField(default=3306)
    dsn_status = models.BooleanField(default=False)

    def __str__(self):
        return self.dsn_name

    class Meta:
        ordering = ['project_name', 'dsn_name']


class Spname(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    project_name = models.ForeignKey(
        Project, on_delete=models.CASCADE, default=1)
    dsn_name = models.ForeignKey(
        DataSource, on_delete=models.CASCADE, default=1)
    report_name = models.CharField(max_length=100)
    sp_name = models.CharField(max_length=100)
    start_dt = models.CharField(max_length=50, blank=True, default='NULL')
    end_dt = models.CharField(max_length=50, blank=True, default='NULL')
    med_center = models.CharField(max_length=100, blank=True, default='NULL')
    result_table = models.CharField(max_length=50)
    additional_param = models.CharField(
        max_length=400, blank=True, default='NULL')
    priority_id = models.SmallIntegerField(default=1)
    is_active = models.CharField(max_length=1, choices=Y_N, default='Y')
    job_type = models.CharField(
        max_length=25, choices=DATABASE_OBJECT_TYPES, default='Stored_Proc')


class Tbllist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    project_name = models.ForeignKey(
        Project, on_delete=models.CASCADE, default=1)
    dsn_name = models.ForeignKey(
        DataSource, on_delete=models.CASCADE, default=1)
    table_name = models.CharField(max_length=100)
    result_table = models.CharField(max_length=100)
    table_type = models.CharField(max_length=1, default='T')
    priority_id = models.SmallIntegerField(default=1)
    import_utility = models.CharField(max_length=50, default='sqoop')
    custom_cmd = models.CharField(max_length=500, blank=True)
    additional_param = models.CharField(max_length=400, blank=True)
    ## etl_sch_time = models.CharField(max_length=100)
    ## execution_flag = models.CharField(max_length=1, default='Y')
    is_active = models.CharField(max_length=1, choices=Y_N, default='Y')
    job_type = models.CharField(
        max_length=25, choices=DATABASE_OBJECT_TYPES, default='Table')

    def __unicode__(self):
        return self.table_name

    class Meta:
        ordering = ['project_name', 'dsn_name', 'table_name', 'table_type']


class Script(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    project_name = models.ForeignKey(
        Project, on_delete=models.CASCADE, default=1)
    job_name = models.CharField(max_length=100)
    script_path_name = models.CharField(max_length=500, blank=False)
    additional_param = models.CharField(max_length=500, blank=False)
    priority_id = models.SmallIntegerField(default=1)
    is_active = models.CharField(max_length=1, choices=Y_N, default='Y')
    job_type = models.CharField(
        max_length=25, choices=DATABASE_OBJECT_TYPES, default='Shell_Script')

    def __unicode__(self):
        return self.job_name

    class Meta:
        ordering = ['project_name', 'job_name', 'script_path_name']


class Jobflow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    project_name = models.ForeignKey(
        Project, on_delete=models.CASCADE, default=1)
    jobflowname = models.CharField(max_length=50, unique=True)
    max_num_of_threads = models.SmallIntegerField(
        blank=False, null=False, default=5)
    is_active = models.CharField(max_length=1, choices=Y_N, default='Y')

    def __unicode__(self):
        return self.jobflowname

    class Meta:
        ordering = ['jobflowname']


class Jobflowdetail(models.Model):
    jobflowname = models.ForeignKey(
        Jobflow, on_delete=models.CASCADE, default=1)
    project_job_name = models.CharField(
        max_length=50, blank=False, default='job_name_alias_name')
    job_name = models.CharField(max_length=50, blank=False, default='job_name')
    job_type = models.CharField(
        max_length=25, blank=False, default='Stored_Proc')
    object_id = models.IntegerField(default=1)
    additional_param = models.CharField(max_length=300, blank=True, default='')
    ## etl_sch_time = models.CharField(max_length=100, default='')
    priority_id = models.SmallIntegerField(default=1)
    is_active = models.CharField(max_length=1, choices=Y_N, default='Y')

    def __unicode__(self):
        return self.job_name

    class Meta:
        ##unique_together = ('jobflowname', 'job_name',)
        ordering = ['job_name']


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pydataflow.settings")
activate(settings.TIME_ZONE)


def get_time():
    # return timezone.localtime(timezone.now())
    activate(pytz.timezone('America/Los_Angeles'))
    return timezone.localtime(timezone.now()) - timezone.timedelta(minutes=420)


class Processlog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    project_name = models.ForeignKey(
        Project, on_delete=models.CASCADE, default=1)
    jobflowname = models.ForeignKey(
        Jobflow, on_delete=models.CASCADE, default=0)
    jobflowdetail = models.ForeignKey(
        Jobflowdetail, on_delete=models.CASCADE, default=0)
    project_job_name = models.CharField(
        max_length=50, blank=False, default='job_name_alias_name')
    process_id = models.IntegerField(default=1)
    job_name = models.CharField(max_length=50, blank=False, default='job_name')
    job_type = models.CharField(
        max_length=25, blank=False, default='Stored_Proc')
    object_id = models.IntegerField(default=1)
    additional_param = models.CharField(max_length=300, blank=True, default='')
    status = models.CharField(max_length=10, blank=True, default='Success')
    # , format="%Y.%m.%dT%H:%M:%S%z"
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(auto_now=True, null=True)
    logfile = models.CharField(max_length=500, blank=True, default='')
    log_url = models.CharField(max_length=100, blank=True, default='')
    pid = models.IntegerField(default=0)
    executed_job_names = models.CharField(
        max_length=800, blank=True, default='')
    execution_type = models.CharField(max_length=1, default='S')

    class Meta:
        ordering = ['process_id', 'status']


class Sch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    project_name = models.ForeignKey(
        Project, on_delete=models.CASCADE, default=1)
    jobflowname = models.ForeignKey(
        Jobflow, on_delete=models.CASCADE, default=0)
    jobflowdetail = models.ForeignKey(
        Jobflowdetail, on_delete=models.CASCADE, default=0)
    job_type = models.CharField(max_length=50, blank=False, default='Script')
    job_name = models.CharField(max_length=50, blank=False, default='Script')
    sch_type = models.IntegerField(default=0)
    create_time = models.DateTimeField(default=timezone.now)
    etl_sch_time = models.CharField(max_length=200, default='')
    delete_cron_url = models.CharField(
        max_length=100, default='/sch_delete_cron/0')
    failure_option = models.BooleanField(default=True)
    sla_long_running_job = models.IntegerField(default=0)

    class Meta:
        ordering = ['project_name', 'jobflowname', 'create_time']


# Env_variables -- > Env_variables_project

# global env variable
class Env_variables(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    project_name = models.ForeignKey(
        Project, on_delete=models.CASCADE, default=1)
    env_variable_name = models.CharField(max_length=100)
    env_variable_value = models.CharField(max_length=400)

    def __str__(self):
        return self.env_variable_name

    class Meta:
        ordering = ['env_variable_name']


class Env_variables_project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    project_name = models.ForeignKey(
        Project, on_delete=models.CASCADE, default=1)
    env_variable_name = models.CharField(max_length=100)
    env_variable_value = models.CharField(max_length=400)

    def __str__(self):
        return self.env_variable_name

    class Meta:
        ordering = ['project_name', 'env_variable_name']


class InitialTbllist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    project_name = models.ForeignKey(
        Project, on_delete=models.CASCADE, default=1)
    dsn_name = models.ForeignKey(
        DataSource, on_delete=models.CASCADE, default=1)
    table_names = models.CharField(max_length=100, default='')
    table_type = models.CharField(max_length=1, default='T')
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return self.table_names


class Person(models.Model):
    name = models.CharField('nome', max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField('telefone', max_length=11, null=True, blank=True)
    GENDER = (
        ('0', ''),
        ('man', 'homem'),
        ('woman', 'mulher'),
    )
    gender = models.CharField(
        'sexo',
        max_length=5,
        choices=GENDER,
        default='0'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'

    def __str__(self):
        return self.name

    def to_dict_json(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'gender': self.get_gender_display(),
        }


# - Add field execution_type to processlog
# - Alter field db_param on datasource
# - Alter field db_port_no on datasource
# - Alter field executed_job_names on processlog
# - Alter field notes on project_access
# - Alter field etl_sch_time on sch
# - Alter field additional_param on script
# - Alter field script_path_name on script
