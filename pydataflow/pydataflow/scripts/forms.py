
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.layout import Div, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.forms import ModelForm, inlineformset_factory
from django.forms import ModelChoiceField, ChoiceField
from django.contrib.auth.models import User, Group

from meta.models import Project, Spname, Tbllist, DataSource, Env_variables
from meta.models import InitialTbllist, Script, Jobflow, Jobflowdetail

#DATABASE_OBJECT_TYPES =[("T", "Tables"), ("V", "Views"), ("S", "Stored_Proc")]

class Choose_obj_Form(forms.Form):
    DATABASE_OBJECT_TYPES =[("Table", "Table"), ("Stored_Proc", "Stored_Proc"), ("Shell_Script", "Shell_Script")]
    job_type = forms.ChoiceField(choices=DATABASE_OBJECT_TYPES, label="Tables/Stored Proc/Shell Scripts", widget=forms.Select(), required=True)


class JobflowForm(ModelForm):
    class Meta:
        model = Jobflow
        exclude = ['user', 'project_name', 'object_id', 'job_type']

JobflowDetailFormSet = inlineformset_factory(Jobflow, Jobflowdetail,
                                            form=JobflowForm, extra=0)


class JobflowDetailFormUpdate(forms.ModelForm):

    class Meta:
        model = Jobflowdetail
        exclude = ['user', 'jobflowname', 'project_job_name', 'job_type', 'object_id']


class ScriptCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ScriptCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Script
        fields = ['job_name', 'script_path_name', 'additional_param', 'priority_id', 'is_active']


class ScriptUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ScriptUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Script
        fields = ['script_path_name', 'additional_param', 'priority_id', 'is_active']

    #'job_name',






