from django.shortcuts import redirect
import csv
# import MySQLdb,
import multiprocessing
from multiprocessing import Semaphore
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
# CreateView, DeleteView, ListView, DetailView
from django.views.generic import UpdateView

from .forms import Choose_dsn_Form, databaseObjectForm, DsnCreateForm
# , EnvVariablesFormSet
from .forms import DataSourceForm, ProjectDataSourceFormSet, ProjectEnvProjectForm
from .forms import ProjectForm, ProjectSpFormSet, SpFormupdate, SpCreateForm
from .models import Project, DataSource, Spname, Script
from .models import Tbllist, InitialTbllist, Jobflow, Jobflowdetail

from .utils import *
from scripts.utils import exe_script_util
import datetime
from django.utils import timezone

import json
from django.db import connection
from operator import attrgetter
from itertools import chain
from .serializers import ProjectJobflowdetailSerializer, ProjectSpnameSerializer
# from .serializers import ProjectHistorySerializer
from rest_framework import routers, serializers, viewsets
from django.shortcuts import redirect
from django.forms.models import model_to_dict

DATABASE_OBJECT_DICT = {'T': "Tables", 'V': "Views", 'S': "Stored_Proc"}


def advance_search(request):
    return render(request, 'meta/advance_search.html')

# projecspnameobjects


def projecspnameobjects(request):
    return render(request, 'meta/projecspnametobjects.html')
    # <li class=""><a href="{% url 'meta:projecspnameobjects' %}"><span aria-hidden="true"></span>&nbsp; Advance Search SP</a> </li>


def get_projecspnameobjects_options():
    return "options", {
        "jobflow": [{'label': obj.jobflowname, 'value': obj.pk} for obj in Jobflow.objects.all()],
        "jobflowdetail": [{'label': obj.project_job_name, 'value': obj.pk} for obj in Jobflowdetail.objects.all()]
    }


class ProjectSpnameViewSet(viewsets.ModelViewSet):
    # queryset = Jobflowdetail.objects.all().order_by('jobflowname')  # .reverse()
    queryset = Spname.objects.all().select_related(
        'project_name').order_by('project_name')
    serializer_class = ProjectSpnameSerializer

    def get_options(self):
        return get_projecspnameobjects_options()

    class Meta:
        datatables_extra_json = ('get_options', )


# projecjobflowdetailtobjects
def projecjobflowdetailtobjects(request):
    return render(request, 'meta/projecjobflowdetailtobjects.html')
    #  <li class=""><a href="{% url 'meta:projecjobflowdetailtobjects' %}"><span aria-hidden="true"></span>&nbsp; Search All Jobflowdetail</a> </li>


def get_projectjobflowdetailobjects_options():
    return "options", {

        "jobflow": [{'label': obj.jobflowname, 'value': obj.pk} for obj in Jobflow.objects.all()],
        "jobflowdetail": [{'label': obj.project_job_name, 'value': obj.pk} for obj in Jobflowdetail.objects.all()]
    }


class ProjectJobflowdetailViewSet(viewsets.ModelViewSet):
    # queryset = Processlog.objects.filter(job_type="Job Flow").order_by('id').reverse()
    queryset = Jobflowdetail.objects.all().order_by('jobflowname')  # .reverse()
    serializer_class = ProjectJobflowdetailSerializer

    def get_options(self):
        return get_projectjobflowdetailobjects_options()

    class Meta:
        datatables_extra_json = ('get_options', )

##############


def select_dsn1(request, project_id):
    project = Project.objects.get(id=project_id)
    dsn_form = Choose_dsn_Form(request.POST or None,
                               initial={'project': project, 'project_id': project_id})
    database_object_form = databaseObjectForm(request.POST or None)
    return render(request, 'meta/select_dsn.html',
                  {'project': project, 'dsn_form': dsn_form, 'database_object_form': database_object_form})


def profile_setting1(request, project_id):
    print("common profile setting project id")
    project = get_object_or_404(Project, pk=project_id)
    dsn_form = Choose_dsn_Form(request.POST or None, initial={
                               'project': project, 'project_id': project_id})
    # database_object_form = databaseObjectForm(request.POST or None)
    return render(request, 'common/profile_setting.html', {'project': project})

#########################import raw tables  view ######################


def select_src_tables(request, project_id):
    print('meta:view:select_src_tables', 'project_id:', project_id)
    project = get_object_or_404(Project, pk=project_id)
    project_d = Project.objects.get(pk=project_id).__dict__
    project_id = project_d['id']
    request.session['project_id'] = project_id
    current_user = request.user
    user_id = current_user.id
    # getting the dsn name from form/html & #Geting the dsn_id from
    dsn_name = request.POST.get('dsn_name')

    if dsn_name is None:
        dsn_name = request.session['dsn_name']
    else:
        request.session['dsn_name'] = dsn_name

    dsn_id = [d.id for d in DataSource.objects.filter(
        dsn_name__exact=dsn_name, project_name_id__exact=project_id)][0]

    request.session['dsn_id'] = dsn_id
    dsn_details = DataSource.objects.get(pk=dsn_id).__dict__

    print("Trying to connect database with,dsn_details:", dsn_details)
    db_object_type = request.POST.get('db_object_type')

    if db_object_type is None:
        db_object_type = request.session['db_object_type']
    else:
        request.session['db_object_type'] = db_object_type

    request.session['project_id'] = project_id
    dsn_details['db_object_type'] = db_object_type

    all_initial_tables = InitialTbllist.objects.filter(user_id=request.user).filter(
        project_name_id=project_id).filter(dsn_name_id=dsn_id).filter(table_type=db_object_type)
    existing_table_list = Tbllist.objects.filter(user_id=request.user).filter(
        project_name_id=project_id).filter(dsn_name_id=dsn_id).filter(table_type=db_object_type)

    # for table in existing_table_list:
    #     print(table.table_name)
    # remove duplicate items from list
    # mylist = list(dict.fromkeys(mylist))

    if 'new_tbls' in request.POST and len(request.POST.getlist('new_tbls')) > 0:
        # import raw tables
        new_tbl_raw = request.POST.getlist('new_tbls', default=None)

        existing_table_list_all = []
        for tbllist in existing_table_list:
            existing_table_list_all.append(tbllist.table_name)

        new_tbl_raw = [(table_name, table_name, db_object_type, 'sqoop', '', '', '',
                        'N', dsn_id, project_id, user_id, 1)
                       for table_name in new_tbl_raw if table_name
                       not in existing_table_list_all]

        sqlite_conn = sqlite_db_connection()
        cur_sqlite = sqlite_conn.cursor()

        # convert to orm:
        insert_statement = ("INSERT INTO meta_Tbllist (table_name, result_table, table_type, import_utility, custom_cmd, additional_param, is_active, dsn_name_id, project_name_id, user_id, priority_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);")
        print('meta:view:select_src_tables:Inserting data into sqlite db',
              'insert_statement:', insert_statement)
        cur_sqlite.executemany(insert_statement, new_tbl_raw)
        sqlite_conn.commit()
        sqlite_conn.close()
        # refreshing the table list and redirecting the page:
        existing_table_list = Tbllist.objects.filter(user_id=request.user).filter(
            project_name_id=project_id).filter(dsn_name_id=dsn_id).filter(table_type=db_object_type)
        return render(request, 'meta/select_src_tables.html', {'project': project, 'all_initial_tables': all_initial_tables, 'existing_table_list': existing_table_list})

    elif 'delete_tble_list[]' in request.POST and len(request.POST.getlist('delete_tble_list[]')) > 0:

        # delete_tble_list = tuple(request.POST.getlist('delete_tble_list[]',default=None))
        delete_tble_list = request.POST.getlist(
            'delete_tble_list[]', default=None)
        db_object_type_str = "'" + db_object_type + "'"
        sqlite_conn = sqlite_db_connection()
        delete_stmt = "Delete from meta_Tbllist where project_name_id = {} and dsn_name_id = {} \
                      and table_type = {} and table_name in (%s)\
                     ".format(project_id, dsn_id, db_object_type_str)

        query_string = delete_stmt % ','.join(['?'] * len(delete_tble_list))
        sqlite_conn.execute(query_string, delete_tble_list)
        print('meta:view:select_src_tables:delete_tble_list[]',
              'delete_stmt:', delete_stmt)
        sqlite_conn.commit()
        sqlite_conn.close()
        # refreshing the table list and redirecting the page:
        existing_table_list = Tbllist.objects.filter(user_id=request.user).filter(
            project_name_id=project_id).filter(dsn_name_id=dsn_id).filter(table_type=db_object_type)
        return render(request, 'meta/select_src_tables.html', {'project': project, 'all_initial_tables': all_initial_tables, 'existing_table_list': existing_table_list})

    else:
        pass

    dsn_conn = test_dsn_generic(**dsn_details)
    if dsn_conn[1] == 'success':
        # importing the tables using the DSN.
        get_data_using_dsn_generic_util(**dsn_details)
        tables_count = InitialTbllist.objects.filter(user_id=request.user).filter(
            project_name_id=project_id).filter(dsn_name_id=dsn_id).filter(table_type=db_object_type).count()

        if tables_count == 0:
            error_message = 'No ' + \
                DATABASE_OBJECT_DICT[db_object_type] + \
                ' in Database: ' + dsn_details['db_name']
            messages.info(request, error_message)
            return render(request, 'meta/select_src_tables.html', {'project': project, 'all_initial_tables': all_initial_tables, 'existing_table_list': existing_table_list})
        else:
            return render(request, 'meta/select_src_tables.html', {'project': project, 'all_initial_tables': all_initial_tables, 'existing_table_list': existing_table_list})
    else:
        error_message = 'Error Connecting Rdbms using DSN: ' + \
            dsn_name + ' Detailed Error Msg: ' + str(dsn_conn[2])
        # return JsonResponse({'Failure': error_message})
        messages.info(request, error_message)
        return redirect('meta:select_dsn', project_id=project_id)


