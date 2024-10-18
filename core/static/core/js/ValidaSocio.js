$(document).ready(function() {
    $('#FormCrud').on('submit', function(event) {
        var valor = $('#txtEstado').val();
        if (valor !== 'I' && valor !== 'A') {
            alert('Error... Valor permitido para Estado ="A/I".');
            event.preventDefault(); // Evita que el formulario se envíe
        }
    });
});