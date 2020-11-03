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
# from .forms import contactForm

from .forms import UserForm, NameForm, domainForm
from .forms import ProjectaccessFormSet
from common.forms import Project_access_Form

##, Type_of_accessForm

from django.core.mail import send_mail, BadHeaderError
#,InitialTbllist
from meta.models import Project, DataSource, Tbllist
from meta.models import Project_access
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.db import models

from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template

from .utils import *

def about_us(request):
    context = {}
    # template = 'account/login.html'
    template = 'common/about_us.html'

    if not request.user.is_authenticated:
        return render(request, 'account/login.html')
    else:
        # return render(request, 'account/login.html')
        return render(request, template, context)

### above view is tested:
def successView(request):
    return HttpResponse('Success! Thank you for your message.')

###to redirect the blank or unwated page access to login page.
def login_redirect(request):
    # return render(request, 'account/login.html')
    if not request.user.is_authenticated:
        print('case 1', request.user.is_authenticated, request.user)
    else:
        print('case 2', request.user.is_authenticated, request.user)
    if not request.user.is_authenticated:
        return render(request, 'account/login.html')
    else:
        return render(request, 'account/login.html')

def update_domain(request):
    current_site = Site.objects.get_current()
    display_name = current_site.name
    domain_name = current_site.domain
    # print("current_site.domain display, domain", current_site.name, current_site.domain)

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

def profile_main_view(request):
    context = {}
    #template = 'common/profile_main_view.html'
    template = 'common/profile_main_view.html'

    return render(request, template, context)
    if request.user.is_authenticated:
        return render(request, template, context)
    else:
        return render(request, 'account/login.html')

