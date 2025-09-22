# implementacion de lista doblemente enlazada para gestionar turnos de pacientes
# cada nodo tiene referencia al siguiente y al anterior
# la lista se mantiene ordenada por prioridad del paciente

class NodoTurno:
    def __init__(self, turno):
        self.turno = turno
        self.siguiente = None # nodo que guarda info, fechas siguiente y el anterior
        self.anterior = None

class ListaDobleTurnos:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.actual = None  # referencia al turno que se está atendiendo

    def agregar(self, turno):
        nuevo = NodoTurno(turno)

        if self.cabeza is None:
            self.cabeza = self.cola = nuevo
            return

        actual = self.cabeza
        while actual and self._valor_prioridad(actual.turno.paciente.prioridad) <= self._valor_prioridad(turno.paciente.prioridad):
            actual = actual.siguiente

        if actual is None:  
            self.cola.siguiente = nuevo
            nuevo.anterior = self.cola
            self.cola = nuevo
        elif actual == self.cabeza:  
            nuevo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo
            self.cabeza = nuevo
        else:  
            anterior = actual.anterior
            anterior.siguiente = nuevo
            nuevo.anterior = anterior
            nuevo.siguiente = actual
            actual.anterior = nuevo

    def atender(self):
        """Avanzar al siguiente turno"""
        if self.actual is None:
            self.actual = self.cabeza
        else:
            self.actual = self.actual.siguiente
        return self.actual.turno if self.actual else None

    def devolver(self):
        """Regresar al turno anterior"""
        if self.actual and self.actual.anterior:
            self.actual = self.actual.anterior
            return self.actual.turno
        return None  # No hay turno anterior

    def recorrer(self):
        actual = self.cabeza
        lista = []
        while actual:
            lista.append(actual.turno)
            actual = actual.siguiente
        return lista

    def _valor_prioridad(self, prioridad): 
        prioridades = {
            "nivel_1": 1,  # Muy alta
            "nivel_2": 2,  # Alta
            "nivel_3": 3,  # Media
            "nivel_4": 4,  # Baja
            "nivel_5": 5,  # Muy baja
        }
        return prioridades.get(prioridad, 99)

