from django.shortcuts import render, redirect
from core.models import SaldoCaja, MovimientoCaja, TablaSistema
from datetime import datetime
from datetime import date

# Create your views here.

######################### Presenta Socios ###################################
# Presento Socios
def selSocioCaja(request):
    yyyymmm = '2024-00'
    sCaja = SaldoCaja.objects.all().order_by('-id_Caja')
    print(sCaja)
    return render(request, 'caja/selSocioCaja.html', {'sCaja':sCaja})

######################### Consulta Caja ###################################
# Paga Int
def selCajaR(request, id):
    
    # Valores de Sistema
    vEstado = "M"
    vcodSis = "FECPRO"
    sTS = TablaSistema.objects.get(cod_Sistema = vcodSis)
    
    yyyymm = str(sTS.Valor_Sistema)

    mCaja = MovimientoCaja.objects.filter(yymm_Caja=id).order_by('-fec_AplicaN')
    return render(request, 'caja/selCajaR.html', {'mCaja':mCaja})

def selCajaM(request, id):
    
    # Valores de Sistema
    vEstado = "M"
    vcodSis = "FECPRO"
    sTS = TablaSistema.objects.get(cod_Sistema = vcodSis)
    
    yyyymm = str(sTS.Valor_Sistema)

    mCaja = MovimientoCaja.objects.filter(yymm_Caja=id).order_by('-fec_AplicaN')

    return render(request, 'caja/selCajaM.html', {'mCaja':mCaja})

def selCajaE(request, id):
    
    # Valores de Sistema
    vEstado = "M"
    vcodSis = "FECPRO"
    sTS = TablaSistema.objects.get(cod_Sistema = vcodSis)
    
    yyyymm = str(sTS.Valor_Sistema)

    mCaja = MovimientoCaja.objects.filter(yymm_Caja=id).order_by('-fec_AplicaN')

    return render(request, 'caja/selCajaE.html', {'mCaja':mCaja})
