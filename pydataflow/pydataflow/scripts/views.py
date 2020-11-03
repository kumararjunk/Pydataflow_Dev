import django.contrib
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from django.core.mail import send_mail
import os, pathlib
import argparse, sys, logging, time, subprocess, os.path, calendar

from meta.models import Project, Processlog, Script, Jobflow, Jobflowdetail, Spname, Tbllist
from django.db.models import Max
from .forms import ScriptCreateForm, ScriptUpdateForm, JobflowForm, Choose_obj_Form
from .forms import JobflowDetailFormUpdate
# import multiprocessing
# from multiprocessing import Process, Queue, Pipe
# from multiprocessing import Pool
# from django.contrib import messages
# from django.views.generic import UpdateView
# import threading, time

def select_obj(request, jobflow_id):
    print("scripts:view:select_obj:jobflow_id:", jobflow_id)
    jobflows = get_object_or_404(Jobflow, pk=jobflow_id)
    jobflow_id_dict = Jobflow.objects.get(pk=jobflow_id).__dict__
    project_id = jobflow_id_dict['project_name_id']
    project = get_object_or_404(Project, pk=project_id)

    # project_d = Project.objects.get(pk=project_id).__dict__
    # project_id = project_d['id']
    request.session['project_id'] = project_id
    current_user = request.user
    user_id = current_user.id
    job_type = request.POST.get('job_type')

    if job_type is None:
        job_type = request.session['job_type']
    else:
        request.session['job_type'] = job_type

    # spname_list --> import_list add the referene to access to the project
    if job_type == 'Stored_Proc':
        import_obj = Spname.objects.filter(user_id=request.user).filter(project_name_id=project_id).filter(job_type = job_type)
        import_obj_dict = Spname.objects.filter(user_id=request.user).filter(project_name_id=project_id).filter(job_type = job_type).values()
        #import_obj_dict = Spname.objects.filter(user_id=request.user).filter(project_name_id=project_id).filter(job_type = job_type).values()

    elif job_type == 'Table':
        import_obj = Tbllist.objects.filter(user_id=request.user).filter(project_name_id=project_id).filter(job_type = job_type)
        import_obj_dict = Tbllist.objects.filter(user_id=request.user).filter(project_name_id=project_id).filter(job_type = job_type).values()

    elif job_type == 'Shell_Script':
        import_obj = Script.objects.filter(user_id=request.user).filter(project_name_id=project_id).filter(job_type = job_type)
        import_obj_dict = Script.objects.filter(user_id=request.user).filter(project_name_id=project_id).filter(job_type = job_type).values()
        #import_obj_dict['additional_param'])

    existing_obj = Jobflowdetail.objects.filter(jobflowname_id=jobflow_id).filter(job_type = job_type)
    existing_obj_list = []

    for job in existing_obj:
        existing_obj_list.append(job.job_name)

    if 'new_tbls' in request.POST and len(request.POST.getlist('new_tbls')) > 0:
        new_tbl_raw = request.POST.getlist('new_tbls',default=None)
        new_tbl_raw = [ x for x in new_tbl_raw if x not in existing_obj_list ]

        new_objects = []
        if job_type == 'Stored_Proc':
            for i in range(len(import_obj_dict)):
                if import_obj_dict[i]['report_name'] in new_tbl_raw:
                    new_objects.append((jobflows.id , import_obj_dict[i]['report_name'], import_obj_dict[i]['additional_param'], job_type, import_obj_dict[i]['id']))

        elif job_type == 'Table':
            for i in range(len(import_obj_dict)):
                if import_obj_dict[i]['table_name'] in new_tbl_raw:
                    new_objects.append((jobflows.id , import_obj_dict[i]['table_name'], import_obj_dict[i]['additional_param'], job_type, import_obj_dict[i]['id']))

        elif job_type == 'Shell_Script':
            for i in range(len(import_obj_dict)):
                if import_obj_dict[i]['job_name'] in new_tbl_raw:
                    new_objects.append((jobflows.id , import_obj_dict[i]['job_name'], import_obj_dict[i]['additional_param'], job_type, import_obj_dict[i]['id']))

        for new_object in new_objects:
            Jobflowdetail.objects.update_or_create(jobflowname_id=new_object[0], project_job_name=new_object[1],
                                                   job_name=new_object[1],additional_param=new_object[2],
                                                  job_type=new_object[3], object_id=new_object[4])

        existing_obj = Jobflowdetail.objects.filter(jobflowname_id=jobflow_id).filter(job_type = job_type)

    elif 'delete_tble_list[]' in request.POST and len(request.POST.getlist('delete_tble_list[]')) > 0:
        delete_tble_list = request.POST.getlist('delete_tble_list[]',default=None)

        for job_name in delete_tble_list:
            job_to_delete = Jobflowdetail.objects.filter(jobflowname_id=jobflow_id).filter(job_type = job_type).filter(job_name = job_name)
            job_to_delete.delete()

        existing_obj = Jobflowdetail.objects.filter(jobflowname_id=jobflow_id).filter(job_type = job_type)

    print("scripts:view:select_obj:job_type:", job_type, 'existing_obj', existing_obj)
    return render(request, 'scripts/select_src_obj.html',
                           {'project': project, 'jobflows': jobflows,
                            'spname_list': import_obj,
                            'table_list': import_obj,
                            'shell_scripts': import_obj,
                            'existing_obj': existing_obj,
                            'job_type': job_type })



     # error_message = 'error_message'
    # return JsonResponse({'Failure': error_message})

