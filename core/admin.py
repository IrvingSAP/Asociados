from django.contrib import admin
from .models import MaestroAsociado, PrestamoAsociado, SaldoCaja, MovimientoCaja, PrestamosMovimiento, TablaSistema

# Register your models here.
admin.site.register(MaestroAsociado)
admin.site.register(PrestamoAsociado)
admin.site.register(SaldoCaja)
admin.site.register(MovimientoCaja)
admin.site.register(PrestamosMovimiento)
admin.site.register(TablaSistema)
