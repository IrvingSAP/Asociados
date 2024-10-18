from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [

    path('cierreCaja/', views.cierreCaja, name='cierreCaja'),
    path('updCierreCaja/', views.updCierreCaja, name='updCierreCaja'),
]
