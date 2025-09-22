from django.shortcuts import render, redirect, get_object_or_404
from .logic.lista_doble import ListaDobleTurnos
from .forms import PacienteForm
from .models import Turno, Paciente
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

# @login_required

class CustomLoginView(LoginView):
    template_name = "pacientes/login.html"
    
# Instancia global de la lista doble
turnos = ListaDobleTurnos()

def lista_turnos(request):
    # obteniendo turnos desde la lista doble
    lista = turnos.recorrer()
    en_atencion = Turno.objects.filter(estado="en_atencion").first()
    return render(request, "pacientes/lista.html", {
        "turnos": lista,
        "en_atencion": en_atencion,
    })

def registrar_paciente(request):
    if request.method == "POST":
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.prioridad = "pendiente"  # por defecto
            paciente.save()

            messages.success(request, f"Paciente {paciente.nombre} registrado. En un momento se te llamará al triage.")
            return redirect("registrar_paciente")  # se queda en el registro
    else:
        form = PacienteForm()

    return render(request, "pacientes/registro.html", {"form": form})

def pasar_turno(request):
    # Buscar el que está en atención
    en_atencion = Turno.objects.filter(estado="en_atencion").first()
    if en_atencion:
        en_atencion.estado = "atendido"
        en_atencion.save()

    # Sacar el siguiente de la lista doble
    siguiente = turnos.atender()
    if siguiente:
        siguiente.estado = "en_atencion"
        siguiente.save()

    return redirect("lista_turnos")

def atender_paciente(request, paciente_id):
    return redirect("lista_turnos")

def lista_espera(request):
    pacientes = Paciente.objects.filter(prioridad="pendiente").order_by("fecha_registro")
    return render(request, "pacientes/lista_espera.html", {"pacientes": pacientes})

@login_required
def asignar_prioridad(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == "POST":
        nueva_prioridad = request.POST.get("prioridad")
        if nueva_prioridad:
            paciente.prioridad = nueva_prioridad
            paciente.save()

            # Generar número de turno
            ultimo_turno = Turno.objects.order_by("-numero_turno").first()
            nuevo_numero = ultimo_turno.numero_turno + 1 if ultimo_turno else 1

            # Crear turno
            turno = Turno.objects.create(
                paciente=paciente,
                numero_turno=nuevo_numero,
                estado="pendiente"
            )

            # Insertar en lista doble
            turnos.agregar(turno)

            messages.success(request, f"Turno {turno.numero_turno} generado para {paciente.nombre}")
            return redirect("lista_espera")

    return redirect("lista_espera")
