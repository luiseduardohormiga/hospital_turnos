class NodoTurno:
    def __init__(self, id_paciente, nombre, prioridad):
        self.id = id_paciente
        self.nombre = nombre
        self.prioridad = prioridad  # "normal", "urgencia", "adulto_mayor", "embarazo"
        self.prev = None
        self.next = None


class ListaTurnos:
    def __init__(self):
        self.head = None
        self.tail = None
        self.contador_turnos = 1  # para asignar turnos automáticos

    def asignar_turno(self, nombre, prioridad="normal"):
        id_paciente = self.contador_turnos
        self.contador_turnos += 1

        nuevo = NodoTurno(id_paciente, nombre, prioridad)

        if not self.head:
            self.head = self.tail = nuevo
        else:
            if prioridad == "normal":
                self.tail.next = nuevo
                nuevo.prev = self.tail
                self.tail = nuevo
            else:
                actual = self.head
                while actual and actual.prioridad != "normal":
                    actual = actual.next
                if not actual:
                    self.tail.next = nuevo
                    nuevo.prev = self.tail
                    self.tail = nuevo
                elif actual == self.head:
                    nuevo.next = self.head
                    self.head.prev = nuevo
                    self.head = nuevo
                else:
                    anterior = actual.prev
                    anterior.next = nuevo
                    nuevo.prev = anterior
                    nuevo.next = actual
                    actual.prev = nuevo
        return nuevo

    def atender_paciente(self):
        if not self.head:
            return None
        paciente = self.head
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        return paciente

    def buscar_paciente(self, id_paciente=None, nombre=None):
        actual = self.head
        while actual:
            if id_paciente and actual.id == id_paciente:
                return actual
            if nombre and actual.nombre.lower() == nombre.lower():
                return actual
            actual = actual.next
        return None

    def recorrer(self):
        actual = self.head
        pacientes = []
        while actual:
            pacientes.append((actual.id, actual.nombre, actual.prioridad))
            actual = actual.next
        return pacientes

    def recorrer_inverso(self):
        actual = self.tail
        pacientes = []
        while actual:
            pacientes.append((actual.id, actual.nombre, actual.prioridad))
            actual = actual.prev
        return pacientes
