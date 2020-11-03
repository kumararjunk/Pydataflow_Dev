from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views import generic
from django.views.generic.edit import FormMixin, FormView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.db import transaction
from django.urls import reverse_lazy

from .forms import UserForm, domainForm
from common.forms import Project_access_Form

#from meta.forms import ProjectEnvFormSet

from django.core.mail import send_mail, BadHeaderError

from meta.models import Project, DataSource, Tbllist
from meta.models import Project_access
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.db import models

from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template

from .utils import *

# from .forms import NameForm
##, Type_of_accessForm
# from .forms import ProjectaccessFormSet
# from .forms import contactForm
#,InitialTbllist


def profile_main_view(request):
    context = {}
    #template = 'common/profile_main_view.html'
    template = 'common/profile_main_view.html'
    # return render(request, template, context)
    if request.user.is_authenticated:
        return render(request, template, context)
    else:
        return render(request, 'account/login.html')

def project_access_request(request):
    current_user = request.user
    current_user_id = current_user.id
    proj_access_form = Project_access_Form(request.POST or None,
                                           initial= {'current_user_id': current_user_id} )
    return render(request, 'common/project_access_request.html', {
      'proj_access_form': proj_access_form})

def project_access_req_validate(request):
    requester_user = request.user
    requester_user_id = requester_user.id
    requester_email = request.user.email

    project_name = request.POST.get('project_name')
    Role = request.POST.get('Role')
    Additional_note = request.POST.get('Additional_note')
    project = Project.objects.get(project_name=project_name)


    # project = get_object_or_404(Project, pk=project.id)
    project_id = project.id
    project_owner_id = project.user_id
    project_owner_name = User.objects.get(id=project_owner_id)

    project_owner_email = []
    project_owner_email.append(project_owner_name.email)
    project_owner_email.append(request.user.email)

    projects_access_req = Project_access.objects.filter(requester_id=requester_user_id).\
                          filter(project_name_id=project_id).filter(access=False).\
                          values_list('project_name')

    projects_access_req_lst = []

    for s in projects_access_req:
        projects_access_req_lst.append(int(s[0]))

    if project_id in projects_access_req_lst:

        existing_access_id = Project_access.objects.filter(requester_id=requester_user_id).\
        filter(project_name_id=project_id).filter(access=False).values_list('id')
        access_id = []

        for s in existing_access_id:
            access_id.append(int(s[0]))
        print('access_id', access_id)

        for accss in access_id:
            accss_obj = Project_access.objects.get(pk=accss)
            accss_obj.requester = request.user
            accss_obj.project_name_id = project_id
            accss_obj.project_owner = project_owner_name
            accss_obj.project_owner_email = project_owner_name.email
            accss_obj.requester_email = request.user.email
            accss_obj.notes = Additional_note
            accss_obj.role = Role
            accss_obj.status = 'Pending'
            accss_obj.access = False
            accss_obj.save()

        context = {
            'project': project,
            # 'form': form,
            'error_message': 'Already submited the access request for the project:{}, send the mail notification to project owner:{}'.format(project_name, project_owner_name)
                    }
    else:
        access = Project_access(requester=request.user, project_name_id=project_id,
                                project_owner=project_owner_name,
                                project_owner_email = project_owner_name.email ,
                                requester_email = request.user.email, notes=Additional_note,
                                role=Role,status='Pending', access=False)
        access.save()

    # print('sending the email')
    subject = "Access request for the project:{}".format(project_name)
    message = "Hi {} , \n \
    Request you to kindly give access to the  project:{} \n \n \
    Thanks & Regards\n\
    {}".format(project_owner_name, project_name, requester_user)
    email_common(subject=subject, message=message, from_email=requester_email, recipient_list=project_owner_email)

    #return render(request,"common/project_access_req_view.html")
    projects = Project_access.objects.filter(requester=request.user)
    print('from validate project details: project.id:', project.id)
    return render(request, 'common/my_project_access_status.html', {'projects': projects})

    #return HttpResponse("Access Request Submited for the project: {}".format(project_name))


def my_project_access_status(request):

    if not request.user.is_authenticated:
        return render(request, 'account/login.html')

    elif request.user.is_superuser:
        projects = Project.objects.all()
        return render(request, 'common/my_project_access_status.html', {'projects': projects})

    else:
        # projects = Project_access.objects.filter(requester=request.user)
        projects_ids = Project_access.objects.filter(requester_id=request.user.id).values_list('project_name_id')
        access_id = []
        for id in projects_ids:
            access_id.append(int(id[0]))
        projects = Project.objects.filter(id__in=access_id)
        return render(request, 'common/my_project_access_status.html', {'projects': projects})

def project_access_status_detail(request, project_id):
    if not request.user.is_authenticated:
        return render(request, 'account/login.html')
    else:
        user = request.user
        project_owner_id = user.id
        project = get_object_or_404(Project, pk=project_id)
        print(project, type(project), ' from project_access_status_detail project_id:', project_id)
        return render(request, 'common/my_project_access_status_detail.html', {'project': project, 'user': user})

