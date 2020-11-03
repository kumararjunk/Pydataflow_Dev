from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, inlineformset_factory
# from meta.models import Srcsystem, Tbllist, InitialTbllist

from meta.models import Project, Project_access


class Project_access_Form(forms.ModelForm):

    class Meta:
        model = Project
        fields = ["project_name"]

    def __init__(self, *args, **kwargs):
        super(Project_access_Form, self).__init__(*args, **kwargs)
        ROLE_TYPE =[("Master", "Master: Full Access"), ("Developer", "Developer: Add/Edit jobs"), ("Operator", "Operator:Only Execute jobs")]
        #project_name_id = kwargs['initial']['project_id']
        current_user_id = kwargs['initial']['current_user_id']
        proj_with_access = Project_access.objects.filter(requester_id=current_user_id).filter(access=True).values_list('project_name',flat=True).distinct()
        proj_with_access_lst = []
        for proj_id in proj_with_access:
            proj_with_access_lst.append(proj_id)

        proj_owner = Project.objects.filter(user_id=current_user_id).values_list('id',flat=True).distinct()

        for proj_id in proj_owner:
            proj_with_access_lst.append(proj_id)

        print('proj_with_access_lst :',proj_with_access_lst, type(proj_with_access_lst))

        if len(proj_with_access_lst) == 0:
            self.fields['project_name']= forms.ModelChoiceField(queryset=Project.objects.all().values_list('project_name',flat=True).distinct() )
        else:
            self.fields['project_name']= forms.ModelChoiceField(queryset=Project.objects.exclude(id__in=proj_with_access_lst).values_list('project_name',flat=True).distinct() )

        # self.fields['Email'] = forms.ChoiceField(choices=ROLE_TYPE, label="Role", widget=forms.Select(), required=True)
        self.fields['Role'] = forms.ChoiceField(choices=ROLE_TYPE, label="Role", widget=forms.Select(), required=True)
        self.fields['Additional_note'] = forms.CharField(widget=forms.Textarea, required=False)


# class Project_access_bulk_Form(ModelForm):
#     class Meta:
#         model = Project_access
#         # exclude = ()
#         fields = ['requester', 'project_name', 'project_owner', 'notes', 'role', 'status', 'access']

# ProjectaccessFormSet = inlineformset_factory(Project, Project_access,
#                                             form=Project_access_bulk_Form, extra=0)



class domainForm(forms.Form):
    display_name = forms.CharField(required=True, max_length=20)
    domain_name = forms.CharField(required=True, max_length=20)
    # domain_name = forms.CharField(required=False, max_length=100, help_text='100 character max.')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

##not used

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class contactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)




