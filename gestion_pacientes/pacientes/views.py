from django.shortcuts import render, redirect
from .logic.lista_doble import ListaTurnos

# Lista global que maneja los turnos
turnos = ListaTurnos()

def lista_turnos(request):
    pacientes = turnos.recorrer()
    return render(request, "pacientes/lista.html", {"pacientes": pacientes})

def registrar_paciente(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        prioridad = request.POST.get("prioridad", "normal")
        turnos.asignar_turno(nombre, prioridad)
        return redirect("lista_turnos")
    return render(request, "pacientes/registro.html")

def atender_paciente(request):
    paciente = turnos.atender_paciente()
    return render(request, "pacientes/atendido.html", {"paciente": paciente})
