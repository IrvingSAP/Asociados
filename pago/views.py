from django.shortcuts import render, redirect
from core.models import MaestroAsociado, PrestamoAsociado, SaldoCaja, MovimientoCaja, PrestamosMovimiento, TablaSistema
from datetime import datetime
from datetime import date

# Create your views here.

# ###################### FUNCIONES   #####################################

def eli_char_fec(c1,valor):
    valor = "".join(valor.split(c1))
    return valor 

# retorna la fecha en formato "%d/%m/%Y"
def retorna_fecha(valor1):
    lista = valor1.split('-')
    fa = lista[0]
    fm = lista[1]
    fd = lista[2]
    nf = lista[2] + '/' + lista[1] + '/' + lista[0]
    fecha_dti = datetime.strptime(nf, "%d/%m/%Y")
    return fecha_dti

# retorna la diferencia en dias entre dos fecha
def retorna_dias(valor1, valor2):
    diferencia = valor2 - valor1
    ddd = diferencia.days
    return ddd

# Reemplaza caracteres
def repl_char(char1,char2,origen):
    origen = origen.replace(char1,char2)
    return origen

# Redondedo 2 decimales
def dos_dcimales(valor1):
    return round(valor1, 2)

######################### Presenta Socios ###################################
# Presento Socios
def selSocioPago(request):
    MAsociados = MaestroAsociado.objects.all()
    return render(request, 'pago/selSocioPago.html', {'MAsociados':MAsociados})

######################### Paga Interes ###################################
# Paga Int
def pagaInt(request, id):
    PPendientes = PrestamosMovimiento.objects.filter(estado_reg='PENDIENTE').filter(id_Asociado = id)
    socio = MaestroAsociado.objects.get(id_asociado=id)
    return render(request, 'pago/pagaInt.html', {'socio':socio,
                                                'PPendientes':PPendientes})

# Prestamo , Adiciono y Actualizo Datos
def registraPagoInt(request):
    aid = request.POST ['txtid_asociado']
    vnombre = request.POST['txtnombre']
    vobserva = request.POST['txtObserva']
    vintcal = request.POST['txtIntcal']
    vcodPrest = request.POST['txtcodPrest']
    vFecIniP = request.POST['txtFecIniP']
    vFecFinP = request.POST['txtFecFinP']
    vMonto = request.POST['txtmontPrestamoF']
    vfecini = request.POST['txtFecInic']
    vfecfin = request.POST['txtFecFinc']
    vRegmov = request.POST['txtregmov']

    vValEnt = request.POST['txtValEnt']

    # Si el usuario presiono cancelar no entra
    if vValEnt == 'True':

        vRegistroN = datetime.now().strftime("%Y%m%d")
        vRegistroN = int(vRegistroN)
        vfecinin = int(eli_char_fec('-',vfecini))
        vfecfinn = int(eli_char_fec('-',vfecfin))
        vfecFinPN = int(eli_char_fec('-',vFecFinP))

        vintcal = repl_char(',','.',vintcal)
        vintcal = float(vintcal)
        vintcal = dos_dcimales(vintcal)

        vMonto = repl_char(',','.',vMonto)
        vMonto = float(vMonto)
        vMonto = dos_dcimales(vMonto)

        vintPers = (vintcal/2)
        vintPers = dos_dcimales(vintPers)
        fecha_actual = str(date.today())

        # Valores de Sistema
        vEstado = "M"
        vcodSis = "FECPRO"
        sTS = TablaSistema.objects.get(cod_Sistema = vcodSis)
        yyyymm = str(sTS.Valor_Sistema)

        # Saldo de Caja
        sCaja = SaldoCaja.objects.get(estadoCaja = vEstado)

        sCaja.entradaCaja = sCaja.entradaCaja + vintPers
        sCaja.salFinCaja = sCaja.salFinCaja + vintPers
        sCaja.save()

        sCaja = SaldoCaja.objects.get(estadoCaja = vEstado)
        sfinal = sCaja.salFinCaja 
        sfinal = dos_dcimales(sfinal)

        # Crea movimiento en caja
        mCaja = MovimientoCaja.objects.create(
            yymm_Caja = yyyymm, fec_RegistroN = vRegistroN, id_Asociado = aid, nombre = vnombre, cod_Prestamo = vcodPrest , 
            sec_Caja = 1 , accion_Caja = "PAGO INT", motivo_Caja = "PAGO INT", fec_AplicaN = vfecFinPN , fec_Aplica = vFecFinP,
            monto_Aplica = vintPers, s_Acumulado = sfinal , observacion_Caja = vobserva,
            tipo_Motivo = "ENTRADA"
        )

        # PrestamosMovimiento
        # Actualizo - Pago
        # calculo dias diferencia

        fip = retorna_fecha(vFecIniP)
        ffp = retorna_fecha(vFecFinP)
        dfd = retorna_dias(fip,ffp)

        sPM = PrestamosMovimiento.objects.get(id_MP = vRegmov )
        sPM.fec_Pag_RegN = vRegistroN
        sPM.fec_Pag_efeN = vfecFinPN
        sPM.fec_Pag_reg = fecha_actual
        sPM.fec_Pag_efe = vFecFinP
        sPM.dias_cal_Pag = dfd
        sPM.int_cal_Pag = vintcal
        sPM.int_01 = vintPers
        sPM.int_02 = vintPers
        sPM.sal_pendiente =  vMonto
        sPM.estado_reg = "COBRADO"
        sPM.estado_prest = "CERRADO"
        sPM.Form_pago = "PAGO INT"
        sPM.save()

        # Creo registro en Movimiento de Prestamo
        vint_cal = ((vMonto * 15) / 100)
        vint_cal = dos_dcimales(vint_cal)
        salpen =  vMonto + vint_cal
        salpen = dos_dcimales(salpen)
        mPM = PrestamosMovimiento.objects.create(
            yymm_MP = yyyymm, fec_RegistroN = vRegistroN, id_Asociado = aid, nombre = vnombre, cod_Prestamo = vcodPrest, monto_Prestamo = vMonto,
            fec_IniN = vfecinin , fec_Ini = vfecini, fec_Fin = vfecfin, fec_FinN = vfecfinn, tasa_Int = 15.0 , dias_cal = 30, int_cal = vint_cal , 
            fec_Pag_RegN = 0 , fec_Pag_efeN = 0 ,  sal_pendiente = salpen, estado_reg = "PENDIENTE", estado_prest = "ACTIVO",
            Form_pago = "COBRO PENDIENTE", Observacion = vobserva, dias_cal_Pag = 0, int_cal_Pag = 0, int_01 = 0, int_02 = 0, abono_cap = 0, monto_pag = 0
        )
    
    MAsociados = MaestroAsociado.objects.all()
    return render(request, 'pago/selSocioPago.html', {'MAsociados':MAsociados})

