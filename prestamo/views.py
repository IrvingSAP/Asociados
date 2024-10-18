from django.shortcuts import render, redirect
from core.models import MaestroAsociado, PrestamoAsociado, SaldoCaja, MovimientoCaja, PrestamosMovimiento, TablaSistema
from datetime import datetime
from datetime import date

# Create your views here.

# ###################### FUNCIONES   #####################################

def eli_char_fec(c1,valor):
    valor = "".join(valor.split(c1))
    return valor 

# Reemplaza caracteres
def repl_char(char1,char2,origen):
    origen = origen.replace(char1,char2)
    return origen

# Redondedo 2 decimales
def dos_dcimales(valor1):
    return round(valor1, 2)

######################### Presenta Socios ###################################
# Presento Socios
def selSocio(request):
    MAsociados = MaestroAsociado.objects.all()
    return render(request, 'prestamo/selSocio.html', {'MAsociados':MAsociados})

######################### Creo Prestamo ###################################
# Creo Prestamo-Prento Panta de Entrada
def creaPrestamo(request, id):
    prestamo = PrestamoAsociado.objects.get(id_asociado=id)
    socio = MaestroAsociado.objects.get(id_asociado=id)
    return render(request, 'prestamo/creaPrestamo.html', {'socio':socio,
                                                          'prestamo':prestamo})

# Prestamo , Adiciono y Actualizo Datos
def registraPrestamo(request):
    aid = request.POST ['txtid_asociado']
    vnombre = request.POST['txtnombre']
    vCPrestamos = request.POST ['txtCPrestamos']
    vAPrestamos = request.POST ['txtAPrestamos']
    vSActual = request.POST ['txtSActual']
    vMonto = request.POST['txtmontPrestamo']
    vfecini = request.POST['txtFecIni']
    vfecfin = request.POST['txtFecFin']
    vobserva = request.POST['txtObserva']

    vValEnt = request.POST['txtValEnt']

    # Si el usuario presiono cancelar no entra
    if vValEnt == 'True':
        vRegistroN = datetime.now().strftime("%Y%m%d")
        vRegistroN = int(vRegistroN)
        vfecinin = int(eli_char_fec('-',vfecini))
        vfecfinn = int(eli_char_fec('-',vfecfin))

        vSActual = repl_char(',','.',vSActual)
        vSActual = float(vSActual)
        vSActual = dos_dcimales(vSActual)

        vMonto = repl_char(',','.',vMonto)
        vMonto = float(vMonto)
        vMonto = dos_dcimales(vMonto)

        vCPrestamosI = int(vCPrestamos)
        vAPrestamosI = int(vAPrestamos)
        vSActualI = vSActual + vMonto

        # Actualizo PrestamosSocio
        pSocio = PrestamoAsociado.objects.get(id_asociado = aid)
        pSocio.cantPrestamos = vCPrestamosI + 1
        pSocio.actPrestamos = vAPrestamosI + 1
        pSocio.saldoPrestamo = vSActualI
        pSocio.ultPrestamo = vfecini
        if pSocio.mayPrestamos < vMonto:
            pSocio.mayPrestamos = vMonto

        pSocio.save()

        # Valores de Sistema
        vEstado = "M"
        vcodSis = "FECPRO"
        sTS = TablaSistema.objects.get(cod_Sistema = vcodSis)
        yyyymm = str(sTS.Valor_Sistema)

        # Saldo de Caja
        try:
            sCaja = SaldoCaja.objects.get(estadoCaja = vEstado)
        except:
            cCaja = SaldoCaja.objects.create(
            estadoCaja = "M" , yymmCaja = yyyymm , salIniCaja = 0,
            salidaCaja = vMonto, entradaCaja = 0 , salFinCaja = vMonto
            )
        else:
            sCaja.salidaCaja = sCaja.salidaCaja + vMonto
            sCaja.salFinCaja = sCaja.salFinCaja - vMonto
            sCaja.save()

        sCaja = SaldoCaja.objects.get(estadoCaja = vEstado)
        sfinal = dos_dcimales(sCaja.salFinCaja) 

        # Crea movimiento en caja
        mCaja = MovimientoCaja.objects.create(
            yymm_Caja = yyyymm, fec_RegistroN = vRegistroN,  id_Asociado = aid, nombre = vnombre, cod_Prestamo = vCPrestamosI + 1 , 
            sec_Caja = 1 , accion_Caja = "CREO PRESTASMO", motivo_Caja = "NUEVO PRESTAMO", fec_AplicaN = vfecinin ,  fec_Aplica = vfecini,
            monto_Aplica = vMonto, s_Acumulado = sfinal , observacion_Caja = vobserva,
            tipo_Motivo = "SALIDA"
        )

        # PrestamosMovimiento
        vint_cal = ((vMonto * 15) / 100)
        vint_cal = dos_dcimales(vint_cal)
        salpen = vMonto + vint_cal
        salpen = dos_dcimales(salpen)
        mPM = PrestamosMovimiento.objects.create(
            yymm_MP = yyyymm, fec_RegistroN = vRegistroN, id_Asociado = aid, nombre = vnombre, cod_Prestamo = vCPrestamosI + 1, monto_Prestamo = vMonto,
            fec_IniN = vfecinin , fec_Ini = vfecini, fec_FinN = vfecfinn, fec_Fin = vfecfin, tasa_Int = 15.0 , dias_cal = 30, int_cal = vint_cal , 
            fec_Pag_RegN = 0 , fec_Pag_efeN = 0 , sal_pendiente = salpen,  estado_reg = "PENDIENTE", estado_prest = "ACTIVO", 
            Form_pago = "COBRO PENDIENTE", Observacion = vobserva, dias_cal_Pag = 0, int_cal_Pag = 0, int_01 = 0, int_02 = 0, abono_cap = 0, monto_pag = 0
        )
    
    return redirect('selSocio')

