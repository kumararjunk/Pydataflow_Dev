from django.contrib.auth.models import User, Group
from rest_framework import serializers
import datetime
from datetime import timedelta

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


from meta.models import Project, Processlog, Jobflow, Jobflowdetail


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

class ProcesslogdetailSerializer(serializers.ModelSerializer):
    jobflowname = JobflowSerializer()
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    elapsed_time = serializers.SerializerMethodField()
    end_time_check = serializers.SerializerMethodField()

    DT_RowId = serializers.SerializerMethodField()
    DT_RowAttr = serializers.SerializerMethodField()
    log_url = serializers.SerializerMethodField()

    def get_DT_RowId(self, processlog):
        return 'row_%d' % processlog.pk

    def get_DT_RowAttr(self, processlog):
        return {'data-pk': processlog.pk}

    def get_log_url(self, processlog):
        return '/log_detail/%d/' % processlog.pk #+ str(processlog.process_id)

    def get_elapsed_time(self, obj):

        if obj.status == "Executing":
            time_diff = datetime.datetime.now() - (obj.start_time.replace(tzinfo=None) + timedelta(hours=16))
            return str(timedelta(seconds=time_diff.seconds))

        else:
            time_diff = obj.end_time - obj.start_time
            return str(timedelta(seconds=time_diff.seconds))

    def get_end_time_check(self, obj):

        if obj.status == "Executing":
            # end_time_check = datetime.datetime.now() + obj.start_time.replace(tzinfo=None)
            return 'N/A' #obj.end_time.strftime("%Y-%m-%d %H:%M:%S")

        else:
            return (obj.end_time - timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
            # return obj.end_time.strftime("%Y-%m-%d %H:%M:%S") ####obj.end_time

    class Meta:
        model = Processlog
        fields = (

          'DT_RowId', 'DT_RowAttr',
          'process_id', 'jobflowname', 'project_job_name'
          ,'start_time', 'end_time',
          'elapsed_time', 'status', 'end_time_check', 'job_type', 'logfile' , 'log_url', 'id'
          ###3, 'project_name'

        )
