from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as aut_views
from .import views

urlpatterns = [
    path('', views.home, name = 'home'),
   # path('login/', aut_views.LoginView, nave='Login'),
    path('asociado/', views.asociado, name='asociado'),
    path('registraSocio/', views.registraSocio, name='registraSocio'),
    path('editaSocio/<int:id>', views.editaSocio, name='editaSocio'),
    path('updateSocio/', views.updateSocio, name='updateSocio'),
    path('exit', views.exit, name='exit'),
]
