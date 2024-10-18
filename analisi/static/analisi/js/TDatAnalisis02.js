$('#TDatAnalisis01').DataTable({
    
    searching: false,
    info: false,
    paging: false,
    scrollCollapse: true,
    scrollY: '350px',
    ordering: false,
    "order": [[ 4 ]],
    buttons: [
                'copy', 'excel', 'pdf'
    ],
    columnDefs: [
        {
            target: 4,
            visible: false,
            searchable: false,
            order: [4]
        }
    ]

});