######################### Amortiza(INT/Capital) ###################################
# Paga - Amortiza
def pagaAmortiza(request, id):

    PPendientes = PrestamosMovimiento.objects.filter(estado_reg='PENDIENTE').filter(id_Asociado = id)
    socio = MaestroAsociado.objects.get(id_asociado=id)
    
    return render(request, 'pago/pagaAmortiza.html', {'socio':socio,
                                                'PPendientes':PPendientes})

# Prestamo , Adiciono y Actualizo Datos
def registraPagoAmortiza(request):
    aid = request.POST ['txtid_asociado']
    vnombre = request.POST['txtnombre']
    vcodPrest = request.POST['txtcodPrest']
    vRegmov = request.POST['txtregmov']
    vFecIniP = request.POST['txtFecIniP']
    vFecFinP = request.POST['txtFecFinP']
    vintcal = request.POST['txtIntcal']
    vPago = request.POST['txtPago']
    vAbono = request.POST['txtAbono']
    vsPend = request.POST['txtSPend']
    vobserva = request.POST['txtObserva']
    vMonto = request.POST['txtmontPrestamoF']
    vfecini = request.POST['txtFecInic']
    vfecfin = request.POST['txtFecFinc']
    vDcal = request.POST['txtDcal']

    vValEnt = request.POST['txtValEnt']

    # Si el usuario presiono cancelar no entra
    if vValEnt == 'True':
        vRegistroN = datetime.now().strftime("%Y%m%d")
        vRegistroN = int(vRegistroN)
        vfecinin = int(eli_char_fec('-',vfecini))
        vfecfinn = int(eli_char_fec('-',vfecfin))
        vfecFinPN = int(eli_char_fec('-',vFecFinP))

        vDcal = int(vDcal)
        vintcal = repl_char(',','.',vintcal)
        vintcal = float(vintcal)
        vintcal = dos_dcimales(vintcal)

        vMonto = repl_char(',','.',vMonto)
        vMonto = float(vMonto)
        vMonto = dos_dcimales(vMonto)

        vAbono = repl_char(',','.',vAbono)
        vAbono = float(vAbono)
        vAbono = dos_dcimales(vAbono)

        vPago = repl_char(',','.',vPago)
        vPago = float(vPago)
        vPago = dos_dcimales(vPago)

        vintPers = (vintcal/2)
        vintPers = dos_dcimales(vintPers)

        fecha_actual = str(date.today())

        # Valores de Sistema
        vEstado = "M"
        vcodSis = "FECPRO"
        sTS = TablaSistema.objects.get(cod_Sistema = vcodSis)
        yyyymm = str(sTS.Valor_Sistema)

        # Actualizo PrestamosSocio
        pSocio = PrestamoAsociado.objects.get(id_asociado = aid)
        pSocio.saldoPrestamo = pSocio.saldoPrestamo - (vAbono)

        pSocio.save()

        # Saldo de Caja
        sCaja = SaldoCaja.objects.get(estadoCaja = vEstado)

        sCajaInt = sCaja.salFinCaja + vintPers
        sCajaInt = dos_dcimales(sCajaInt)

        sCajaabono = sCaja.salFinCaja + vAbono + vintPers 
        sCajaabono = dos_dcimales(sCajaabono)


        sCaja.entradaCaja = sCaja.entradaCaja + vintPers + vAbono
        sCaja.salFinCaja = sCajaabono
        sCaja.save()

        # Crea movimiento en caja - Pago Int
        mCaja = MovimientoCaja.objects.create(
            yymm_Caja = yyyymm, fec_RegistroN = vRegistroN, id_Asociado = aid, nombre = vnombre, cod_Prestamo = vcodPrest , 
            sec_Caja = 1 , accion_Caja = "AMORTIZA", motivo_Caja = "PAGO INT",  fec_AplicaN = vfecFinPN , fec_Aplica = vFecFinP,
            monto_Aplica = vintPers, s_Acumulado = sCajaInt , observacion_Caja = vobserva,
            tipo_Motivo = "ENTRADA"
        )

        # Crea movimiento en caja - Amortiza Capital
        mCaja = MovimientoCaja.objects.create(
            yymm_Caja = yyyymm, fec_RegistroN = vRegistroN, id_Asociado = aid, nombre = vnombre, cod_Prestamo = vcodPrest , 
            sec_Caja = 2 , accion_Caja = "AMORTIZA", motivo_Caja = "ABONA CAPITAL", fec_AplicaN = vfecFinPN , fec_Aplica = vFecFinP,
            monto_Aplica = vAbono, s_Acumulado = sCajaabono , observacion_Caja = vobserva,
            tipo_Motivo = "ENTRADA"
        )

        # PrestamosMovimiento
        # Creo Registro----
        vint_cal = ((vMonto * 15) / 100)
        vint_cal = dos_dcimales(vint_cal)
        salpend =  (vMonto + vint_cal)
        salpend = dos_dcimales(salpend)

        mPM = PrestamosMovimiento.objects.create(
            yymm_MP = yyyymm, fec_RegistroN = vRegistroN,  id_Asociado = aid, nombre = vnombre, cod_Prestamo = vcodPrest, monto_Prestamo = vMonto,
            fec_IniN = vfecinin , fec_Ini = vfecini, fec_Fin = vfecfin, fec_FinN = vfecfinn, tasa_Int = 15.0 , dias_cal = 30, int_cal = vint_cal ,
            fec_Pag_RegN = 0 , fec_Pag_efeN = 0 ,  sal_pendiente = salpend, estado_reg = "PENDIENTE", estado_prest = "ACTIVO",
            Form_pago = "COBRO PENDIENTE", Observacion = vobserva, dias_cal_Pag = 0, int_cal_Pag = 0, int_01 = 0, int_02 = 0, abono_cap = 0, monto_pag = 0
        )
    
        # Actualizo registro----campos de pago
        sPM = PrestamosMovimiento.objects.get(id_MP = vRegmov )
        sPM.fec_Pag_RegN = vRegistroN
        sPM.fec_Pag_efeN = vfecFinPN
        sPM.fec_Pag_reg = fecha_actual
        sPM.fec_Pag_efe = vFecFinP
        sPM.dias_cal_Pag = vDcal
        sPM.int_cal_Pag = vintcal
        sPM.int_01 = vintPers
        sPM.int_02 = vintPers
        sPM.abono_cap = vAbono
        sPM.monto_pag = vPago
        sPM.sal_pendiente =  vMonto
        sPM.estado_reg = "COBRADO"
        sPM.estado_prest = "CERRADO"
        sPM.Form_pago = "AMORTIZA"
        sPM.save()
    
    MAsociados = MaestroAsociado.objects.all()
    return render(request, 'pago/selSocioPago.html', {'MAsociados':MAsociados})