def project_access_request(request):
    current_user = request.user
    current_user_id = current_user.id
    proj_access_form = Project_access_Form(request.POST or None, \
        initial= {'current_user_id': current_user_id} )
    return render(request, 'common/project_access_request.html', { \
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

    # project_owner_object = User.objects.get(id=project_owner_id)
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
            print('****', s)
            access_id.append(int(s[0]))
        print('access_id', access_id)

        for accss in access_id:
            accss_obj = Project_access.objects.get(pk=accss)
            accss_obj.requester = request.user
            accss_obj.project_name_id = project_id
            accss_obj.project_owner = project_owner_name
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
        access = Project_access(requester=request.user, project_name_id=project_id, \
            project_owner=project_owner_name, notes=Additional_note, \
            role=Role,status='Pending', access=False)
        access.save()

    # print('sending the email')
    subject = "Access request for the project:{}".format(project_name)
    message = "Hi {} , \n \
    Request you to kindly give access to the  project:{} \n \n \
    Thanks & Regards\n\
    {}".format(project_owner_name, project_name, requester_user)
    email_common(subject=subject, message=message, from_email=requester_email, recipient_list=project_owner_email)

    return render(request,"common/project_access_req_view.html")
    #return redirect(project_access_request)

    #return HttpResponse("Access Request Submited for the project: {}".format(project_name))
    #return HttpResponse('Success! Thank you for your message.')


#to display all the project with access:
def project_access_req_view(request):
    if not request.user.is_authenticated:
        return render(request, 'account/login.html')

    elif request.user.is_superuser:
        projects = Project.objects.all()
        return render(request, 'common/project_access_req_view.html', {'projects': projects})

    else:
        projects = Project.objects.filter(user=request.user)
        return render(request, 'common/project_access_req_view.html', {'projects': projects})



def project_access_status(request, project_id):
    if not request.user.is_authenticated:
        return render(request, 'account/login.html')
    else:
        user = request.user
        project_owner_id = user.id
        project = get_object_or_404(Project, pk=project_id)
        print(project, type(project))
        return render(request, 'common/access_detail.html', {'project': project, 'user': user})



def project_access_status_update(request, project_id, access_id, is_approve):
    print('*'*100)
    print('arjun',request.POST.get('form-id'), request.POST)
    print('kumar',request.POST.get('lr_action'), request.POST)
    print('tmp1',request.POST.get('tmp1'), request.POST)
    print('tmp',request.POST.get('tmp'), request.POST)

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

    return render(request, 'common/access_detail.html', {'project': project, 'user': user})




class Project_accessview_update(UpdateView):
    pk_url_kwarg = "project_id"
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True

    model = Project
    fields = ['project_name']
    template_name = 'common/project_access_update.html'

    def get_success_url(self):

        return reverse_lazy('common:project_access_req_view')
        # return reverse_lazy('common:project_access_status', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        data = super(Project_accessview_update, self).get_context_data(**kwargs)
        if self.request.POST:
            data['datasources'] = ProjectaccessFormSet(self.request.POST, instance=self.object)
        else:
            data['datasources'] = ProjectaccessFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        datasources = context['datasources']
        with transaction.atomic():
            self.object = form.save()

            if datasources.is_valid():
                datasources.instance = self.object
                datasources.save()
        return super(Project_accessview_update, self).form_valid(form)





# project_filter
def project_filter(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'account/login.html')
    else:
        return render(request, 'account/login.html')
        # try:
        #     song_ids = []
        #     for album in Album.objects.filter(user=request.user):
        #         for song in album.song_set.all():
        #             song_ids.append(song.pk)
        #     users_songs = Song.objects.filter(pk__in=song_ids)
        #     if filter_by == 'favorites':
        #         users_songs = users_songs.filter(is_favorite=True)
        # except Album.DoesNotExist:
        #     users_songs = []
        # return render(request, 'music/songs.html', {
        #     'song_list': users_songs,
        #     'filter_by': filter_by,
        # })

def current_project_list_view(request):
    current_user = request.user
    current_user_id = current_user.id
    print('current_user_id', current_user_id, request.user)
    print("session  logged in user:", request.user)
    prj_list_with_no_access = Project_access.objects.exclude(user_id=current_user_id)
    prj_list_with_access = Project_access.objects.filter(user_id=current_user_id)

    prj_list_with_no_access1 = Project_access.objects.exclude(user_id=current_user_id)
    data = [person.to_dict_json() for person in prj_list_with_no_access1]
    print('prj_list_with_no_access1', data, type(prj_list_with_no_access1))

    prj_list_with_access1 = Project_access.objects.filter(user_id=current_user_id)
    # data1 = [person.to_dict_json() for person in prj_list_with_access1]
    xx = [x for x in Project_access().__dict__.values() ]
    print(request.user, 'prj_list_with_access1 xx', xx)

    return HttpResponse('Success! Thank you for your message.')

    # results = Model.objects.filter(x=5).exclude(a=true)
    existing_table_list = Project.objects.all()
    project = Project.objects.all()
    return render(request, 'common/project_list_view.html',
            {'project': project,
            'prj_list_with_no_access': prj_list_with_no_access,
            'prj_list_with_access': prj_list_with_access })


# def project_list(request):

#     project = get_object_or_404(Project, pk=project_id)
    project_d = Project.objects.get(pk=project_id).__dict__
    project_id = project_d['id']
    request.session['project_id'] = project_id
    current_user = request.user
    user_id = current_user.id
    #getting the dsn name from form/html & #Geting the dsn_id from
    dsn_name = request.POST.get('dsn_name')

    if dsn_name is None:
        dsn_name = request.session['dsn_name']
    else:
        request.session['dsn_name'] = dsn_name

    dsn_id = [ d.id for d in DataSource.objects.filter(dsn_name__exact=dsn_name,project_name_id__exact=project_id) ][0]

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

    all_initial_tables = InitialTbllist.objects.filter(user_id=request.user).filter(project_name_id=project_id).filter(dsn_name_id = dsn_id).filter(table_type = db_object_type)
    existing_table_list = Tbllist.objects.filter(user_id=request.user).filter(project_name_id=project_id).filter(dsn_name_id = dsn_id).filter(table_type = db_object_type)

    # for table in existing_table_list:
    #     print(table.table_name)
    # remove duplicate items from list
    # mylist = list(dict.fromkeys(mylist))

    if 'new_tbls' in request.POST and len(request.POST.getlist('new_tbls')) > 0:
        #import raw tables
        new_tbl_raw = request.POST.getlist('new_tbls',default=None)

        existing_table_list_all = []
        for tbllist in existing_table_list:
            existing_table_list_all.append(tbllist.table_name)

        new_tbl_raw = [(table_name, table_name, db_object_type, 'sqoop', '', '', '',
                        'N', dsn_id, project_id, user_id, 1) \
                        for table_name in new_tbl_raw if table_name \
                        not in existing_table_list_all]

        sqlite_conn = sqlite_db_connection()
        cur_sqlite = sqlite_conn.cursor()

        insert_statement = ("INSERT INTO meta_Tbllist (table_name, result_table, table_type, import_utility, custom_cmd, additional_param, etl_sch_time, execution_flag, dsn_name_id, project_name_id, user_id, priority_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);")
        print("Info:refresh_report_monitor:Inserting data into sqlite db", insert_statement)
        cur_sqlite.executemany(insert_statement, new_tbl_raw)
        sqlite_conn.commit()
        sqlite_conn.close()
        #refreshing the table list and redirecting the page:
        existing_table_list = Tbllist.objects.filter(user_id=request.user).filter(project_name_id=project_id).filter(dsn_name_id = dsn_id).filter(table_type = db_object_type)
        return render(request, 'meta/select_src_tables.html', {'project': project, 'all_initial_tables': all_initial_tables, 'existing_table_list': existing_table_list })

    elif 'delete_tble_list[]' in request.POST and len(request.POST.getlist('delete_tble_list[]')) > 0:
        # delete_tble_list = tuple(request.POST.getlist('delete_tble_list[]',default=None))
        delete_tble_list = request.POST.getlist('delete_tble_list[]',default=None)
        db_object_type_str = "'" + db_object_type + "'"
        sqlite_conn = sqlite_db_connection()
        delete_stmt = "Delete from meta_Tbllist where project_name_id = {} and dsn_name_id = {} \
                      and table_type = {} and table_name in (%s)\
                     ".format(project_id, dsn_id, db_object_type_str)

        query_string = delete_stmt % ','.join(['?'] * len(delete_tble_list))
        sqlite_conn.execute(query_string, delete_tble_list)
        sqlite_conn.commit()
        sqlite_conn.close()
        #refreshing the table list and redirecting the page:
        existing_table_list = Tbllist.objects.filter(user_id=request.user).filter(project_name_id=project_id).filter(dsn_name_id = dsn_id).filter(table_type = db_object_type)
        return render(request, 'meta/select_src_tables.html', {'project': project, 'all_initial_tables': all_initial_tables, 'existing_table_list': existing_table_list })

    else:
        pass

    dsn_conn = test_dsn_generic(**dsn_details)
    if dsn_conn[1] == 'success':
        #importing the tables using the DSN.
        get_data_using_dsn_generic_util(**dsn_details)
        tables_count = InitialTbllist.objects.filter(user_id=request.user).filter(project_name_id=project_id).filter(dsn_name_id = dsn_id).filter(table_type = db_object_type).count()

        if tables_count == 0:
            error_message = 'No ' + DATABASE_OBJECT_DICT[db_object_type] + ' in Database: ' + dsn_details['db_name']
            messages.info(request, error_message)
            return render(request, 'meta/select_src_tables.html', {'project': project, 'all_initial_tables': all_initial_tables, 'existing_table_list': existing_table_list })
        else:
            return render(request, 'meta/select_src_tables.html', {'project': project, 'all_initial_tables': all_initial_tables, 'existing_table_list': existing_table_list })
    else:
        error_message = 'Error Connecting Rdbms using DSN: ' + dsn_name + ' Detailed Error Msg: ' + str(dsn_conn[2])
        # return JsonResponse({'Failure': error_message})
        messages.info(request, error_message)
        return redirect('meta:select_dsn', project_id=project_id)


####################################################################################################
# def login_user(request):
#     if request.method == "POST":
#         print("post 3066")
#         print()
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 projects = Project.objects.filter(user=request.user)
#                 return render(request, 'common/index.html', {'projects': projects})
#             else:
#                 return render(request, 'account/login.html', {'error_message': 'Your account has been disabled'})
#         else:
#             return render(request, 'account/login.html', {'error_message': 'Invalid login'})
#     return render(request, 'account/login.html')

####################################################################################################
# def emailView(request):
#     if request.method == 'GET':
#         form = contactForm()
#     else:
#         form = contactForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             from_email = form.cleaned_data['from_email']
#             message = form.cleaned_data['message']
#             try:
#                 send_mail(subject, message, from_email, ['admin@example.com'])
#             except BadHeaderError:
#                 return HttpResponse('Invalid header found.')
#             return redirect('success')
#     return render(request, "common/email_test_can_be_deleted.html", {'form': form})

# def base_old(request):
#     context = {}
#     # template = 'common/base_only.html'
#     template = 'common/base_common.html'
#     return render(request, template, context)

# def base_new(request):
#     context = {}
#     # template = 'account/base_common_a.html'
#     template = 'common/base.html'
#     return render(request, template, context)

# def DsnView(request, project_id):
#     project = get_object_or_404(Project, pk=project_id)
#     return render(request, 'meta/project_dsn_view.html', {'project': project})

# @login_required
# uncomment it

# def home(request):
#     context = {}
#     template = 'common/home.html'
#     return render(request, template, context)

# def fade(request):
#     context = {}
#     template = 'common/fade.html'
#     return render(request, template, context)

# Srcsystem -->Project
# srcsystem  ---> project
# srcsystems --> projects
# src_name  --> project_name
#SrcSystemForm -->ProjectForm
