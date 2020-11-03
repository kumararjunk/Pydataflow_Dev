from import_export import resources
from .models import Srcsystem, Tbllist


from .models import Person

class PersonResource(resources.ModelResource):
    class Meta:
        model = Person

class SrcsystemResource(resources.ModelResource):
    class Meta:
        model = Srcsystem
        fields = ('src_name', 'src_host', 'src_user', 'src_pw', 'db_type', 'hdfs_dir', 'email_notification','ETL_schedule_time','is_active','max_num_of_threads')


class TbllistResource(resources.ModelResource):
    class Meta:
        model = Tbllist