def select_dsn(request, project_id):
    project = Project.objects.get(id=project_id)
    dsn_form = Choose_dsn_Form(request.POST or None, initial={
                               'project': project, 'project_id': project_id})
    database_object_form = databaseObjectForm(request.POST or None)
    return render(request, 'meta/select_dsn.html', {'project': project, 'dsn_form': dsn_form, 'database_object_form': database_object_form})


def favorite(request, datasource_id):
    datasource = get_object_or_404(DataSource, pk=datasource_id)
    try:
        if datasource.dsn_status:
            datasource.dsn_status = False
            print("datasource was favorite, making it unfavorite", datasource_id)
        else:
            datasource.dsn_status = True
            print("datasource was unfavorite, making it favorite", datasource_id)
        datasource.save()
    except (KeyError, DataSource.DoesNotExist):
        # return JsonResponse({'success': False})
        # return render(request, 'music/detail.html', {'album': album})
        return HttpResponseRedirect(request.path_info)
    else:
        # return JsonResponse({'success': True})
        # return render(request, 'music/detail.html', {'album': album})
        return HttpResponseRedirect(request.path_info)
#########################DSN view views######################


def DsnTest(request, project_id):
    # project = get_object_or_404(Project, pk=project_id)
    project_d = Project.objects.get(pk=project_id).__dict__
    project_name_id = project_d['id']
    project = Project.objects.get(id=project_id)
    form = myForm2(request.POST or None, initial={
                   'project': project, 'project_id': project_id})
    # form = myForm2(initial={'project_name_id':project_name_id})
    return render(request, 'meta/project_dsn_list_tmp2.html', {'project': project, 'form': form, 'project_name_id': project_name_id})


class DsnUpdate(UpdateView):
    model = DataSource
    form_class = DataSourceForm
    pk_url_kwarg = "datasource_id"
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    template_name = 'meta/dsn_update.html'
    # success_url = reverse_lazy('meta:index')

    def get_success_url(self):
        # datasource_id = self.object.id
        datasource_as_dict = DataSource.objects.get(pk=self.object.id).__dict__
        project_name_id = datasource_as_dict['project_name_id']
        return reverse_lazy('meta:dsn_view',
                            kwargs={'project_id': project_name_id})


