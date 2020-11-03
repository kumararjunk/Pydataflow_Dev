$(document).ready( function () {
  // $('#myTable1').DataTable();

  $('#myTable1').DataTable({
    dom: 'B<"clear">lfrtip',
    buttons: {
        name: 'primary',
        buttons: [ 'copy', 'csv', 'excel', 'pdf' ]
        }}
    );

  $('#myTable2').DataTable({
    "ajax": "/person/json/",
    "columns": [
      {"data": "name"},
      {"data": "email"},
      {"data": "phone"},
      {"data": "gender"}
    ]
  });
});


// <script>
//     $(document).ready( function () {
//     $('#table_id').DataTable({
//     dom: 'B<"clear">lfrtip',
//     buttons: {
//         name: 'primary',
//         buttons: [ 'copy', 'csv', 'excel', 'pdf' ]
//         }}
//     );
// } );
// </script>