#only project
def project_access_req_view(request):
    if not request.user.is_authenticated:
        return render(request, 'account/login.html')

    elif request.user.is_superuser:
        #projects = Project.objects.all()
        projects = Project_access.objects.all()
        return render(request, 'common/project_access_req_view.html', {'projects': projects})

    else:
        projects = Project_access.objects.filter(project_owner_id=request.user)
        return render(request, 'common/project_access_req_view.html', {'projects': projects})

def project_access_req_view_detail(request, project_id):

    if not request.user.is_authenticated:
        return render(request, 'account/login.html')
    else:
        user = request.user
        project_owner_id = user.id
        access_id = []
        projects_ids = Project_access.objects.filter(id=project_id).values_list('project_name_id')

        for id in projects_ids:
            access_id.append(int(id[0]))
        access_id = access_id[0]
        print('project_access_req_view_detail first t project id :', project_id, 'projects_ids nex ', projects_ids, type(projects_ids))
        print('access_id', access_id, type(access_id))

        project = get_object_or_404(Project, pk=access_id)
        print(project, type(project), ' from project_access_status_detail project_id:', project_id)
        return render(request, 'common/project_access_req_view_detail.html', {'project': project, 'user': user})

def project_access_status_update(request, project_id, access_id, is_approve):
    print('request.POST:', request.POST, 'request.GET:', request.GET, request.GET.get)
    user = request.user
    project_owner_id = user.id
    project = get_object_or_404(Project, pk=project_id)
    accss_obj = Project_access.objects.get(pk=access_id)

    if is_approve == '0':
        print('Deleting/revoking the  the request:is_approve', is_approve)
        accss_obj.status = 'Pending'
        accss_obj.access = False
        accss_obj.save()
        # accss_obj.delete()
    elif is_approve == '1':
        print('Approving the request:is_approve', is_approve)
        accss_obj.status = 'Approved'
        accss_obj.access = True
        accss_obj.save()

    return render(request, 'common/project_access_req_view_detail.html', {'project': project, 'user': user})

def about_us(request):
    context = {}
    template = 'common/about_us.html'

    if not request.user.is_authenticated:
        return render(request, 'account/login.html')
    else:
        return render(request, template, context)

def successView(request):
    return HttpResponse('Success! Thank you for your message.')

###to redirect the blank or unwated page access to login page.
def login_redirect(request):
    if not request.user.is_authenticated:
        return render(request, 'account/login.html')
    else:
        return render(request, 'account/login.html')

def update_domain(request):
    current_site = Site.objects.get_current()
    display_name = current_site.name
    domain_name = current_site.domain

    if request.method == 'GET':
        form = domainForm(initial={'display_name': display_name, 'domain_name': domain_name })

    else:
        form = domainForm(request.POST)
        if form.is_valid():
            try:
                display_name = form.cleaned_data['display_name']
                domain_name = form.cleaned_data['domain_name']
                new_site_details = Site.objects.all()[0]
                new_site_details.domain = domain_name
                new_site_details.name = display_name
                new_site_details.save()
                # send_mail(domain_name, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Due to internal Error, Not able to update the domain or site name')
            return redirect('profile_setting')
    return render(request, "common/update_domain.html", {'form': form})

# project_filter
# def project_filter(request, filter_by):
#     if not request.user.is_authenticated():
#         return render(request, 'account/login.html')
#     else:
#         return render(request, 'account/login.html')
#         # try:
#         #     song_ids = []
#         #     for album in Album.objects.filter(user=request.user):
#         #         for song in album.song_set.all():
#         #             song_ids.append(song.pk)
#         #     users_songs = Song.objects.filter(pk__in=song_ids)
#         #     if filter_by == 'favorites':
#         #         users_songs = users_songs.filter(is_favorite=True)
#         # except Album.DoesNotExist:
#         #     users_songs = []
#         # return render(request, 'music/songs.html', {
#         #     'song_list': users_songs,
#         #     'filter_by': filter_by,
#         # })

# def current_project_list_view(request):
#     current_user = request.user
#     current_user_id = current_user.id
#     print('current_user_id', current_user_id, request.user)
#     print("session  logged in user:", request.user)
#     prj_list_with_no_access = Project_access.objects.exclude(user_id=current_user_id)
#     prj_list_with_access = Project_access.objects.filter(user_id=current_user_id)

#     prj_list_with_no_access1 = Project_access.objects.exclude(user_id=current_user_id)
#     data = [person.to_dict_json() for person in prj_list_with_no_access1]
#     print('prj_list_with_no_access1', data, type(prj_list_with_no_access1))

#     prj_list_with_access1 = Project_access.objects.filter(user_id=current_user_id)
#     # data1 = [person.to_dict_json() for person in prj_list_with_access1]
#     xx = [x for x in Project_access().__dict__.values() ]
#     print(request.user, 'prj_list_with_access1 xx', xx)

#     return HttpResponse('Success! Thank you for your message.')

#     # results = Model.objects.filter(x=5).exclude(a=true)
#     existing_table_list = Project.objects.all()
#     project = Project.objects.all()
#     return render(request, 'common/project_list_view.html',
#             {'project': project,
#             'prj_list_with_no_access': prj_list_with_no_access,
#             'prj_list_with_access': prj_list_with_access })