class DsnBulkUpdate(UpdateView):
    pk_url_kwarg = "project_id"
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True

    model = Project
    fields = ['project_name']
    template_name = 'meta/project_dsn_update.html'

    def get_success_url(self):
        return reverse_lazy('meta:dsn_view', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        data = super(DsnBulkUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['datasources'] = ProjectDataSourceFormSet(
                self.request.POST, instance=self.object)
        else:
            data['datasources'] = ProjectDataSourceFormSet(
                instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        datasources = context['datasources']
        with transaction.atomic():
            self.object = form.save()

            if datasources.is_valid():
                datasources.instance = self.object
                datasources.save()
        return super(DsnBulkUpdate, self).form_valid(form)


@login_required
def del_dsn(request, project_id, datasource_id):
    project = get_object_or_404(Project, pk=project_id)
    datasource = DataSource.objects.get(pk=datasource_id)
    datasource.delete()
    return render(request, 'meta/dsn_delete_list.html', {'project': project})


@login_required
def del_dsn_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'meta/dsn_delete_list.html', {'project': project})


def dsn_add(request, project_id):
    print('meta:view:dsn_add:', 'project_id:', project_id)
    project = get_object_or_404(Project, pk=project_id)
    project_id = int(project_id)
    print("project:", project, "project_id:", project_id)
    form = DsnCreateForm(request.POST or None, initial={
                         'project_id': project_id})
    if form.is_valid():
        # projects_dsn = project.dataSource_set.all()
        projects_dsn = DataSource.objects.filter(
            user_id=request.user).filter(project_name_id=project_id)
        for s in projects_dsn:
            if s.dsn_name == form.cleaned_data.get("dsn_name"):
                context = {
                    'project': project,
                    'form': form,
                    'error_message': 'You already added dsn_name in project',
                }
                return render(request, 'meta/add_dsn.html', context)
        dsnlist = form.save(commit=False)
        # dsnlist.project = project
        dsnlist.project_name = project
        dsnlist.save()
        return render(request, 'meta/project_dsn_view.html', {'project': project})
    context = {
        'project': project,
        'form': form,
    }
    return render(request, 'meta/add_dsn.html', context)


def DsnView(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'meta/project_dsn_view.html', {'project': project})


#############execute job flow  #############


def child_process_execute_jobs(user, process_id, jobflowdetail_id, project_d):
    time.sleep(1)
    exec_parallel_ind = {"ind": True}
    Jobflowdetail_d = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__
    job_type = Jobflowdetail_d['job_type']
    object_id = Jobflowdetail_d['object_id']
    execution_type = 'jobflow'

    if job_type == 'Stored_Proc':
        print('meta:view:child_process:Executing Stored_Proc', 'process_id:',
              process_id, 'jobflowdetail_id:', jobflowdetail_id, 'project_d:', project_d)
        spname_d = Spname.objects.get(pk=object_id).__dict__
        project_spname_all_d = {**project_d, **spname_d, **exec_parallel_ind}
        project_spname_all_d['jobflowdetail_id'] = jobflowdetail_id
        project_spname_all_d['job_name'] = project_spname_all_d['report_name']
        exe_sp_util(execution_type, process_id, **project_spname_all_d)

    elif job_type == 'Shell_Script':
        script_d = Script.objects.get(pk=object_id).__dict__
        print('meta:view:child_process:Executing Shell_Script', 'process_id:',
              process_id, 'jobflowdetail_id:', jobflowdetail_id, 'script_d:', script_d)
        exe_script_util(execution_type, user, process_id,
                        jobflowdetail_id, **script_d)

    elif job_type == 'Table':
        print("Executing Table:", job_type, id)
        pass


def child_process(user, process_id, jobflowdetail_id, sema, project_d):
    time.sleep(1)
    sema.acquire()

    child_process_execute_jobs_process = multiprocessing.Process(
        target=child_process_execute_jobs, args=(user, process_id, jobflowdetail_id, project_d))
    child_process_execute_jobs_process.daemon = True
    child_process_execute_jobs_process.start()
    child_process_execute_jobs_process.join(10800)
    # child_process_execute_jobs_process.join(5)

    # If thread is still active
    if child_process_execute_jobs_process.is_alive():
        print("Job is running more then 3 hours:", 'process_id:', process_id)
        # worker_proces_bridge.terminate()
        Jobflowdetail_d = Jobflowdetail.objects.get(
            pk=jobflowdetail_id).__dict__
        msg = 'Job is running more then 3 hours: ' + str(process_id)

        email_notification_logrunning_job(
            msg, process_id=process_id, **Jobflowdetail_d)
        child_process_execute_jobs_process.join()
    else:
        child_process_execute_jobs_process.join()

    sema.release()


def child_process_monitor(user, rerun_flag, process_id, jobflow_pk, jobflow_id, project_id, project_d):
    time.sleep(.5)
    print('meta:view:child_process_monitor:', 'user:', user, 'rerun_flag:', rerun_flag, 'process_id:',
          process_id, 'jobflow_id:', jobflow_id, 'project_id:', project_id, 'project_d:', project_d)
    jobflow_d = Jobflow.objects.get(pk=jobflow_id).__dict__
    ### max_limit = num_of_active_thread + max_limit
    #max_limit = get_job_flow_max_limit(jobflow_id)
    max_limit = jobflow_d['max_num_of_threads']
    sema = Semaphore(max_limit)
    # num_of_active_thread = threading.activeCount()
    num_of_active_thread = Processlog.objects.filter(process_id=process_id).filter(
        jobflowname=jobflow_id).filter(status='Executing').count()
    threads = []
    priority_id_list = Jobflowdetail.objects.filter(jobflowname=jobflow_id).filter(
        is_active='Y').order_by('priority_id').values_list('priority_id', flat=True).distinct()[::1]

    for priority_id in priority_id_list:
        time.sleep(2)

        all_jobflowdetail_ids = Jobflowdetail.objects.filter(jobflowname=jobflow_id).filter(is_active='Y').filter(
            priority_id=priority_id).order_by('id').order_by('priority_id').values_list('id', flat=True)[::1]
        print('meta:view:child_process_monitor:', 'submiting jobflowname:', jobflow_d['jobflowname'], 'process_id:', process_id,
              'project_id:', project_id, 'jobflow_id:', jobflow_id, 'all_jobflowdetail_ids:', all_jobflowdetail_ids, type(all_jobflowdetail_ids))

        for jobflowdetail_id in all_jobflowdetail_ids:
            time.sleep(1)

            jobflowdetail_id_obj = Jobflowdetail.objects.get(
                id=jobflowdetail_id)

            if rerun_flag:
                jobdetail_succes_status = Processlog.objects.filter(process_id=process_id).filter(
                    jobflowdetail=jobflowdetail_id_obj).filter(status='Success').exists()
                if jobdetail_succes_status:
                    continue

                else:
                    while num_of_active_thread > max_limit:
                        time.sleep(2)
                        num_of_active_thread = Processlog.objects.filter(
                            jobflowname=jobflow_id).filter(status='Executing').count()

                    time.sleep(1)
                    job_process = multiprocessing.Process(target=child_process, args=(
                        user, process_id, jobflowdetail_id, sema, project_d))
                    threads.append(job_process)
                    job_process.start()

            else:
                time.sleep(1)
                any_job_fail = Processlog.objects.filter(
                    process_id=process_id).filter(status='Failed').exists()

                if any_job_fail:
                    print(
                        'Some job have failed and exiting the process, please check the detailed log:', )

                    for all_process in threads:
                        all_process.join()
                    return 9

                while num_of_active_thread > max_limit:
                    time.sleep(1)
                    num_of_active_thread = Processlog.objects.filter(
                        jobflowname=jobflow_id).filter(status='Executing').count()

                job_process = multiprocessing.Process(target=child_process, args=(
                    user, process_id, jobflowdetail_id, sema, project_d))
                threads.append(job_process)
                job_process.start()

        for all_process in threads:  # Wait for all of them to finish
            time.sleep(1)
            print(
                'Waiting for all the job in jobflow to complete, with priority id:', priority_id)
            print(user, rerun_flag, process_id,
                  jobflow_id, project_id, project_d)
            all_process.join()
            time.sleep(1)

            # any_job_fail = Processlog.objects.filter(process_id = process_id).filter(status='Failed').exists()
            # if any_job_fail:
            #     print('from if any_job_fail:', any_job_fail)
            #     # break;
            #     pass
            # else:
            #     print('from if else:', any_job_fail)


def exe_jobflow_process(user, rerun_flag, process_id, jobflow_pk, jobflow_id, project_id, project_d):
    time.sleep(1)
    print('meta:view:exe_jobflow_process:', 'process_id:', process_id,
          'project_id:', project_id, 'jobflow_id:', jobflow_id)
    new_process = multiprocessing.Process(target=child_process_monitor, args=(
        user, rerun_flag, process_id, jobflow_pk, jobflow_id, project_id, project_d))
    new_process.start()
    new_process.join()
    time.sleep(1)
    check_flow_status_send_email(process_id, jobflow_pk, jobflow_id)


def check_flow_status_send_email(process_id, jobflow_pk, jobflow_id):
    time.sleep(1)
    # jobflow_d = Jobflow.objects.get(pk=jobflow_id).__dict__
    # tables_count = InitialTbllist.objects.filter(user_id=request.user).filter(project_name_id=project_id).filter(dsn_name_id = dsn_id).filter(table_type = db_object_type).count()
    processlog_job_names_success = Processlog.objects.filter(process_id=process_id).filter(jobflowname=jobflow_id).filter(
        status='Success').exclude(job_name='Job Flow').values_list('job_name', flat=True).distinct()[::1]  # .count()   #
    processlog_job_names_success.sort()

    jobflow_names_is_active_all = []
    priority_id_list = Jobflowdetail.objects.filter(jobflowname=jobflow_id).filter(
        is_active='Y').order_by('priority_id').values_list('priority_id', flat=True).distinct()[::1]

    for priority_id in priority_id_list:
        time.sleep(.5)
        jobflow_names_is_active_priority_id = Jobflowdetail.objects.filter(jobflowname=jobflow_id).filter(is_active='Y').filter(
            priority_id=priority_id).order_by('id').order_by('priority_id').values_list('job_name', flat=True)[::1]
        jobflow_names_is_active_all.extend(jobflow_names_is_active_priority_id)

    jobflow_names_is_active_all.sort()

    last_start_time = Processlog.objects.filter(process_id=process_id).filter(
        job_name='Job Flow').order_by('-start_time').first().start_time
    # geting objects from the process log which ran after the last ran
    # x = Processlog.objects.filter(process_id=process_id, start_time__gte = last_start_time).exclude(job_name='Job Flow')

    if processlog_job_names_success == jobflow_names_is_active_all:
        job_success_count_match = True

    else:
        job_success_count_match = False
        job_not_ran = list(set(jobflow_names_is_active_all)
                           ^ set(processlog_job_names_success))

    if job_success_count_match:

        job_status = 'Success'
        processlog_update_status_util(job_status, jobflow_pk)
        print('check_flow_status_send_email', job_status)
        job_names_list = Processlog.objects.filter(process_id=process_id).filter(
            jobflowname=jobflow_id).exclude(job_name='Job Flow').values_list('job_name', flat=True).distinct()[::1]
        job_names_list = list(set(job_names_list))
        job_names_str = job_names_list[0]

        for i in range(len(job_names_list) - 1):
            job_names_str = job_names_str + ", " + job_names_list[i + 1]
        email_notification_jobflow(
            msg=job_status, failed_killed_jobnames=job_names_str, process_id=process_id, jobflow_id=jobflow_id)
        return 0

    # elif Processlog.objects.filter(process_id=process_id).filter(jobflowname=jobflow_id).filter(status='Killed').exists():
    elif Processlog.objects.filter(process_id=process_id, start_time__gte=last_start_time).filter(status='Killed').exists():
        print('meta:view:check_flow_status_send_email:Killed',
              'process_id:', process_id)
        job_status = 'Killed'
        processlog_update_status_util(job_status, jobflow_pk)
        print('check_flow_status_send_email',)
        job_names_list = Processlog.objects.filter(process_id=process_id).filter(jobflowname=jobflow_id).exclude(
            job_name='Job Flow').exclude(status='Success').values_list('job_name', flat=True)[::1]
        job_names_str = job_names_list[0]

        for i in range(len(job_names_list) - 1):
            job_names_str = job_names_str + ", " + job_names_list[i + 1]

        email_notification_jobflow(
            msg=job_status, failed_killed_jobnames=job_names_str, process_id=process_id, jobflow_id=jobflow_id)
        # return 1

    # elif Processlog.objects.filter(process_id=process_id).filter(jobflowname=jobflow_id).filter(status='Failed').exists():
    elif Processlog.objects.filter(process_id=process_id, start_time__gte=last_start_time).filter(status='Failed').exists():
        print('meta:view:check_flow_status_send_email:Failed',
              'process_id:', process_id)
        job_status = 'Failed'
        processlog_update_status_util(job_status, jobflow_pk)
        print('check_flow_status_send_email',)

        job_names_list = Processlog.objects.filter(process_id=process_id).filter(jobflowname=jobflow_id).filter(
            status='Failed').exclude(job_name='Job Flow').exclude(status='Success').values_list('job_name', flat=True).distinct()[::1]
        job_names_str = job_names_list[0]

        for i in range(len(job_names_list) - 1):
            job_names_str = job_names_str + ", " + job_names_list[i + 1]

        email_notification_jobflow(
            msg=job_status, failed_killed_jobnames=job_names_str, process_id=process_id, jobflow_id=jobflow_id)
        # return 2

    elif not job_success_count_match:
        processlog_update_status_util(
            'In-Complete Run', jobflow_process_log_id)
        job_status = 'In-Complete Run'
        processlog_update_status_util(job_status, jobflow_pk)
        print('check_flow_status_send_email In-Complete Run', job_status)
        # job_names_list = Processlog.objects.filter(process_id=process_id).filter(
        #     jobflowname=jobflow_id).exclude(job_name='Job Flow').values_list('job_name', flat=True)[::1]
        # job_names_str = job_names_list[0]
        job_names_str = job_not_ran

        for i in range(len(job_names_list) - 1):
            job_names_str = job_names_str + ", " + job_names_list[i + 1]

        email_notification_jobflow(
            msg=job_status, failed_killed_jobnames=job_names_str, process_id=process_id, jobflow_id=jobflow_id)
        return 0


def exe_jobflow(request, project_id, jobflow_id):
    print('meta:view:exe_jobflow:', 'project_id:',
          project_id, 'jobflow_id:', jobflow_id)
    user = request.user
    rerun_flag = False
    # project = get_object_or_404(Project, pk=project_id)
    project_d = Project.objects.get(pk=project_id).__dict__
    jobflow_d = Jobflow.objects.get(pk=jobflow_id).__dict__
    project = get_object_or_404(Project, pk=project_id)
    jobflow = get_object_or_404(Jobflow, pk=jobflow_id)
    template_name = 'scripts/jobflow_detail.html'

    if project_d['is_active'] != 'Y':  # checking if the project is active
        error_message = 'Project:' + \
            project_d['project_name'] + ' is Not Active'
        messages.info(request, error_message)
        # return redirect('sch:sch_main_view', project_id=project_id, jobflow_id=jobflow_id)
        return redirect('scripts:jobflowdetail', jobflow_id=jobflow_id)

    if jobflow_d['is_active'] != 'Y':  # checking if the jobflow is active
        error_message = 'Jobflow:' + \
            jobflow_d['jobflowname'] + ' is Not Active'
        messages.info(request, error_message)
        # return redirect('sch:sch_main_view', project_id=project_id, jobflow_id=jobflow_id)
        return redirect('scripts:jobflowdetail', jobflow_id=jobflow_id)

    jobflowdetail_id = Jobflowdetail.objects.filter(
        jobflowname=jobflow_id).filter(is_active='Y').values()[0]['id']

    process_id, jobflow_pk = processlog_create_jobflow_util(
        jobflowdetail_id, 'M')

    print('Executing the jobflow with process id',
          process_id, 'jobflow_process_log_id', 'M')
    jobflow_worker_process = multiprocessing.Process(target=exe_jobflow_process, args=(
        user, rerun_flag, process_id, jobflow_pk, jobflow_id, project_id, project_d))
    jobflow_worker_process.start()
    print('meta:view:exe_jobflow: process_id, jobflow_pk, jobflow_worker_process.pid',
          process_id, jobflow_pk, jobflow_worker_process.pid)
    processlog_update_pid_util(
        jobflow_pk, jobflow_worker_process.pid)

    error_message = 'Job flow: ' + \
        str(jobflow_d['jobflowname']) + \
        ', Submited, Process id:' + str(process_id)
    messages.info(request, error_message)

    return redirect('scripts:jobflowdetail', jobflow_id=jobflow_id)

#####end of execute job flow ######
def exe_jobs_worker_process(user, rerun_flag, process_id, jobflow_pk, job_type, jobflowdetail_id, object_id, project_d):
    time.sleep(.5)
    exec_parallel_ind = {"ind": True}
    #execution_type = 'single_job'
    jobflowdetail_d = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__
    jobflow_id = jobflowdetail_d['jobflowname_id']
    execution_type = Processlog.objects.filter(process_id=process_id).filter(
        jobflowname=jobflow_id).filter(job_type='Job Flow').values_list('execution_type', flat=True)[::1][0]

    if job_type == 'Stored_Proc':
        print('meta:view:exe_jobs: executing Stored_Proc')
        spname_d = Spname.objects.get(pk=object_id).__dict__
        project_spname_all_d = {**project_d, **spname_d, **exec_parallel_ind}
        project_spname_all_d['jobflowdetail_id'] = jobflowdetail_id
        project_spname_all_d['job_name'] = project_spname_all_d['report_name']
        exe_sp_util(execution_type, process_id, **project_spname_all_d)

    if job_type == 'Shell_Script':
        script_d = Script.objects.get(pk=object_id).__dict__
        exe_script_util(execution_type, user, process_id,
                        jobflowdetail_id, **script_d)

    if job_type == 'Table':
        ### table_d = Tbllist.objects.get(pk=object_id).__dict__
        print('meta:exe_jobs: executing Table')

    time.sleep(1)

    if execution_type == 'S':
        update_jobflow_single_job_executed(
            rerun_flag, execution_type, process_id, jobflow_id, jobflowdetail_id, jobflow_pk)

    if execution_type == 'M':
        update_jobflow_if_multiple_job_execute_before(
            rerun_flag, execution_type, process_id, jobflow_id, jobflowdetail_id, jobflow_pk)


def update_jobflow_if_multiple_job_execute_before(rerun_flag, execution_type, process_id, jobflow_id, jobflowdetail_id, jobflow_pk):
    print('update_jobflow_if_multiple_job_execute'*10)
    processlog_job_names_success = Processlog.objects.filter(process_id=process_id).filter(jobflowname=jobflow_id).filter(
        status='Success').exclude(job_name='Job Flow').values_list('job_name', flat=True).distinct()[::1]  # .count()   #
    processlog_job_names_success.sort()

    jobflow_names_is_active_all = []
    priority_id_list = Jobflowdetail.objects.filter(jobflowname=jobflow_id).filter(
        is_active='Y').order_by('priority_id').values_list('priority_id', flat=True).distinct()[::1]

    for priority_id in priority_id_list:
        time.sleep(.2)
        jobflow_names_is_active_priority_id = Jobflowdetail.objects.filter(jobflowname=jobflow_id).filter(is_active='Y').filter(
            priority_id=priority_id).order_by('id').order_by('priority_id').values_list('job_name', flat=True)[::1]
        jobflow_names_is_active_all.extend(jobflow_names_is_active_priority_id)

    jobflow_names_is_active_all.sort()

    if processlog_job_names_success == jobflow_names_is_active_all:
        job_success_count_match = True
    else:
        job_success_count_match = False

    last_run_status = Processlog.objects.filter(process_id=process_id).filter(jobflowname=jobflow_id).filter(
        jobflowdetail=jobflowdetail_id).exclude(job_name='Job Flow').order_by('-id').values_list('status', flat=True)[::1][0]

    if last_run_status == 'Success':
        # print('*Success'*100)
        # print('jobflow_names_is_active_all', jobflow_names_is_active_all)
        # job_names_list = Processlog.objects.filter(process_id = process_id).filter(jobflowname=jobflow_id).filter(status = 'Success').exclude(job_name='Job Flow').values_list('job_name', flat=True)[::1]
        # job_names_str = job_names_list[0]

        # for i in range(len(job_names_list) - 1):
        #     job_names_str = job_names_str + ", " + job_names_list[i + 1]

        # email_notification_jobflow(msg='Success', failed_killed_jobnames=job_names_str, process_id=process_id, jobflow_id=jobflow_id)
        if job_success_count_match:
            # processlog_update_status_util(
            #     'Success', process_id, jobflow_id)
            processlog_update_status_util('Success', jobflow_pk)
            print('*****Success')
        else:
            # processlog_update_status_util(
            #     'In-Complete Run', process_id, jobflow_id)
            processlog_update_status_util('In-Complete Run', jobflow_pk)
            print('*****In-Complete Run')

    elif last_run_status == 'Killed':
        print('*Killed'*100)
        # processlog_update_status_util('Killed', process_id, jobflow_id)
        processlog_update_status_util('Killed', jobflow_pk)
        # job_names_list = Processlog.objects.filter(process_id = process_id).filter(jobflowname=jobflow_id).exclude(job_name='Job Flow').exclude(status='Success').values_list('job_name', flat=True)[::1]
        # job_names_str = job_names_list[0]

        # for i in range(len(job_names_list) - 1):
        #     job_names_str = job_names_str + ", " + job_names_list[i + 1]

        # email_notification_jobflow(msg='Killed', failed_killed_jobnames=job_names_str, process_id=process_id, jobflow_id=jobflow_id)

    elif last_run_status == 'Failed':
        print('*Failed'*100)
        # processlog_update_status_util('Failed', process_id, jobflow_id)
        processlog_update_status_util('Failed', jobflow_pk)

        # job_names_list = Processlog.objects.filter(process_id = process_id).filter(jobflowname=jobflow_id).exclude(job_name='Job Flow').exclude(status='Success').values_list('job_name', flat=True)[::1]
        # job_names_str = job_names_list[0]

        # for i in range(len(job_names_list) - 1):
        #     job_names_str = job_names_str + ", " + job_names_list[i + 1]

        # email_notification_jobflow(msg='Failed', failed_killed_jobnames=job_names_str, process_id=process_id, jobflow_id=jobflow_id)




def update_jobflow_single_job_executed(rerun_flag, execution_type, process_id, jobflow_id, jobflowdetail_id, jobflow_pk):
    time.sleep(1)
    if execution_type == 'S' and not rerun_flag:

        if Processlog.objects.filter(process_id=process_id).filter(jobflowname=jobflow_id).filter(jobflowdetail=jobflowdetail_id).filter(status='Success').exists():
            print('meta:view:exe_jobs_worker_process:Success',
                  'process_id:', process_id)
            processlog_update_status_util('Success', jobflow_pk)
            return 0

        if Processlog.objects.filter(process_id=process_id).filter(jobflowname=jobflow_id).filter(jobflowdetail=jobflowdetail_id).filter(status='Killed').exists():
            print('meta:view:exe_jobs_worker_process:Killed',
                  'process_id:', process_id)
            processlog_update_status_util('Killed', jobflow_pk)
            return 1

        elif Processlog.objects.filter(process_id=process_id).filter(jobflowname=jobflow_id).filter(jobflowdetail=jobflowdetail_id).filter(status='Failed').exists():
            print('meta:view:exe_jobs_worker_process:Failed',
                  'process_id:', process_id)
            processlog_update_status_util('Failed', jobflow_pk)
            return 2

    elif execution_type == 'S' and execution_type:
        if Processlog.objects.filter(process_id=process_id).filter(jobflowname=jobflow_id).filter(jobflowdetail=jobflowdetail_id).filter(status='Success').exists():
            print('meta:view:exe_jobs_worker_process:Success',
                  'process_id:', process_id)
            processlog_update_status_util('Success', jobflow_pk)
            return 0

        if Processlog.objects.filter(process_id=process_id).filter(jobflowname=jobflow_id).filter(jobflowdetail=jobflowdetail_id).filter(status='Killed').exists():
            print('meta:view:exe_jobs_worker_process:Killed',
                  'process_id:', process_id)
            processlog_update_status_util('Killed', jobflow_pk)
            return 1

        elif Processlog.objects.filter(process_id=process_id).filter(jobflowname=jobflow_id).filter(jobflowdetail=jobflowdetail_id).filter(status='Failed').exists():
            print('meta:view:exe_jobs_worker_process:Failed',
                  'process_id:', process_id)
            processlog_update_status_util('Failed', jobflow_pk)
            return 2

def exe_jobs_worker_process_bridge(user, rerun_flag, process_id, jobflow_pk, job_type, jobflowdetail_id, object_id, project_d):
    worker_proces_bridge = multiprocessing.Process(target=exe_jobs_worker_process, args=(
        user, rerun_flag, process_id, jobflow_pk, job_type, jobflowdetail_id, object_id, project_d))
    worker_proces_bridge.daemon = True
    worker_proces_bridge.start()
    worker_proces_bridge.join(10800)
    # worker_proces_bridge.join(5)
    # If thread is still active
    if worker_proces_bridge.is_alive():
        print("Job is running more then 3 hours:", 'process_id:', process_id)
        # worker_proces_bridge.terminate()
        Jobflowdetail_d = Jobflowdetail.objects.get(
            pk=jobflowdetail_id).__dict__
        msg = 'Job is running more then 3 hours: ' + str(process_id)
        email_notification_logrunning_job(
            msg, process_id=process_id, **Jobflowdetail_d)
        worker_proces_bridge.join()
    else:
        worker_proces_bridge.join()

def exe_jobs(request, project_id, jobflow_id, jobflowdetail_id):
    print('meta:view:exe_jobs', 'jobflow_id:', jobflow_id,
          'jobflowdetail_id:', jobflowdetail_id)

    rerun_flag = False
    project_d = Project.objects.get(pk=project_id).__dict__
    jobflow_d = Jobflow.objects.get(pk=jobflow_id).__dict__
    jobflowdetail_d = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__
    user = request.user

    if project_d['is_active'] != 'Y':  # checking if the project is active
        error_message = 'Project:' + \
            project_d['project_name'] + ' is Not Active'
        messages.info(request, error_message)
        return redirect('scripts:jobflowdetail', jobflow_id=jobflow_id)

    if jobflow_d['is_active'] != 'Y':  # checking if the jobflow is active
        error_message = 'Jobflow:' + \
            jobflow_d['jobflowname'] + ' is Not Active'
        messages.info(request, error_message)
        return redirect('scripts:jobflowdetail', jobflow_id=jobflow_id)

    if jobflowdetail_d['is_active'] != 'Y':  # checking if the jobdetail is active
        error_message = 'Job Name:' + \
            jobflowdetail_d['job_name'] + ' is Not Active'
        messages.info(request, error_message)
        return redirect('scripts:jobflowdetail', jobflow_id=jobflow_id)

    job_type, object_id = jobflowdetail_d['job_type'], jobflowdetail_d['object_id']
    # check_object_is_active_request(request, jobflow_id, job_type, object_id)
    if job_type == 'Stored_Proc':
        spname_d = Spname.objects.get(pk=object_id).__dict__

        if spname_d['is_active'] != 'Y':
            error_message = 'Stored Proc Name:' + \
                spname_d['report_name'] + \
                ' is Not Active, Please check SP Details page'
            messages.info(request, error_message)
            return redirect('scripts:jobflowdetail', jobflow_id=jobflow_id)

    elif job_type == 'Shell_Script':
        script_d = Script.objects.get(pk=object_id).__dict__

        if script_d['is_active'] != 'Y':
            error_message = 'Script Name:' + \
                script_d['job_name'] + \
                ' is Not Active, Please check Shell Scripts'
            messages.info(request, error_message)
            return redirect('scripts:jobflowdetail', jobflow_id=jobflow_id)

    elif job_type == 'Table':
        table_d = Tbllist.objects.get(pk=object_id).__dict__

        if table_d['is_active'] != 'Y':
            print('meta:exe_jobs: executing Table')
            return redirect('scripts:jobflowdetail', jobflow_id=jobflow_id)

    process_id, jobflow_pk = processlog_create_jobflow_util(
        jobflowdetail_id, 'S')
    worker_proces = multiprocessing.Process(target=exe_jobs_worker_process_bridge, args=(
        user, rerun_flag, process_id, jobflow_pk, job_type, jobflowdetail_id, object_id, project_d))
    # worker_proces.daemon = True
    worker_proces.start()
    time.sleep(.02)
    processlog_update_pid_util(jobflow_pk, worker_proces.pid)

    info_message = 'Job Submited: ' + \
        str(jobflowdetail_d['job_name']) + \
        ', Submited, Process id:' + str(process_id)
    messages.info(request, info_message)

    return redirect('scripts:jobflowdetail', jobflow_id=jobflow_id)

#####end of execute single job generic######
###################restart#################
def exe_jobflow_rerun(request, process_id, record_id):
    print('meta:view:exe_jobflow_rerun:', 'process_id:',
          process_id, 'record_id:', record_id)
    rerun_flag = True
    user = request.user
    p = Processlog.objects.get(pk=record_id)
    jobflow_id = p.jobflowname_id
    jobflow_d = Jobflow.objects.get(pk=jobflow_id).__dict__
    project_id = jobflow_d['project_name_id']
    project = get_object_or_404(Project, pk=project_id)
    project_d = project.__dict__

    jobflow_process_ins = Processlog.objects.get(
        process_id=process_id, project_job_name='Job Flow')
    jobflow_process_ins.status = 'Executing'
    # jobflow_process_ins.start_time = timezone.now()
    jobflow_process_ins.save()
    # time.sleep(.25)
    # jobflow_process_log_id = jobflow_process_ins.pk
    jobflow_pk = jobflow_process_ins.pk
    print('job_type,', p.job_type, 'jobflow_process_ins:',
          jobflow_process_ins.execution_type, 'rerun_flag:', rerun_flag)

    # if (p.job_type != 'Job Flow' or jobflow_process_ins.execution_type == 'S'):
    # when single job is triggered,
    # when single job ir re run or failed jobflow is re run, to handle case 1 & 2
    if (jobflow_process_ins.execution_type == 'S'):
        jobflowdetail_id = p.jobflowdetail_id
        jobflowdetail_d = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__
        object_id = jobflowdetail_d['object_id']
        job_type = jobflowdetail_d['job_type']
        worker_proces = multiprocessing.Process(target=exe_jobs_worker_process_bridge, args=(
            user, rerun_flag, process_id, jobflow_pk, job_type, jobflowdetail_id, object_id, project_d))
        worker_proces.start()
        time.sleep(.2)
        processlog_update_pid_util(jobflow_pk, worker_proces.pid)
        time.sleep(.5)
        return redirect('logview:process_detail', process_id=process_id)

    # when job flow is executed, and in re run single job is executed case 3
    # if (jobflow_process_ins.execution_type == 'S'):

    elif (p.job_type != 'Job Flow' and jobflow_process_ins.execution_type == 'M'):  # print('job flow')
        print('single job flow')
        # jobflow_worker_process = multiprocessing.Process(target=exe_jobflow_process, args=(
        #     user, rerun_flag, process_id, jobflow_pk, jobflow_id, project_id, project_d))

        jobflowdetail_id = p.jobflowdetail_id
        jobflowdetail_d = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__
        object_id = jobflowdetail_d['object_id']
        job_type = jobflowdetail_d['job_type']

        jobflow_worker_process = multiprocessing.Process(target=exe_jobs_worker_process_bridge, args=(
            user, rerun_flag, process_id, jobflow_pk, job_type, jobflowdetail_id, object_id, project_d))

        jobflow_worker_process.start()
        time.sleep(.2)
        processlog_update_pid_util(jobflow_pk, jobflow_worker_process.pid)
        #return redirect('logview:processlog')
        time.sleep(.5)
        return redirect('logview:process_detail', process_id=process_id)

    # when job flow is executed, and in re run jobflowexecuted case 4
    else:  # print('job flow')
        print('job flow')
        jobflow_worker_process = multiprocessing.Process(target=exe_jobflow_process, args=(
            user, rerun_flag, process_id, jobflow_pk, jobflow_id, project_id, project_d))

        jobflow_worker_process.start()
        time.sleep(.2)
        processlog_update_pid_util(jobflow_pk, jobflow_worker_process.pid)
        #return redirect('logview:processlog')
        time.sleep(.5)
        return redirect('logview:process_detail', process_id=process_id)





###################restart#################


#########################import/exported view ######################
def imp_sp(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    myfile = request.FILES['myfile']
    file_obj = myfile.readlines()[1:]
    tmp_num_of_lines = file_obj
    number_of_lines = len(tmp_num_of_lines)
    print("Info:meta:import_src_system_all_item: Number of lines", number_of_lines)

    column_list = ['project_name', 'dsn_name', 'report_name', 'sp_name', 'start_dt',
                   'end_dt', 'med_center', 'result_table', 'additional_param', 'priority_id', 'is_active']

    for i in range(number_of_lines):
        file_obj_tmp = file_obj[i]
        file_obj_tmp = file_obj_tmp.decode("utf-8").rstrip()
        # print(file_obj_tmp) .rstrip()
        input_file = ''.join(file_obj_tmp)
        input_file_list = input_file.split(",")

        input_file_list.pop(0)
        input_file_list.insert(0, project)
        # defaults = {}
        defaults = dict(zip(column_list, input_file_list))

        dsn = get_object_or_404(DataSource, pk=defaults['dsn_name'])
        defaults['dsn_name'] = dsn
        print("last ", defaults)

        try:
            obj = Spname.objects.get(
                project_name=defaults['project_name'], report_name=defaults['report_name'])
            print("obj", obj)
            for key, value in defaults.items():
                setattr(obj, key, value)
            obj.save()

            print("Info:meta:import_src_system_all_item:Updated the source system:",
                  defaults['project_name'], "report_name:", defaults['report_name'])
        except Spname.DoesNotExist:
            new_values = defaults
            new_values.update(defaults)
            obj = Spname(**new_values)
            obj.save()
            print("Info:meta:import_sp:Imported new sp in Project:",
                  defaults['project_name'], "report_name:", defaults['report_name'])

    return render(request, 'meta/import_sp_view.html', {'project': project})


def imp_sp_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'meta/import_sp_view.html', {'project': project})


def exp_sp(request, project_id, spname_id=0):
    spname_id = int(spname_id)
    project_to_export = get_object_or_404(Project, pk=project_id)
    print("Exporting individual_objects from source system::",
          project_to_export, "sp_id:", spname_id)
    print("spname_idspname_idspname_idspname_id", spname_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sp_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['project_name', 'dsn_name', 'report_name', 'sp_name', 'start_dt', 'end_dt',
                     'med_center', 'result_table', 'additional_param', 'priority_id', 'is_active'])

    if spname_id == 0:
        print("all project 333333spname_idspname_idspname_idspname_id", spname_id)
        sp_list = Spname.objects.filter(project_name=project_id).values_list('project_name', 'dsn_name', 'report_name',
                                                                             'sp_name', 'start_dt', 'end_dt', 'med_center', 'result_table', 'additional_param', 'priority_id', 'is_active')
    else:
        print("22222spname_idspname_idspname_idspname_id", spname_id)
        sp_list = Spname.objects.filter(project_name=project_id).filter(pk=spname_id).values_list(
            'project_name', 'dsn_name', 'report_name', 'sp_name', 'start_dt', 'end_dt', 'med_center', 'result_table', 'additional_param', 'priority_id', 'is_active')

    for individual_sp in sp_list:
        writer.writerow(individual_sp)

    return response


def exp_sp_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'meta/export_sp_names.html', {'project': project})

#########################sp views######################


@login_required
def del_sp(request, project_id, spname_id):
    print("meta:view:del_sp:project_id:", project_id, 'spname_id:', spname_id)
    project = get_object_or_404(Project, pk=project_id)
    spname = Spname.objects.get(pk=spname_id)
    spname.delete()
    # return redirect('meta:del_sp_view', project=project)
    return render(request, 'meta/sp_delete_list.html', {'project': project})


@login_required
def del_sp_view(request, project_id):
    print("meta:view:del_sp_view:project_id:", project_id)
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'meta/sp_delete_list.html', {'project': project})


