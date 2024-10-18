from django.shortcuts import render, redirect
from core.models import SaldoCaja, TablaSistema
from datetime import datetime
from datetime import date

# Create your views here.

######################### Presenta Socios ###################################
# Presento Socios
def cierreCaja(request):

    # Saldo de Caja
    vEstado = "M"
    sCaja = SaldoCaja.objects.get(estadoCaja = vEstado)
    return render(request, 'proceso/cierreCaja.html', {'sCaja':sCaja})

def updCierreCaja(request):
    VYYMM = request.POST['txtFecproF']
    vValEnt = request.POST['txtValEnt']

    # Si el usuario presiono cancelar no entra
    if vValEnt == 'True':

        print('Cancele')
        print('valor ValEnt' , vValEnt)
        #Actualizo la tabla de Sistemas
        FPRO = 'FECPRO'
        vSistema = TablaSistema.objects.get(cod_Sistema = FPRO)
        vSistema.Valor_Sistema = VYYMM
        vSistema.save()

        # Saldo de Caja - Actualizo registro actual
        vEstado = "M"
        sCaja = SaldoCaja.objects.get(estadoCaja = vEstado)
        SFC = sCaja.salFinCaja
        sCaja.estadoCaja = 'H'
        sCaja.save()

        # Caja - Creo Nuevo Registro
        cCaja = SaldoCaja.objects.create(
        estadoCaja = "M" , yymmCaja = VYYMM , salIniCaja = SFC,
        salidaCaja = 0, entradaCaja = 0 , salFinCaja = SFC
        )

    return redirect('home')