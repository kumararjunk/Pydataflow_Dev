#!/bin/sh

###################################script for clob and non partiotioned#########################
#################################################################################################
# Program     : to execute SP in oracle db
# Description : This shell script execute the stored proc in oracle and return the output in file
# Parameters  : 0
#
# Date        Author                Project#  Modification
# ==========  ====================  ========  ==================================
# 06/02/2015  Kumar, Arjun        kpit     Created
#for incremental tables converted oracle script

if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters, expecting stored proc file and result_table name"
fi


export LD_LIBRARY_PATH=/appdata/middleware/oracle_instant_client/instantclient_12_2

__tmp_sp_script=$1
report_name=$2
result_table=$3


echo ${__tmp_sp_script}
temp_path=`dirname ${__tmp_sp_script}`
# echo "tmp script used for execution:${temp_path}"
# echo "logfile path: ${temp_path}"

cat ${__tmp_sp_script}

echo "Detailed Oracle Execution Log"

hdfs_raw_dir=/ttg/microbiology/database/td2ex_mlab_report/

#/appdata/middleware/oracle_instant_client/instantclient_12_2/sqlplus NC_RLTGRPT_EXT[nc_group_rltg]/Report16@'(description=(address=(protocol=tcp)(host=scan-nzepc01f01db001x.nndc.kp.org)(port=1571))(connect_data=(service_name=PRODNCM_USR.nndc.kp.org)))' @${__tmp_sp_script}


# /appdata/middleware/oracle_instant_client/instantclient_12_2/sqlplus NC_RLTGRPT_EXT[nc_group_rltg]/Report16@'(description=(address=(protocol=tcp)(host=172.18.75.169)(port=1521))(connect_data=(service_name=PDB_NCWITS3.nndc.kp.org)))' @${__tmp_sp_script}

#old
# /appdata/middleware/oracle_instant_client/instantclient_12_2/sqlplus NC_RLTGRPT_EXT[nc_group_rltg]/Report16@'(description=(address=(protocol=tcp)(host=scan-qancal.appl.kp.org)(port=1521))(connect_data=(service_name=NCPSUP_USR.nndc.kp.org)))' @${__tmp_sp_script}


/appdata/middleware/oracle_instant_client/instantclient_12_2/sqlplus NC_RLTGRPT_EXT[nc_group_rltg]/Report16@'(description=(address=(protocol=tcp)(host=scan-nzepc01f01db001x.nndc.kp.org)(port=1571))(connect_data=(service_name=PRODNCM_EXT.nndc.kp.org)))' @${__tmp_sp_script}

sleep 5;

record_count=`cat ${temp_path}/${report_name}_data.txt | wc -l`
error_chk=`cat ${temp_path}/${report_name}_data.txt|tail -50|grep "ERROR"`
ora_chk=`cat ${temp_path}/${report_name}_data.txt|tail -50|grep "ORA-"`
error_content=`cat ${temp_path}/${report_name}_data.txt | tail -50`


echo "Record Count:$record_count"

if [[ $record_count -gt 10 ]];
then
    hadoop fs -rm ${hdfs_raw_dir}${result_table}/*
    hadoop fs -put ${temp_path}/${report_name}_data.txt ${hdfs_raw_dir}${result_table}/
    #echo "removing the file after moving into hadoop"
    #sleep 1;
    #rm -f ${temp_path}/${report_name}_data.txt

else
    # echo "stored_proc:nc_group_rltg.${sp_name}, has processed these records:$record_count "
    if [ -z $error_chk ] && [ -z $ora_chk ];
    then
        echo "stored proc executed successfully, but it generated less then 10 records and there were no errors"

        #echo "stored_proc:nc_group_rltg.${sp_name}, was executed successfully, But it processed $record_count Records.

       #" | mailx -s "Dev:Warning:$record_count Records processed by Stored Proc for Report no: ${report_name}" -r arjun.kumar@kp.org

    else
        #echo ${error_content}"stored_proc:nc_group_rltg.${sp_name}, has failed,
        #Please refer to the etl management log folder for the detailed log." | mailx -s "Dev:Failed:Failed in executing stored proc for report ${report_name}" -r arjun.kumar@kp.org,

        exit 9

    fi;
fi;


