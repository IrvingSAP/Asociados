$('#TDatAnalisis01').DataTable({
    
    searching: false,
    info: false,
    paging: false,
    scrollCollapse: true,
    scrollY: '350px',
    ordering: false,
    columnDefs: [
        {
            target: 4,
            visible: false,
            searchable: false,
            order: [4]
        },
        {
            target: 7,
            visible: false,
            searchable: false,
        }
    ]

});