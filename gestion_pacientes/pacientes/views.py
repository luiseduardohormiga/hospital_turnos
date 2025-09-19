from django.shortcuts import render, redirect
from .logic.lista_doble import ListaDobleTurnos
from .forms import PacienteForm
from .models import Turno
from django.contrib import messages

# Instancia global de la lista doble
turnos = ListaDobleTurnos()

def lista_turnos(request):
    # Obtener turnos desde la lista doble, no desde sorted()
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
            # Guardamos el paciente
            paciente = form.save()

            # Generar número de turno
            ultimo_turno = Turno.objects.order_by("-numero_turno").first()
            nuevo_numero = ultimo_turno.numero_turno + 1 if ultimo_turno else 1

            # Crear el turno
            turno = Turno.objects.create(
                paciente=paciente,
                numero_turno=nuevo_numero,
                estado="pendiente"
            )

            # Agregar el turno a la lista doble
            turnos.agregar(turno)
            
            messages.success(request, f"Paciente {paciente.nombre} registrado con turno {turno.numero_turno}")

            # Te quedas en la misma página, pero con form limpio
            return redirect("registrar_paciente")
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
