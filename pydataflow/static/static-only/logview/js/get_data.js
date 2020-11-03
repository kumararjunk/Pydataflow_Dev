var xhr;
if (window.XMLHttpRequest) xhr = new XMLHttpRequest();      // all browsers except IE
else xhr = new ActiveXObject("Microsoft.XMLHTTP");      // for IE

xhr.open('GET', '/Users/arjunkumar/Desktop/notes2/pre-prod/front_end/PyDataFlow_Local/PyDataFlow/pydataflow/logs/2019-12-09/etl_mgmt_test/13_26_job_flow_job_name_test_etl_mgmt_script_2019-12-09-02:54:02.log', false);
xhr.onreadystatechange = function () {
    if (xhr.readyState===4 && xhr.status===200) {
        var div = document.getElementById('update');
        div.innerHTML = xhr.responseText;
    }
}
xhr.send();


