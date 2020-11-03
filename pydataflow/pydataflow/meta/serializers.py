from rest_framework import serializers
from meta.models import Project, Processlog, Jobflow, Jobflowdetail, Spname, Script, Tbllist
# from meta.models import HistoricalProject
import datetime
from datetime import timedelta

###advance search
class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = (
            'id', 'project_name'
        )

        datatables_always_serialize = ('id',)

class JobflowSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    project_name = ProjectSerializer()

    class Meta:
        model = Jobflow
        fields = (
            'id', 'jobflowname', 'project_name'
        )

        datatables_always_serialize = ('id',)

# new
class JobflowdetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    project_name = ProjectSerializer()

    class Meta:
        model = Jobflow
        fields = (
            'id', 'project_name', 'jobflowname', 'project_job_name', 'job_name'
        )

        datatables_always_serialize = ('id',)

# ProjectobjectSerializer
class ProjectJobflowdetailSerializer(serializers.ModelSerializer):
    DT_RowId = serializers.SerializerMethodField()
    DT_RowAttr = serializers.SerializerMethodField()
    jobflowname = JobflowSerializer(required=False)
    project_job_name = serializers.SerializerMethodField(required=False)
    job_name = serializers.SerializerMethodField(required=False)
    job_type = serializers.SerializerMethodField(required=False)

    def get_queryset(self):
        return Jobflowdetail.objects.all()

    def get_DT_RowId(self, processlog):
        return 'row_%d' % processlog.pk

    def get_DT_RowAttr(self, processlog):
        return {'data-pk': processlog.pk}

    def get_project_job_name(self, obj):
        return obj.project_job_name

    def get_job_name(self, obj):
        return obj.job_name

    def get_job_type(self, obj):
        return obj.job_type

    class Meta:
        #model = Processlog
        model = Jobflowdetail
        fields = ('DT_RowId', 'DT_RowAttr'
          ,'jobflowname' , 'project_job_name', 'job_name'
          ,'job_type'
          )

class SpnameSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # project_name = ProjectSerializer()

    class Meta:
        model = Spname
        fields = ['id'] # , 'project_name'] #'job_type' ,'report_name', 'sp_name' ,

        datatables_always_serialize = ('id',)




class JobflowSerializer2(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    project_name = ProjectSerializer()

    class Meta:
        model = Jobflow
        fields = (
            'id', 'jobflowname', 'project_name'
        )

        datatables_always_serialize = ('id',)

class JobflowdetailSerializer2(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    project_name = ProjectSerializer()

    class Meta:
        model = Jobflowdetail
        fields = (
            'id', 'project_name', 'jobflowname', 'project_job_name', 'job_name'
        )

        datatables_always_serialize = ('id',)

class ProjectSpnameSerializer(serializers.ModelSerializer):
    DT_RowId = serializers.SerializerMethodField()
    DT_RowAttr = serializers.SerializerMethodField()
    project_name = ProjectSerializer()
    job_type = serializers.SerializerMethodField(required=False)
    report_name = serializers.SerializerMethodField()
    sp_name = serializers.SerializerMethodField()
    # project_name = serializers.SerializerMethodField()

    # jobflowname = JobflowdetailSerializer2(required=False)
    # retry after creating the project fk in joblfowdetail
    jobflowdetailed_id = serializers.SerializerMethodField()

    def get_queryset(self):
        #return Spname.objects.all()
        return Spname.objects.filter(id=35)

    def get_DT_RowId(self, spname):
        return 'row_%d' % spname.pk

    def get_DT_RowAttr(self, spname):
        return {'data-pk': spname.pk}

    def get_report_name(self, obj):
        return obj.report_name

    def get_sp_name(self, obj):
        return obj.sp_name

    def get_job_type(self, obj):
        return obj.job_type


    def get_jobflowdetailed_id(self, obj):
        object_id = obj.pk
        if object_id:
            #jobflowdetailed_id_var = Jobflowdetail.objects.filter(object_id=object_id).values('jobflowname')\
            jobflowdetailed_id_list = Jobflowdetail.objects.filter(object_id=object_id).filter(job_type='Stored_Proc')\
            .values_list('jobflowname', flat=True).distinct()

            jobflowname_list = Jobflow.objects.filter(pk__in=jobflowdetailed_id_list).values_list('jobflowname', flat=True).distinct()
            jobflowname_list_dict = Jobflow.objects.filter(pk__in=jobflowdetailed_id_list).values_list('jobflowname', 'pk').distinct()

            jobflownames_unique = []

            jobflownames_dict_str = ''
            for i in jobflowname_list_dict:
                # print('jobflowname:', i[0], 'jobflowpk', i[1])
                if i[0] not in jobflownames_unique:
                    jobflownames_unique.append(i[0])
                    jobflownames_dict_str += i[0] + ',' + str(i[1]) + ';'

            if not jobflownames_unique:
                jobflownames_dict_str = 'None'
            else:
                jobflownames_dict_str
            return jobflownames_dict_str




    class Meta:
        model = Spname
        fields = ('DT_RowId', 'DT_RowAttr','report_name', 'sp_name' ,'job_type'
          ,'project_name'
          #,'jobflowname'
          ,'jobflowdetailed_id'

          )

