#!/usr/bin/python
#import MySQLdb,
import sqlite3, cx_Oracle
import argparse, os ,sys, logging, pathlib, time, subprocess, os.path, calendar
from shutil import copyfile
from django.conf import settings
from django.core.mail import send_mail
from collections import deque
from crontab import CronTab
#import pymssql

from django.shortcuts import render, get_object_or_404, render_to_response
from meta.models import User, Project, DataSource, Spname, Tbllist
# import pyodbc


def email_common(subject=None, message=None, from_email=None, recipient_list=None):
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False, auth_user=None, auth_password=None, connection=None,
        html_message=None)


