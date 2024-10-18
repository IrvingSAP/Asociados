from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [

    # Selecciona Socio
    path('selSocioPago/', views.selSocioPago, name='selSocioPago'),

    # Paga Int
    path('pagaInt/<int:id>', views.pagaInt, name='pagaInt'),
    path('registraPagoInt/', views.registraPagoInt, name='registraPagoInt'),

    # AMortiza
    path('pagaAmortiza/<int:id>', views.pagaAmortiza, name = 'pagaAmortiza'),
    path('registraPagoAmortiza/', views.registraPagoAmortiza, name='registraPagoAmortiza'),

    # Cancela Prestamo
    path('pagaCancela/<int:id>', views.pagaCancela, name ='pagaCancela'),
    path('registraCancela/',views.registraCancela, name='registraCancela'),
]