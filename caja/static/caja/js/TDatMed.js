$('#TDatCaja').DataTable({
    
    searching: false,
    info: false,
    paging: false,
    scrollCollapse: true,
    scrollY: '450px',
    ordering: false,
    columnDefs: [
        {
            target: 5,
            visible: false,
            searchable: false,
            order: [4]
        },
    ]
});