######################### Cancela Prestamo ###################################
def pagaCancela(request, id):

    PPendientes = PrestamosMovimiento.objects.filter(estado_reg='PENDIENTE').filter(id_Asociado = id)
    socio = MaestroAsociado.objects.get(id_asociado=id)
    
    return render(request, 'pago/pagaCancela.html', {'socio':socio,
                                                'PPendientes':PPendientes})

# Prestamo , Adiciono y Actualizo Datos
def registraCancela(request):
    aid = request.POST ['txtid_asociado']
    vnombre = request.POST['txtnombre']
    vcodPrest = request.POST['txtcodPrest']
    vRegmov = request.POST['txtregmov']
    vFecFinP = request.POST['txtFecFinP']
    vintcal = request.POST['txtIntcal']
    vsPend = request.POST['txtSPend']
    vobserva = request.POST['txtObserva']
    vMonto = request.POST['txtmontPrestamoO']
    vDcal = request.POST['txtDcal']

    vValEnt = request.POST['txtValEnt']

    # Si el usuario presiono cancelar no entra
    if vValEnt == 'True':
        vRegistroN = datetime.now().strftime("%Y%m%d")
        vRegistroN = int(vRegistroN)
        vfecFinPN = int(eli_char_fec('-',vFecFinP))

        vDcal = int(vDcal)

        vintcal = repl_char(',','.',vintcal)
        vintcal = float(vintcal)
        vintcal = dos_dcimales(vintcal)

        vsPend = repl_char(',','.',vsPend)
        vsPend = float(vsPend)
        vsPend = dos_dcimales(vsPend)

        vMonto = repl_char(',','.',vMonto)
        vMonto = float(vMonto)
        vMonto = dos_dcimales(vMonto)

        vintPers = (vintcal/2)
        vintPers = dos_dcimales(vintPers)

        fecha_actual = str(date.today())

        # Valores de Sistema
        vEstado = "M"
        vcodSis = "FECPRO"
        sTS = TablaSistema.objects.get(cod_Sistema = vcodSis)
        yyyymm = str(sTS.Valor_Sistema)

        # Actualizo PrestamosSocio
        pSocio = PrestamoAsociado.objects.get(id_asociado = aid)
        pSocio.cantPrestamos = pSocio.cantPrestamos - 1
        pSocio.actPrestamos = pSocio.actPrestamos - 1
        pSocio.saldoPrestamo = pSocio.saldoPrestamo - vMonto

        pSocio.save()

        # Saldo de Caja
        sCaja = SaldoCaja.objects.get(estadoCaja = vEstado)

        sCajaInt = sCaja.salFinCaja + vintPers
        sCajaInt = dos_dcimales(sCajaInt)

        sCajaabono = sCaja.salFinCaja + vMonto + vintPers 
        sCajaabono = dos_dcimales(sCajaabono)

        sCaja.entradaCaja = sCaja.entradaCaja + vintPers + vMonto
        sCaja.salFinCaja = sCajaabono
        sCaja.save()

        # Crea movimiento en caja - Cancela Int
        mCaja = MovimientoCaja.objects.create(
            yymm_Caja = yyyymm, fec_RegistroN = vRegistroN, id_Asociado = aid, nombre = vnombre, cod_Prestamo = vcodPrest , 
            sec_Caja = 1 , accion_Caja = "CANCELA", motivo_Caja = "CANCELA INT", fec_AplicaN = vfecFinPN , fec_Aplica = vFecFinP,
            monto_Aplica = vintPers, s_Acumulado = sCajaInt , observacion_Caja = vobserva,
            tipo_Motivo = "ENTRADA"
        )

        # Crea movimiento en caja - Cancela Capital
        mCaja = MovimientoCaja.objects.create(
            yymm_Caja = yyyymm, fec_RegistroN = vRegistroN, id_Asociado = aid, nombre = vnombre, cod_Prestamo = vcodPrest , 
            sec_Caja = 2 , accion_Caja = "CANCELA", motivo_Caja = "CANCELA CAPITAL", fec_AplicaN = vfecFinPN , fec_Aplica = vFecFinP,
            monto_Aplica = vMonto, s_Acumulado = sCajaabono , observacion_Caja = vobserva,
            tipo_Motivo = "ENTRADA"
        )

        # PrestamosMovimiento

        vint_cal = ((vMonto * 15) / 100)
        vint_cal = dos_dcimales(vint_cal)
    
        # Actualizo registro----campos de pago
        sPM = PrestamosMovimiento.objects.get(id_MP = vRegmov )
        sPM.fec_Pag_RegN = vRegistroN
        sPM.fec_Pag_efeN = vfecFinPN
        sPM.fec_Pag_reg = fecha_actual
        sPM.fec_Pag_efe = vFecFinP
        sPM.dias_cal_Pag = vDcal
        sPM.int_cal_Pag = vintcal
        sPM.int_01 = vintPers
        sPM.int_02 = vintPers
        sPM.monto_pag = vsPend
        sPM.sal_pendiente = 0
        sPM.estado_reg = "COBRADO"
        sPM.estado_prest = "CERRADO"
        sPM.Form_pago = "CANCELA"
        sPM.Observacion = vobserva
        sPM.save()

    MAsociados = MaestroAsociado.objects.all()
    return render(request, 'pago/selSocioPago.html', {'MAsociados':MAsociados})