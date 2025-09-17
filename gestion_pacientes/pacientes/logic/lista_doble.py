class NodoTurno:
    def __init__(self, id_paciente, nombre, prioridad):
        self.id = id_paciente
        self.nombre = nombre
        self.prioridad = prioridad  # "normal", "urgencia", "adulto_mayor", "embarazo"
        self.estado = "espera"      # "espera", "atendiendo", "atendido"
        self.prev = None
        self.next = None


class ListaTurnos:
    def __init__(self):
        self.head = None
        self.tail = None
        self.contador_turnos = 1
        self.turno_actual = None  # referencia al paciente atendiendo

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
        # si no hay nadie atendiendo, este pasa directo
        if not self.turno_actual:
            self.turno_actual = self.head
            self.turno_actual.estado = "atendiendo"
        return nuevo

    def pasar_a_atendido(self):
        """El admin marca el turno en atención como atendido y pasa al siguiente."""
        if not self.turno_actual:
            return None
        # marcar el turno actual como atendido
        self.turno_actual.estado = "atendido"
        # mover al siguiente turno en espera
        siguiente = self.turno_actual.next
        while siguiente and siguiente.estado != "espera":
            siguiente = siguiente.next
        if siguiente:
            siguiente.estado = "atendiendo"
            self.turno_actual = siguiente
        else:
            self.turno_actual = None
        return True

    def recorrer(self):
        """Devuelve todos los turnos (espera, atendiendo, atendido)."""
        actual = self.head
        pacientes = []
        while actual:
            pacientes.append((actual.id, actual.nombre, actual.prioridad, actual.estado))
            actual = actual.next
        return pacientes

    def turno_en_atencion(self):
        """Devuelve el paciente que está en turno."""
        return self.turno_actual
