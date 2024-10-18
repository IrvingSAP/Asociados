from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [

    # Selecciona registros de moviento
    path('analisis01/', views.analisis01, name='analisis01'),
]