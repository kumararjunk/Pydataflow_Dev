from .utils import *
import os, pathlib
import argparse, sys, logging, time, subprocess, os.path, calendar
from meta.models import Project, Jobflow, Jobflowdetail, Sch
#from meta.models import Script, Spname,

from django.db.models import Max
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework import routers, serializers, viewsets
from .serializers import ScheduleSerializer
from .serializers import ProjectSerializer, JobflowSerializer
#from .serializers import StandardResultsSetPagination


###sch jobflow#####################################

def sch_delete_cron(request, record_id):
    remove_sch_generic_util(record_id)
    return redirect('sch:schedule')

def sch_create_cron(request, project_id, jobflow_id=0, jobflowdetail_id=0, sch_type=0):
    jobflow_id, jobflowdetail_id, sch_type = int(jobflow_id), int(jobflowdetail_id), int(sch_type)
    project = get_object_or_404(Project, pk=project_id)
    print("Info:sch:sch_create_cron:Consolidating all the parameter passed, Trying to scheudle the Project name:",project ,"jobflow_id:",jobflow_id, 'jobflowdetail_id:', jobflowdetail_id)
    #Minutes
    every_minutes, selected_minutes = request.POST.getlist('minutes'), request.POST.getlist('selectMinutes[]')
    minutes = every_minutes if 'select' not in str(every_minutes) else selected_minutes
    #Hour
    every_hours, selected_hours = request.POST.getlist('hours'), request.POST.getlist('selectHours[]')
    hours = every_hours if 'select' not in str(every_hours) else selected_hours
    #Days
    every_days, selected_days = request.POST.getlist('days'), request.POST.getlist('selectDays[]')
    days = every_days if 'select' not in str(every_days) else selected_days
    #Months
    every_months, selected_months = request.POST.getlist('months'), request.POST.getlist('selectMonths[]')
    months = every_months if 'select' not in str(every_months) else selected_months
    #weekdays
    every_weekdays, selected_weekdays = request.POST.getlist('weekdays'), request.POST.getlist('selectWeekdays[]')
    weekdays = every_weekdays if 'select' not in str(every_weekdays) else selected_weekdays

    etl_schedule = str(minutes) + ' :' + str(hours) + ' :' + \
                    str(days) + ' :' + str(months) + ' :' + str(weekdays) + ' '

    etl_schedule = etl_schedule.replace("[", "").replace("]", "").replace("'", "")
    #print("Info:sch:sch_create_cron:Trying to scheudle the Project name:",project ,"jobflow_id:",jobflow_id, 'jobflowdetail_id:', jobflowdetail_id, 'etl_schedule:', etl_schedule)
    ##updating the backend database
    sch_pk = create_etl_sch_util(project_id, jobflow_id, jobflowdetail_id, sch_type, etl_schedule)
    # print('sch_pk:', sch_pk ,'Sch:',Sch.objects.get(pk=sch_pk).__dict__)

    scheudle_project_util(project_id=project_id, jobflow_id=jobflow_id, jobflowdetail_id=jobflowdetail_id, sch_type=sch_type, sch_pk=sch_pk)
    #return redirect('scripts:jobflowdetail', jobflow_id=jobflow_id)
    return redirect('sch:schedule')

# sch_wizard_generic
def sch_wizard_generic(request, project_id, jobflow_id=0, jobflowdetail_id=0, sch_type=0):
    project = get_object_or_404(Project, pk=project_id)
    jobflow_id = int(jobflow_id)
    jobflowdetail_id = int(jobflowdetail_id)
    sch_type = int(sch_type)

    if sch_type == 1:
        jobflow = get_object_or_404(Jobflow, pk=jobflow_id)
        template = 'sch/scheudle_wizard_flow.html'
        return render(request, template, {'project': project, 'jobflow': jobflow})

    elif sch_type == 2:
        jobflow = get_object_or_404(Jobflow, pk=jobflow_id)
        jobflowdetail = get_object_or_404(Jobflowdetail, pk=jobflowdetail_id)
        template = 'sch/scheudle_wizard_flow_detail.html'
        return render(request, template, {'project': project, 'jobflow': jobflow, 'jobflowdetail': jobflowdetail})

def get_processlog_options():
    return "options", {

        "jobflow": [{'label': obj.jobflowname, 'value': obj.pk} for obj in Jobflow.objects.all()],
        "jobflowdetail": [{'label': obj.project_job_name, 'value': obj.pk} for obj in Jobflowdetail.objects.all()]
    }

def schedule(request):
    return render(request, 'sch/sch.html')

class ScheduleViewSet(viewsets.ModelViewSet):
    # queryset = Sch.objects.all().order_by('id') #(user=request.user).order_by('id')
    #queryset = Sch.objects.filter(job_type="Job Flow").order_by('id').reverse()
    queryset = Sch.objects.all().order_by('id').reverse()
    serializer_class = ScheduleSerializer
    # pagination_class = StandardResultsSetPagination
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # search_fields = ['project_name__project_name', 'jobflowname__jobflowname2']
    #, 'jobflow__jobflowname'

    def get_options(self):
        return get_processlog_options()

    class Meta:
        datatables_extra_json = ('get_options', )






###end sch jobflow#####################################


##this view will be decommisioned
# def sch_main_view(request, project_id, jobflow_id):
#     # curr_date_time = time.strftime("%Y-%m-%d")
#     # curr_timestamp = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
#     project = get_object_or_404(Project, pk=project_id)
#     jobflow = get_object_or_404(Jobflow, pk=jobflow_id)
#     print("Info:sch:sch_project_table_main_view:Showing the scheudle main view for the project/tables:", project)
#     return render(request, 'scripts/sch_main_view.html',
#         {'project': project, 'jobflow': jobflow})


# def sch_remove_cron(request, project_id, jobflow_id=0, jobflowdetail_id=0, sch_type=0):
#     print('*'*100)
#     print('sch_remove_cron '*10)
#     jobflow_id = int(jobflow_id)
#     jobflowdetail_id = int(jobflowdetail_id)
#     sch_type = int(sch_type)
#     project = get_object_or_404(Project, pk=project_id)
#     jobflow = get_object_or_404(Jobflow, pk=jobflow_id)
#     print("Info:sch:un_scheudle_project:Un scheudeling the project:",project, 'jobflow:', jobflow)
#     #remove_sch_generic_util(project_id, jobflow_id, jobflowdetail_id, sch_type, **project_jobname_all_d)
#     etl_schedule=''
#     #update_etl_sch_util(project_id, jobflow_id, jobflowdetail_id, sch_type, etl_schedule)

#     #recreating the query set to get the updated values
#     project = get_object_or_404(Project, pk=project_id)
#     jobflow = get_object_or_404(Jobflow, pk=jobflow_id)

#     return redirect('sch:schedule')
