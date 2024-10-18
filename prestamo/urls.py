from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [

    path('selSocio/', views.selSocio, name='selSocio'),
    path('creaPrestamo/<int:id>', views.creaPrestamo, name='creaPrestamo'),
    path('registraPrestamo/', views.registraPrestamo, name='registraPrestamo'),
    path('pRef/<int:id>', views.pRef, name='pRef'),
    path('registrapRef/', views.registrapRef, name= 'registrapRef'),
]
