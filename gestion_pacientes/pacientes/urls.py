from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_turnos, name="lista_turnos"),
    path('registrar/', views.registrar_paciente, name="registrar_paciente"),
    path('atender/', views.atender_paciente, name="atender_paciente"),
]
