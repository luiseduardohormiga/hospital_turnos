from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.lista_turnos, name="lista_turnos"),
    path('registrar/', views.registrar_paciente, name="registrar_paciente"),
    path('pasar_turno/', views.pasar_turno, name="pasar_turno"),
    path("atender/<int:paciente_id>/", views.atender_paciente, name="atender_paciente"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("espera/", views.lista_espera, name="lista_espera"),
    path("asignar/<int:paciente_id>/", views.asignar_prioridad, name="asignar_prioridad"),
    path("devolver_turno/", views.devolver_turno, name="devolver_turno"),
]
