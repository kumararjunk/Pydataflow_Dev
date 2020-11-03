from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.layout import Div, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.forms import ModelForm, inlineformset_factory
from django.forms import ModelChoiceField
from django.contrib.auth.models import User, Group

from .models import Project, Spname, Tbllist, DataSource, Env_variables, Env_variables_project
from .models import InitialTbllist

DATABASE_TYPES = ['oracle', 'sqlserver', 'teradata', 'mysql']
DATABASE_OBJECT_TYPES = ['None', 'Tables', 'Views', 'Stored_Proc']

class databaseObjectForm(forms.Form):
    DATABASE_OBJECT_TYPES =[("T", "Tables"), ("V", "Views"), ("S", "Stored_Proc")]
    db_object_type = forms.ChoiceField(choices=DATABASE_OBJECT_TYPES, label="Tables/View or Stored Proc", widget=forms.Select(), required=True)


class Choose_dsn_Form(forms.ModelForm):
    DATABASE_OBJECT_TYPES =[("T", "Tables"), ("V", "Views"), ("S", "Stored_Proc")]
    class Meta:
        model = DataSource
        fields = ["dsn_name"]

    def __init__(self, *args, **kwargs):
        super(Choose_dsn_Form, self).__init__(*args, **kwargs)
        # project_name_id = self.instance.project_name_id
        project_name_id = kwargs['initial']['project_id']

        self.fields['dsn_name']= forms.ModelChoiceField(queryset=DataSource.objects.filter(project_name_id = project_name_id).values_list('dsn_name',flat=True).distinct() )
        # self.fields['db_object_type'] = forms.ChoiceField(choices=DATABASE_OBJECT_TYPES, label="Tables/View or Stored Proc", widget=forms.Select(), required=True)


class myForm(forms.ModelForm):
    dsn_name = forms.ModelChoiceField(queryset=DataSource.objects.values_list('dsn_name',flat=True).distinct())

    class Meta:
        model = DataSource
        fields = ["dsn_name"]

#ProjectEnvForm   --> ProjectEnvProjectForm
#ProjectEnvFormSet  --> ProjectEnvProjectFormSet
####Environment varaibles form

class ProjectEnvProjectForm(ModelForm):
    class Meta:
        model = Env_variables_project
        exclude = ['user']

ProjectEnvProjectFormSet = inlineformset_factory(Project, Env_variables_project,
                                            form=ProjectEnvProjectForm, extra=1)


class EnvVariablesForm(ModelForm):
    class Meta:
        model = Env_variables
        exclude = ['user']

EnvVariablesFormSet = inlineformset_factory(Project, Env_variables_project,
                                            form=EnvVariablesForm, extra=1)







####Project forms used in ProjectUpdate/project_create
class ProjectForm(ModelForm):

    class Meta:
        model = Project
        # exclude = ()
        exclude = ['user']
        #fields = ['project_name', 'success_email', 'failure_email_ind', 'failure_email', 'is_active']

#####Project  Form for bulk update
class ProjectSpForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectSpForm, self).__init__(*args, **kwargs)
        self.fields['start_dt'] = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'MM-DD-YYYY or NULL'}))
        self.fields['end_dt'] = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'MM-DD-YYYY or NULL'}))
    class Meta:
        model = Spname
        # exclude = ()
        fields = ['project_name', 'dsn_name', 'report_name', 'sp_name', 'start_dt', 'end_dt', 'med_center', 'result_table', 'is_active']

ProjectSpFormSet = inlineformset_factory(Project, Spname,
                                            form=ProjectSpForm, extra=1)


class DsnCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # project_id = kwargs.pop('project_id','')
        super(DsnCreateForm, self).__init__(*args, **kwargs)
        # project_id = kwargs.pop('project_id', '1')
        if 'project_id' in kwargs:
            # project_id = int(kwargs.pop('project_id'))
            ### self.fields['dsn_name'].queryset = DataSource.objects.filter(project_name=project_id)
            self.fields['dsn_name'].queryset = DataSource.objects.filter(project_name='project_id')

        # self.fields['dsn_name'].queryset=DataSource.objects.filter(project_name=self.instance.project_name)

    class Meta:
        model = DataSource
        fields = ['dsn_name', 'db_host', 'db_user', 'db_pw', 'db_name', 'db_type',
         'db_param', 'db_port_no']

#####Data source Form for bulk update
class DataSourceForm(forms.ModelForm):
    db_pw = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = DataSource
        fields = ['dsn_name', 'db_host', 'db_user', 'db_pw', 'db_name', 'db_port_no','db_type', 'db_param']


class ProjectDataSourceForm(ModelForm):
    # db_pw = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = DataSource
        exclude = ['db_pw', 'dsn_status']

ProjectDataSourceFormSet = inlineformset_factory(Project, DataSource,
                                            form=ProjectDataSourceForm, extra=1)


class SpCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # project_id = kwargs.pop('project_id','')
        super(SpCreateForm, self).__init__(*args, **kwargs)
        # project_id = kwargs.pop('project_id', '1')
        if 'project_id' in kwargs:
            # project_id = int(kwargs.pop('project_id'))
            ### self.fields['dsn_name'].queryset = DataSource.objects.filter(project_name=project_id)
            self.fields['dsn_name'].queryset = DataSource.objects.filter(project_name='project_id')

        self.fields['start_dt'] = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'MM-DD-YYYY or NULL'}))
        self.fields['end_dt'] = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'MM-DD-YYYY or NULL'}))

    class Meta:
        model = Spname
        fields = ['project_name', 'dsn_name', 'report_name', 'sp_name', 'start_dt', 'end_dt', 'med_center', 'result_table', 'is_active']

class SpFormupdate(forms.ModelForm):
    class Meta:
        model = Spname
        #fields = ['project_name', 'dsn_name', 'report_name', 'sp_name', 'start_dt', 'end_dt', 'med_center', 'result_table', 'is_active']
        fields = ['project_name', 'dsn_name', 'report_name', 'sp_name', 'start_dt', 'end_dt', 'med_center', 'result_table', 'is_active']

    def __init__(self, *args, **kwargs):
        # id = kwargs.pop('tbllist_id','')
        super(SpFormupdate, self).__init__(*args, **kwargs)
        self.fields['dsn_name']=forms.ModelChoiceField(queryset=DataSource.objects.filter(project_name=self.instance.project_name))
        self.fields['start_dt'] = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'MM-DD-YYYY or NULL'}))
        self.fields['end_dt'] = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'MM-DD-YYYY or NULL'}))
        # self.fields['start_dt'].widget.attrs['placeholder'] = 'start_dt'

