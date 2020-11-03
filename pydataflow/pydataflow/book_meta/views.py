from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.db.models import Q
from django.template import loader, RequestContext

from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import connection, transaction
# from django.db import transaction
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.views.generic.edit import FormMixin, FormView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
#import MySQLdb,
import sqlite3, csv, threading, time

from tablib import Dataset
from django import forms
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory, BaseFormSet
from meta.forms import ProjectForm, ProjectSpFormSet,SpFormupdate #, SpCreateForm
from meta.forms import DataSourceForm, ProjectDataSourceForm, ProjectDataSourceFormSet, ProjectEnvProjectFormSet


from meta.models import User, Project, DataSource, Spname, Tbllist, InitialTbllist
from meta.forms import Choose_dsn_Form, databaseObjectForm, DsnCreateForm


from django.template.loader import render_to_string

from .forms import SpCreateForm


from books.models import Book
from .forms import BookForm



def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_meta/book_list.html', {'books': books})

# book_list  --> sp_list

def sp_list(request, project_id):
    if not request.user.is_authenticated:
        return render(request, 'account/login.html')
    else:
        user = request.user
        project = get_object_or_404(Project, pk=project_id)
        return render(request, 'book_meta2/sp_list.html', {'project': project, 'user': user})





#save_book_form --> save_sp_form
def save_sp_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            sps = Spname.objects.all()
            data['html_book_list'] = render_to_string('book_meta2/includes/partial_book_list.html', {
                'sps': sps
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


# book_create --> sp_create
def sp_create(request):
    if request.method == 'POST':
        form = SpCreateForm(request.POST)
    else:
        form = SpCreateForm()
    return save_sp_form(request, form, 'book_meta2/includes/partial_sp_create.html')


#book_update --> sp_update

def sp_update(request, pk):
    sp = get_object_or_404(Spname, pk=pk)
    if request.method == 'POST':
        form = SpCreateForm(request.POST, instance=sp)
    else:
        form = SpCreateForm(instance=sp)
    return save_sp_form(request, form, 'book_meta2/includes/partial_sp_update.html')


#book_delete  --> sp_delete

def sp_delete(request, pk):
    sp = get_object_or_404(Spname, pk=pk)
    data = dict()
    if request.method == 'POST':
        sp.delete()
        data['form_is_valid'] = True
        sps = Spname.objects.all()
        data['html_book_list'] = render_to_string('book_meta2/includes/partial_sp_list.html', {
            'books': books
        })
    else:
        context = {'sp': sp}
        data['html_form'] = render_to_string('book_meta2/includes/partial_sp_delete.html', context, request=request)
    return JsonResponse(data)




    # return HttpResponse("Access Request Submited for the project:")






def save_book_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = Book.objects.all()
            data['html_book_list'] = render_to_string('book_meta/includes/partial_book_list.html', {
                'books': books
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
    else:
        form = BookForm()
    return save_book_form(request, form, 'book_meta/includes/partial_book_create.html')


    # return HttpResponse("Access Request Submited for the project:")

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
    else:
        form = BookForm(instance=book)
    return save_book_form(request, form, 'book_meta/includes/partial_book_update.html')


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True
        books = Book.objects.all()
        data['html_book_list'] = render_to_string('book_meta/includes/partial_book_list.html', {
            'books': books
        })
    else:
        context = {'book': book}
        data['html_form'] = render_to_string('book_meta/includes/partial_book_delete.html', context, request=request)
    return JsonResponse(data)