class SpUpdate(UpdateView):
    model = Spname
    form_class = SpFormupdate
    pk_url_kwarg = "spname_id"
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    template_name = 'meta/sp_update.html'
    # success_url = reverse_lazy('meta:index')

    def get_success_url(self):
        spname_id = self.kwargs['spname_id']
        print('self', self.kwargs['spname_id'])
        project_id = Spname.objects.get(pk=spname_id).__dict__[
            'project_name_id']
        return reverse_lazy('meta:sp_detail', args=(project_id,))


def sp_add(request, project_id):
    print("meta:view:sp_add:project_id:", project_id, 'adding stored proc')
    project = get_object_or_404(Project, pk=project_id)
    project_id = int(project_id)
    # form = SpCreateForm(request.POST or None, request.FILES or None, initial={'project_name': project,'project_id': project_id})
    form = SpCreateForm(request.POST or None, initial={
                        'project_id': project_id})
    if form.is_valid():
        # projects_spname = project.spname_set.all()
        projects_spname = project.spname_set.all().filter(project_name_id=project_id)
        projects_spname_dict = project.spname_set.all().filter(
            project_name_id=project_id).__dict__
        print("projects_spname_dict", projects_spname_dict)
        # projects_spname = get_object_or_404(Project, pk=project_id)
        for s in projects_spname:
            if s.sp_name == form.cleaned_data.get("sp_name"):
                context = {
                    'project': project,
                    'form': form,
                    'error_message': 'You already added table/sp_name in project',
                }
                return render(request, 'meta/sp_add.html', context)
        splist = form.save(commit=False)
        splist.project = project
        splist.save()
        return render(request, 'meta/sp_detail.html', {'project': project})
    context = {
        'project': project,
        'form': form,
    }
    return render(request, 'meta/sp_add.html', context)

