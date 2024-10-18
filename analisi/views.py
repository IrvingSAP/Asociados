from django.shortcuts import render, redirect
from core.models import PrestamosMovimiento

# Create your views here.

# ###################### FUNCIONES   #####################################


######################### Presenta Socios ###################################
# Presento Socios
def analisis01(request):
    Movimientos = PrestamosMovimiento.objects.all()
    return render(request, 'analisi/analisis01.html', {'Movimientos':Movimientos})