from django.shortcuts import render, redirect
from .logic.lista_doble import ListaTurnos
from .forms import PacienteForm
from .models import Paciente, Turno

turnos = ListaTurnos()

def lista_turnos(request):
    turnos = Turno.objects.select_related("paciente").all()
    # Ordenar primero por prioridad (menor valor primero), luego por número de turno
    turnos = sorted(turnos, key=lambda t: (t.paciente.prioridad_valor(), t.numero_turno))
    en_atencion = Turno.objects.filter(estado="en_atencion").first()
    return render(request, "pacientes/lista.html", {
        "turnos": turnos,
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
            Turno.objects.create(
                paciente=paciente,
                numero_turno=nuevo_numero,
                estado="pendiente"
            )

            return redirect("lista_turnos")
    else:
        form = PacienteForm()

    return render(request, "pacientes/registro.html", {"form": form})

def pasar_turno(request):
    # Buscar el que está en atención
    en_atencion = Turno.objects.filter(estado="en_atencion").first()
    if en_atencion:
        en_atencion.estado = "atendido"
        en_atencion.save()

    # Seleccionar el siguiente pendiente (ordenado por prioridad y número)
    pendientes = Turno.objects.filter(estado="pendiente").all()
    pendientes = sorted(pendientes, key=lambda t: (t.paciente.prioridad_valor(), t.numero_turno))

    if pendientes:
        siguiente = pendientes[0]
        siguiente.estado = "en_atencion"
        siguiente.save()

    return redirect("lista_turnos")

def atender_paciente(request, paciente_id):
    turnos.pasar_a_atendido(paciente_id)  # necesitas que tu lógica acepte ID
    return redirect("lista_turnos")