######################### Refinancia ###################################
# Refinanca Prestamo
def pRef(request, id):
    Pendientes = PrestamosMovimiento.objects.filter(estado_reg='PENDIENTE').filter(id_Asociado = id)
    socio = MaestroAsociado.objects.get(id_asociado=id)
    return render(request, 'prestamo/pRef.html', {'socio':socio,
                                                    'Pendientes':Pendientes})

def registrapRef(request):

    aid = request.POST ['txtid_asociado']
    vMontoO = request.POST['txtmontPrestamoO']
    vMonto = request.POST ['txtmontPrestamoF']
    vFecFinP = request.POST['txtFecFinP']
    vnombre = request.POST['txtnombre']
    vcodPrest = request.POST['txtcodPrest']
    vobserva = request.POST['txtObserva']
    vRegmov = request.POST['txtregmov']
    vfecini = request.POST['txtFecInic']
    vfecfin = request.POST['txtFecFinc']

    vValEnt = request.POST['txtValEnt']

    # Si el usuario presiono cancelar no entra
    if vValEnt == 'True':
        vRegistroN = datetime.now().strftime("%Y%m%d")
        vRegistroN = int(vRegistroN)
        vfecinin = int(eli_char_fec('-',vfecini))
        vfecfinn = int(eli_char_fec('-',vfecfin))
        vfecFinPN = int(eli_char_fec('-',vFecFinP))

        vMontoO = repl_char(',','.',vMontoO)
        vMontoO = float(vMontoO)
        vMontoO = dos_dcimales(vMontoO)

        vMonto = repl_char(',','.',vMonto)
        vMonto = float(vMonto)
        vMonto = dos_dcimales(vMonto)

        # Actualizo PrestamosSocio
        pSocio = PrestamoAsociado.objects.get(id_asociado = aid)
        pSocio.saldoPrestamo = ((pSocio.saldoPrestamo - vMontoO) + vMonto)
        pSocio.ultPrestamo = vFecFinP
        if pSocio.mayPrestamos < vMonto:
            pSocio.mayPrestamos = vMonto

        pSocio.save()

        # Valores de Sistema
        vEstado = "M"
        vcodSis = "FECPRO"
        sTS = TablaSistema.objects.get(cod_Sistema = vcodSis)
        yyyymm = str(sTS.Valor_Sistema)

        # Saldo de Caja
        sCaja = SaldoCaja.objects.get(estadoCaja = vEstado)

        vsaldo1 = sCaja.salFinCaja + vMontoO
        vsaldo1 = dos_dcimales(vsaldo1)
        vsaldo2 = (sCaja.salFinCaja + vMontoO) - vMonto
        vsaldo2 = dos_dcimales(vsaldo2)

        sCaja.entradaCaja = sCaja.entradaCaja + vMontoO
        sCaja.salidaCaja = sCaja.salidaCaja + vMonto
        sCaja.salFinCaja = ((sCaja.salIniCaja + sCaja.entradaCaja) - sCaja.salidaCaja)
        sCaja.save()

        sCaja = SaldoCaja.objects.get(estadoCaja = vEstado)
        sfinal = sCaja.salFinCaja 

        # Crea movimiento en caja - Cancela Int

        mCaja = MovimientoCaja.objects.create(
            yymm_Caja = yyyymm, fec_RegistroN = vRegistroN,  id_Asociado = aid, nombre = vnombre, cod_Prestamo = vcodPrest , 
            sec_Caja = 1 , accion_Caja = "REFINANCIA", motivo_Caja = "SALDO ORIGEN", fec_AplicaN = vfecinin ,  fec_Aplica = vfecini,
            monto_Aplica = vMontoO, s_Acumulado = vsaldo1 , observacion_Caja = vobserva,
            tipo_Motivo = "ENTRADA"
        )

        # Crea movimiento en caja - Cancela Capital
        mCaja = MovimientoCaja.objects.create(
            yymm_Caja = yyyymm, fec_RegistroN = vRegistroN, id_Asociado = aid, nombre = vnombre, cod_Prestamo = vcodPrest , 
            sec_Caja = 2 , accion_Caja = "REFINANCIA", motivo_Caja = "NUEVO SALDO", fec_AplicaN = vfecinin , fec_Aplica = vFecFinP,
            monto_Aplica = vMonto, s_Acumulado = vsaldo2 , observacion_Caja = vobserva,
            tipo_Motivo = "SALIDA"
        )

        # PrestamosMovimiento
    
        # Actualizo registro----campos de pago
        sPM = PrestamosMovimiento.objects.get(id_MP = vRegmov )
        sPM.fec_Pag_RegN = vRegistroN
        sPM.fec_Pag_efeN = vfecFinPN
        sPM.fec_Pag_efe = vFecFinP
        sPM.monto_pag = vMontoO
        sPM.sal_pendiente =  0
        sPM.estado_reg = "COBRADO"
        sPM.estado_prest = "CERRADO"
        sPM.Form_pago = "REFINANCIA"
        sPM.Observacion = vobserva
        sPM.save()

        vint_cal = ((vMonto * 15) / 100)
        vint_cal = dos_dcimales(vint_cal)
        salpen =  (vMonto + vint_cal)
        salpen = dos_dcimales(salpen)
        mPM = PrestamosMovimiento.objects.create(
            yymm_MP = yyyymm, fec_RegistroN = vRegistroN, id_Asociado = aid, nombre = vnombre, cod_Prestamo = vcodPrest, monto_Prestamo = vMonto,
            fec_IniN = vfecinin , fec_Ini = vfecini, fec_FinN = vfecfinn, fec_Fin = vfecfin, tasa_Int = 15.0 , dias_cal = 30, int_cal = vint_cal , 
            fec_Pag_RegN = 0 , fec_Pag_efeN = 0 , sal_pendiente = salpen , estado_reg = "PENDIENTE", estado_prest = "ACTIVO", 
            Form_pago = "REFINANCIA", Observacion = vobserva, dias_cal_Pag = 0, int_cal_Pag = 0, int_01 = 0, int_02 = 0, abono_cap = 0, monto_pag = 0
        )

    return redirect('selSocio')
