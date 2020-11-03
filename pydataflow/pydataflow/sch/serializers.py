from rest_framework import serializers
from meta.models import Project, Processlog, Jobflow, Jobflowdetail, Sch
import datetime
from datetime import timedelta

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
            'id', 'jobflowname' , 'project_name'
        )

        datatables_always_serialize = ('id',)

class JobflowdetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    jobflowname = JobflowSerializer()

    class Meta:
        model = Jobflowdetail
        fields = (
            'id', 'jobflowname', 'project_job_name'
        )

        datatables_always_serialize = ('id',)


    # def get_queryset(self):
    #     return Sch.objects.filter(job_type="Job Flow")

    # def get_queryset(self):
    #     return Sch.objects.filter(pk=53)

    # def get_DT_RowId(self, sch):
    #     return '%d' % sch.pk

    # def get_DT_RowAttr(self, sch):
    #     return {'data-pk': sch.pk}

class ScheduleSerializer(serializers.ModelSerializer):
    # DT_RowId = serializers.SerializerMethodField()
    # DT_RowAttr = serializers.SerializerMethodField()
    project_name = ProjectSerializer()
    jobflowname = JobflowSerializer()
    jobflowdetail = JobflowdetailSerializer()

    job_type = serializers.SerializerMethodField()
    sch_type = serializers.SerializerMethodField()
    create_time = serializers.SerializerMethodField()
    etl_sch_time = serializers.SerializerMethodField()
    delete_cron_url = serializers.SerializerMethodField()

    job_name = serializers.SerializerMethodField()

    def get_queryset(self):
        return Sch.objects.all()

    # def get_DT_RowId(self, sch):
    #     return '%d' % sch.pk

    # def get_DT_RowAttr(self, sch):
    #     return {'data-pk': sch.pk}

    def get_job_type(self, obj):
        return obj.job_type

    def get_sch_type(self, obj):
        return obj.sch_type

    def get_create_time(self, obj):
        return obj.create_time

    def get_etl_sch_time(self, obj):
        return obj.etl_sch_time

    def get_delete_cron_url(self, obj):
        return obj.delete_cron_url

    def get_job_name(self, obj):
        return obj.job_name

    class Meta:
        model = Sch
        fields = (
          # 'DT_RowId', 'DT_RowAttr',
          'project_name', 'jobflowname',
          'jobflowdetail'
          , 'job_type',
          'sch_type', 'create_time', 'etl_sch_time',
          'delete_cron_url',
          'job_name'

        )

