from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [

    # Selecciona Socio
    path('selSocioCaja/', views.selSocioCaja, name='selSocioCaja'),
    path('selCajaR/<id>', views.selCajaR, name='selCajaR'),
    path('selCajaM/<id>', views.selCajaM, name='selCajaM'),
    path('selCajaE/<id>', views.selCajaE, name='selCajaE'),
    
]