# SP BULK Update


class ProjectSPBulkUpdated(UpdateView):
    pk_url_kwarg = "project_id"
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True

    model = Project
    fields = ['project_name']
    # template_name = 'meta/project_dsn_update.html'
    template_name = 'meta/project_SPBulkUpdate.html'

    def get_success_url(self):
        return reverse_lazy('meta:sp_detail', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        data = super(ProjectSPBulkUpdated, self).get_context_data(**kwargs)
        if self.request.POST:
            data['datasources'] = ProjectSpFormSet(
                self.request.POST, instance=self.object)
        else:
            data['datasources'] = ProjectSpFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        datasources = context['datasources']
        with transaction.atomic():
            self.object = form.save()

            if datasources.is_valid():
                datasources.instance = self.object
                datasources.save()
        return super(ProjectSPBulkUpdated, self).form_valid(form)


def sp_detail(request, project_id):
    if not request.user.is_authenticated:
        return render(request, 'account/login.html')
    else:
        user = request.user
        project = get_object_or_404(Project, pk=project_id)
        return render(request, 'meta/sp_detail.html', {'project': project, 'user': user})

#########################Environment variables ##############################


class ProjectEnvUpdated(UpdateView):
    pk_url_kwarg = "project_id"
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True

    model = Project
    fields = ['project_name']
    template_name = 'meta/project_EnvUpdate.html'

    def get_success_url(self):
        # return reverse_lazy('meta:sp_detail', args=(self.object.id,))
        return reverse_lazy('meta:project_update', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        data = super(ProjectEnvUpdated, self).get_context_data(**kwargs)
        if self.request.POST:
            data['datasources'] = ProjectEnvProjectFormSet(
                self.request.POST, instance=self.object)
        else:
            data['datasources'] = ProjectEnvProjectFormSet(
                instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        datasources = context['datasources']
        with transaction.atomic():
            self.object = form.save()

            if datasources.is_valid():
                datasources.instance = self.object
                datasources.save()
        return super(ProjectEnvUpdated, self).form_valid(form)

#########################Project views######################
# # #put the confirm delete page


@login_required
def project_delete(request, project_id):
    project = Project.objects.get(pk=project_id)
    project.delete()
    print("meta:view:project_delete:project id:",
          project_id, 'project_name:', project.project_name)

    if request.user.is_superuser:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(user=request.user)
    return redirect('meta:index')


class ProjectUpdate(UpdateView):
    model = Project
    template_name = 'meta/project_update.html'
    form_class = ProjectForm
    success_url = reverse_lazy('meta:index')


@login_required
def project_create(request):
    print("meta:view:project_create")
    if not request.user.is_authenticated:
        return render(request, 'account/login.html')
    else:
        form = ProjectForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return render(request, 'meta/sp_detail.html', {'project': project})
        context = {
            "form": form,
        }
        return render(request, 'meta/project_create.html', context)

#########################index views######################


@login_required
def index(request):
    # SERVER_NAME = settings.SERVER_NAME
    # print('SERVER_NAME:', SERVER_NAME)
    if not request.user.is_authenticated:
        return render(request, 'account/login.html')

    elif request.user.is_superuser:
        projects = Project.objects.all().order_by('id')
        sp_results = Spname.objects.all()
        # query = request.GET.get("q")
        # print('query:', query, type(query))

        # if query:
        # if request.GET.get("q").key():
        if 'q' in request.GET:
            query = request.GET.get("q")
            projects = projects.filter(
                Q(project_name__icontains=query)
            ).distinct()
            # sp_results = sp_results.filter(
            #     Q(report_name__icontains=query)
            # ).distinct()
            return render(request, 'common/index.html', {
                'projects': projects,
                # 'sp_results': sp_results,
            })
        else:
            projects = Project.objects.all()
            return render(request, 'common/index.html', {'projects': projects})
            # return render(request, 'common/index.html', {'projects': projects, 'SERVER_NAME':SERVER_NAME})

    else:
        projects = Project.objects.filter(user=request.user).order_by('id')
        sp_results = Spname.objects.all()

        # if query:
        if 'q' in request.GET:
            query = request.GET.get("q")
            projects = projects.filter(
                Q(project_name__icontains=query)
            ).distinct()
            # sp_results = sp_results.filter(
            #     Q(report_name__icontains=query)
            # ).distinct()
            return render(request, 'common/index.html', {
                'projects': projects,
                # 'sp_results': sp_results,
            })
        else:
            return render(request, 'common/index.html', {'projects': projects})
            # return render(request, 'common/index.html', {'projects': projects, 'SERVER_NAME':SERVER_NAME})


# def index(request):
#     if not request.user.is_authenticated:
#         return render(request, 'account/login.html')

#     elif request.user.is_superuser:
#         projects = Project.objects.all().order_by('id')
#         sp_results = Spname.objects.all()
#         query = request.GET.get("q")
#         if query:
#             projects = projects.filter(
#                 Q(project_name__icontains=query)
#             ).distinct()
#             sp_results = sp_results.filter(
#                 Q(report_name__icontains=query)
#             ).distinct()
#             return render(request, 'common/index.html', {
#                 'projects': projects,
#                 'sp_results': sp_results,
#             })
#         else:
#             return render(request, 'common/index.html', {'projects': projects})

#     else:
#         projects = Project.objects.filter(user=request.user).order_by('id')
#         sp_results = Spname.objects.all()
#         query = request.GET.get("q")
#         if query:
#             projects = projects.filter(
#                 Q(project_name__icontains=query)
#             ).distinct()
#             sp_results = sp_results.filter(
#                 Q(report_name__icontains=query)
#             ).distinct()
#             return render(request, 'common/index.html', {
#                 'projects': projects,
#                 'sp_results': sp_results,
#             })
#         else:
#             return render(request, 'common/index.html', {'projects': projects})

#     # error_message = 'error_message' + ' ' + str(project) + ' ' + str(max_limit)
#     # return JsonResponse({'Failure': error_message})


# from scripts.views import *

# from .models import User
# from django.db import connection, transaction
# import sqlite3, csv, threading, time
# from multiprocessing import Process, Queue, Pipe
# from django.core.mail import send_mail
# from django.conf import settings


# class SpUpdate(UpdateView):
#     model = Spname
#     form_class = SpFormupdate
#     pk_url_kwarg = "spname_id"
#     slug_url_kwarg = 'slug'
#     query_pk_and_slug = True
#     template_name = 'meta/sp_update.html'
#     success_url = reverse_lazy('meta:index')


# jobflow history

####search job name stored proc name ####


# tracking user activity

# def project_history(request):
#     user = request.user
#     project = Project.history.filter(user=user)

#     # project = get_object_or_404(Project, pk=project_id)
#     return render(request, 'meta/project_history.html', {'project': project, 'user': user})

# return HttpResponse(p)


# projecjobflowdetailtobjects

# def projecthistorytobjects(request):
#     return render(request, 'meta/project_history.html')


# def get_projecthistory_options():
#     return "options", {

#         "jobflow": [{'label': obj.jobflowname, 'value': obj.pk} for obj in Jobflow.objects.all()],
#         "jobflowdetail": [{'label': obj.project_job_name, 'value': obj.pk} for obj in Jobflowdetail.objects.all()]
#     }


# from logview.serializers import JobflowSerializer, ProcesslogSerializer, DetaillogSerializer

# #ProjectJobflowdetailViewSet
# class ProjectHistorylViewSet(viewsets.ModelViewSet):
#     ##queryset = Jobflowdetail.objects.all().order_by('jobflowname')  # .reverse()
#     ##queryset = Project.history.filter(user=user)
#     ##queryset = Project.history.all()
#     ## queryset = Processlog.objects.all()
#     ## serializer_class = ProjectHistorySerializer

#     queryset = Processlog.objects.filter(job_type="Job Flow").order_by('id').reverse()
#     serializer_class = ProcesslogSerializer

#     # # def get_options(self):
#     # #     return get_projecthistory_options()

#     class Meta:
#         datatables_extra_json = ('get_options', )


# can be deleted
# def test(request):
#     # p = Project.objects.create(project_name="ddd", success_email='arjun.kumar@kp.com')
#     # p.project_name = "ddd1"
#     # p.save()

#     # delta = new_record.diff_against(old_record)
#     # for change in delta.changes:
#     #     print("{} changed from {} to {}".format(change.field, change.old, change.new))


#     # p = Project.objects.filter(history__history_user=1)
#     # p = Project.history.all().values()
#     # print(p)

#     p = Project.objects.get(pk=1)
#     print(model_to_dict(p))
#     #p = Project
#     # p = Project.objects.filter(something).prefetch_related(Prefetch('history', queryset=Project.history.order_by('-history_date'), \
#     #                                         to_attr='ordered_histories')

#     return HttpResponse(p)
#     # return render(request, 'meta/advance_search.html')

# def get_job_flow_max_limit(jobflow_id):
#     jobflow_d = Jobflow.objects.get(pk=jobflow_id).__dict__
#     max_limit = jobflow_d['max_num_of_threads']
#     return max_limit








# if Processlog.objects.filter(process_id = process_id).filter(jobflowname=jobflow_id).filter(status='Success').exists():
    #     print('meta:view:exe_jobs_worker_process:Success', 'process_id:', process_id)
    #     #job_status =
    #     processlog_update_status_util('Success', process_id, jobflow_id)
    #     return 0

    # if Processlog.objects.filter(process_id = process_id).filter(jobflowname=jobflow_id).filter(status='Killed').exists():
    #     print('meta:view:exe_jobs_worker_process:Killed', 'process_id:', process_id)
    #     #job_status =
    #     processlog_update_status_util('Killed', process_id, jobflow_id)
    #     return 1

    # elif Processlog.objects.filter(process_id = process_id).filter(jobflowname=jobflow_id).filter(status='Failed').exists():
    #     print('meta:view:exe_jobs_worker_process:Fail', 'process_id:', process_id)
    #     #job_status =
    #     processlog_update_status_util('Failed', process_id, jobflow_id)
    #     return 2
