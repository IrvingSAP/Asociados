$('#TselSocioDP').DataTable({
    searching: false,
    info: false,
    paging: false,
    scrollCollapse: true,
    scrollY: '350px',
    ordering: false,
    "order": [[ 3 ]],
    buttons: [
                'copy', 'excel', 'pdf'
    ]
});