def select_obj_type(request, jobflow_id):
    print("scripts:view:select_obj_type:jobflow_id:", jobflow_id)
    jobflow_id_dict = Jobflow.objects.get(pk=jobflow_id).__dict__
    project_id = jobflow_id_dict['project_name_id']

    project = Project.objects.get(id=project_id)
    jobflows = get_object_or_404(Jobflow, pk=jobflow_id)
    obj_form = Choose_obj_Form(request.POST or None, initial= {'job_type':'Tables'})
    return render(request, 'scripts/select_obj.html', {'project': project,
        'obj_form': obj_form,  'jobflows': jobflows})

class  jobflowdetailUpdate(UpdateView):
    model = Jobflowdetail
    form_class = JobflowDetailFormUpdate
    pk_url_kwarg = "jobflowdetail_id"
    #pk_url_kwarg = "jobflow_id"
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    template_name = 'scripts/jobflowdetail_update.html'
    # success_url = reverse_lazy('meta:index')

    def get_context_data(self, **kwargs):
        data = super(jobflowdetailUpdate, self).get_context_data(**kwargs)

        if self.request.POST:
            data['datasources'] = JobflowDetailFormUpdate(self.request.POST, instance=self.object)
        else:
            data['datasources'] = JobflowDetailFormUpdate(instance=self.object)
        return data

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        jobflowdetail_id = self.object.id
        jobflowdetail_d = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__
        job_name=cleaned_data['job_name']

        if 'job_name' in form.changed_data:
            if Jobflowdetail.objects.filter(job_name=cleaned_data['job_name'],
                                    jobflowname=jobflowdetail_d['jobflowname_id']).exists():
                message = job_name + ' already exist in the Jobflow:'
                form.add_error('job_name', (message))
                return super(jobflowdetailUpdate, self).form_invalid(form)

        return super(jobflowdetailUpdate, self).form_valid(form)

    def get_success_url(self):
        ## print('get success_url object id:', self.object.id, type(self.object.id))
        jobflowdetail_id = self.object.id
        jobflowdetail_d = Jobflowdetail.objects.get(pk=jobflowdetail_id).__dict__
        jobflow_id = jobflowdetail_d['jobflowname_id']
        return reverse_lazy('scripts:jobflowdetail', args=[jobflow_id])


def jobflowdetail_detail(request, jobflow_id):
    # print("scripts:view:jobflowdetail_detail:jobflow_id:", jobflow_id)
    if not request.user.is_authenticated:
        return render(request, 'account/login.html')
    else:
        jobflow_id_dict = Jobflow.objects.get(pk=jobflow_id).__dict__
        project_id = jobflow_id_dict['project_name_id']
        project = get_object_or_404(Project, pk=project_id)
        user = request.user
        jobflow = get_object_or_404(Jobflow, pk=jobflow_id)
        return render(request, 'scripts/jobflow_detail.html', {
            'project': project, 'jobflow': jobflow, 'user': user })

####jobflow
def jobflow_delete(request, jobflow_id):
    print("scripts:view:jobflow_delete:jobflow_id:", jobflow_id)
    jobflow_id_dict = Jobflow.objects.get(pk=jobflow_id).__dict__
    project_id = jobflow_id_dict['project_name_id']
    project = get_object_or_404(Project, pk=project_id)

    jobflow_delete = Jobflow.objects.get(pk=jobflow_id)
    jobflow_delete.delete()  # jobflow_delete.save()

    jobflows = Jobflow.objects.filter(project_name=project_id)
    return render(request, 'scripts/jobflow_index.html', {
            'project': project, 'jobflows': jobflows})

