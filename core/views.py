from django.shortcuts import render, redirect
from .models import MaestroAsociado, PrestamoAsociado
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime

################## FUNCIONES #########################


# Create your views here.

# Valida Login he inicio de Web
@login_required
def home(request):
    return render(request, 'core/home.html')

# Salir de Conexion BD
def exit(request):
    logout(request)
    return redirect('/')

# Muestra los Asociados
def asociado(request):
    MAsociados = MaestroAsociado.objects.all()
    return render(request, 'core/asociado.html', {'MAsociados':MAsociados})

# Registra Asociado y PrestamoAsociado
def registraSocio(request):

    # Registra Socio

    anombre = request.POST ['txtNombre']
    atelefono = request.POST ['txtTelefono']
    acorreo = request.POST ['txtCorreo']
    aestado = request.POST ['txtEstado']

    asociado = MaestroAsociado.objects.create(
        nombre=anombre, telefono=atelefono, correo=acorreo, estado=aestado)
    
    # Registra PrestamoSocio
    fecha_actual = datetime.now()
    socio = MaestroAsociado.objects.last()
    Iid_asociado = socio.id_asociado

    pasociado = PrestamoAsociado.objects.create(
        id_asociado = Iid_asociado, cantPrestamos=0 , actPrestamos=0, inacPrestamos=0,
          mayPrestamos = 0, ultPrestamo= fecha_actual, saldoPrestamo=0, estado='A' )

    MAsociados = MaestroAsociado.objects.all()
    return render(request, 'core/asociado.html', {'MAsociados':MAsociados})

# Edita el Socio
def editaSocio(request, id):
    socio = MaestroAsociado.objects.get(id_asociado=id)
    print(socio)
    return render(request, 'core/editaSocio.html', {'socio':socio})

# Actualiza el Socio
def updateSocio(request):
    aid = request.POST ['txtID']
    anombre = request.POST ['txtNombre']
    atelefono = request.POST ['txtTelefono']
    acorreo = request.POST ['txtCorreo']
    aestado = request.POST ['txtEstado']
    socio = MaestroAsociado.objects.get(id_asociado = aid)
    socio.nombre=anombre
    socio.telefono=atelefono
    socio.correo=acorreo
    socio.estado=aestado
    socio.save()
    MAsociados = MaestroAsociado.objects.all()
    return render(request, 'core/asociado.html', {'MAsociados':MAsociados})