from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_turnos, name="lista_turnos"),
    path('registrar/', views.registrar_paciente, name="registrar_paciente"),
    path('pasar_turno/', views.pasar_turno, name="pasar_turno"),
    path("atender/<int:paciente_id>/", views.atender_paciente, name="atender_paciente"),
]