class JobflowUpdate(UpdateView):
    model = Jobflow
    form_class = JobflowForm
    pk_url_kwarg = "jobflow_id"
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    template_name = 'scripts/jobflow_update.html'
    # success_url = reverse_lazy('meta:index')

    def get_success_url(self):
        jobflow_id = self.object.id
        jobflow_id_dict = Jobflow.objects.get(pk=jobflow_id).__dict__
        project_id = jobflow_id_dict['project_name_id']
        print('jobflow_id:', jobflow_id, 'project_id:', project_id)
        # project = get_object_or_404(Project, pk=project_id)
        # jobflows = Jobflow.objects.filter(project_name=project_id)
        return reverse_lazy('scripts:jobflow_index', args=[project_id])

        # return reverse_lazy('scripts:jobflow_index',kwargs={'project': project_id})

def create_jobflow(request, project_id):
    print("scripts:view:create_jobflow:project_id:", project_id)
    if not request.user.is_authenticated:
        return render(request, 'account/login.html')
    else:
        project = get_object_or_404(Project, pk=project_id)
        form = JobflowForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            jobflow = form.save(commit=False)
            jobflow.user = request.user
            jobflow.project_name = project
            jobflow.save()
            jobflows = Jobflow.objects.filter(project_name=project_id)
            return render(request, 'scripts/jobflow_index.html', {'project': project, 'jobflows': jobflows})
        context = { "form": form }
        return render(request, 'scripts/jobflow_create.html', context)

@login_required
def jobflow_index(request, project_id):
    print("scripts:view:jobflow_index:project_id:", project_id)

    if not request.user.is_authenticated:
        return render(request, 'account/login.html')

    else:
        project = get_object_or_404(Project, pk=project_id)
        jobflows = Jobflow.objects.filter(project_name=project_id)
        return render(request, 'scripts/jobflow_index.html', {
            'project': project, 'jobflows': jobflows })

@login_required
def del_script(request, project_id, script_id):
    print("scripts:view:del_script:project_id:", project_id, 'script_id', script_id)
    project = get_object_or_404(Project, pk=project_id)
    script = Script.objects.get(pk=script_id)
    script.delete()
    return render(request, 'scripts/scripts_delete_list.html', {'project': project})

@login_required
def del_script_view(request, project_id):
    print("scripts:view:del_script_view:project_id:", project_id)
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'scripts/scripts_delete_list.html', {'project': project})

class scriptupdate(UpdateView):
    model = Script
    form_class = ScriptUpdateForm     # form_class = ScriptFormupdate
    pk_url_kwarg = "script_id"
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    template_name = 'scripts/scripts_update.html'
    pk_url_kwarg_project_id = "project_id"
    # success_url = reverse_lazy('meta:index')

    def get_success_url(self):
        script_id = self.object.id
        script_id_dict = Script.objects.get(pk=script_id).__dict__
        project_id = script_id_dict['project_name_id']
        # project = get_object_or_404(Project, pk=project_id)
        return reverse_lazy('scripts:scripts_detail', args=[project_id])

def scripts_add(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project_id = int(project_id)
    print("scripts:view:scripts_add:project_id:", project_id)
    # form = SpCreateForm(request.POST or None, request.FILES or None, initial={'project_name': project,'project_id': project_id})
    form = ScriptCreateForm(request.POST or None, initial={'project_id': project_id} )
    if form.is_valid():
        projects_script = project.script_set.all().filter(project_name_id=project_id)
        #projects_script_dict = project.script_set.all().filter(project_name_id=project_id).__dict__
        ## print("projects_script_dict", projects_script_dict)
        ## projects_script = get_object_or_404(Project, pk=project_id)
        for s in projects_script:
            if s.job_name == form.cleaned_data.get("job_name"):
                print("script_add job_name"*10, s.job_name)
                context = {
                    'project': project,
                    'form': form,
                    'error_message': 'You already added job_name/script in project',
                }
                return render(request, 'scripts/scripts_add.html', context)
        # print("adding job_name"*20, form.cleaned_data.get("job_name"))
        scriptlist = form.save(commit=False)
        scriptlist.user = request.user
        # scriptlist.project = project
        scriptlist.project_name = project
        scriptlist.save()
        return render(request, 'scripts/scripts_detail.html', {'project': project})
    context = {
        'project': project,
        'form': form,
    }
    return render(request, 'scripts/scripts_add.html', context)

def scripts_detail(request, project_id):
    print("scripts:view:scripts_detail:project_id:", project_id)
    if not request.user.is_authenticated:
        return render(request, 'account/login.html')
    else:
        user = request.user
        project = get_object_or_404(Project, pk=project_id)
        return render(request, 'scripts/scripts_detail.html', {'project': project, 'user': user})


