from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [

    # Selecciona Socio
    path('conSocio/', views.conSocio, name='conSocio'),
    path('conSocPend/<int:id>', views.conSocPend, name='conSocPend'),
    path('conSocPendDet/<int:id>/<int:codpre>' , views.conSocPendDet, name ='conSocPendDet' ),

]