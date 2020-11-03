from django import forms

from books.models import Book
from meta.models import Spname


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'publication_date', 'author', 'price', 'pages', 'book_type' )




class SpCreateForm(forms.ModelForm):
    class Meta:
        model = Spname
        fields = ('project_name', 'dsn_name', 'report_name', 'sp_name', 'start_dt', 'end_dt', 'med_center', 'result_table', 'is_active' )


# class SpCreateForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(SpCreateForm, self).__init__(*args, **kwargs)
#         if 'project_id' in kwargs:
#             project_id = int(kwargs.pop('project_id'))
#             self.fields['dsn_name'].queryset = DataSource.objects.filter(project_name='project_id')

#     class Meta:
#         model = Spname
#         fields = ['project_name', 'dsn_name', 'report_name', 'sp_name', 'start_dt', 'end_dt', 'med_center', 'result_table', 'is_active']


# class Spname(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
#     project_name = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)
#     dsn_name = models.ForeignKey(DataSource, on_delete=models.CASCADE, default=1)
#     report_name = models.CharField(max_length=100)
#     sp_name = models.CharField(max_length=100)
#     start_dt = models.CharField(max_length=50, blank=True, default='NULL')
#     end_dt = models.CharField(max_length=50, blank=True, default='NULL')
#     med_center = models.CharField(max_length=100, blank=True, default='NULL')
#     result_table = models.CharField(max_length=50)
#     additional_param = models.CharField(max_length=400, blank=True, default='NULL')
#     etl_sch_time = models.CharField(max_length=50,  blank=True, default='')
#     priority_id = models.SmallIntegerField(max_length=1, default=1)


