from django.shortcuts import render
from core.models import MaestroAsociado, PrestamoAsociado, PrestamosMovimiento

# Create your views here.

######################### Presenta Socios ###################################
# Presento Socios
def conSocio(request):
    MAsociados = MaestroAsociado.objects.all()
    return render(request, 'consultaSocio/conSocio.html', {'MAsociados':MAsociados})

######################### Prestamo Socio ###################################
# Presento Prestmos de Socio
def conSocPend(request, id):

    PPendientes = PrestamosMovimiento.objects.filter(estado_reg='PENDIENTE')
    socio = MaestroAsociado.objects.get(id_asociado=id)
    return render(request, 'consultaSocio/conSocPend.html', {'socio':socio,
                                                'PPendientes':PPendientes})

######################### Detalle Prestamo Socio ###################################
# Presento Detalle Prestamos de Socio
def conSocPendDet(request, id, codpre):

    #PPendientes = PrestamosMovimiento.objects.filter(id_Asociado=id).filter(cod_Prestamo=codpre)
    PPendientes = PrestamosMovimiento.objects.all()
    print(PPendientes)
    socio = MaestroAsociado.objects.get(id_asociado=id)
    print(id)
    print(codpre)

    return render(request, 'consultaSocio/conSocPendDet.html', {'socio':socio,
                                                'PPendientes':PPendientes})
    #return render(request, 'core/home.html')
