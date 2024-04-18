$(document).ready(function () {
    $('#applicationsTable').DataTable({
        responsive: true, // Enable responsiveness
        "paging": true,           // Enable paging
        "searching": true,        // Enable search box
        "ordering": true,         // Enable sorting
        "info": true,              // Enable info display
        "lengthMenu": [10, 25, 50, 100], // Define available page lengths
        "pageLength": 100,         // Set default page length to 100
        "columnDefs": [{
            "targets": [0], // Replace 'column_index' with the index of the edit button column (starting from 0)
            "orderable": false        // Disable sorting for this column
        }]
    });
});