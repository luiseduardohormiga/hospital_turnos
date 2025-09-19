# pacientes/logic/lista_doble.py
class NodoTurno:
    def __init__(self, turno):
        self.turno = turno
        self.siguiente = None
        self.anterior = None

class ListaDobleTurnos:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def agregar(self, turno):
        nuevo = NodoTurno(turno)

        # Si está vacía
        if self.cabeza is None:
            self.cabeza = self.cola = nuevo
            return

        # Insertar ordenado por prioridad
        actual = self.cabeza
        while actual and self._valor_prioridad(actual.turno.paciente.prioridad) <= self._valor_prioridad(turno.paciente.prioridad):
            actual = actual.siguiente

        if actual is None:  # va al final
            self.cola.siguiente = nuevo
            nuevo.anterior = self.cola
            self.cola = nuevo
        elif actual == self.cabeza:  # va al inicio
            nuevo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo
            self.cabeza = nuevo
        else:  # en medio
            anterior = actual.anterior
            anterior.siguiente = nuevo
            nuevo.anterior = anterior
            nuevo.siguiente = actual
            actual.anterior = nuevo

    def atender(self):
        if self.cabeza is None:
            return None

        turno = self.cabeza.turno
        self.cabeza = self.cabeza.siguiente
        if self.cabeza:
            self.cabeza.anterior = None
        else:
            self.cola = None
        return turno

    def recorrer(self):
        actual = self.cabeza
        lista = []
        while actual:
            lista.append(actual.turno)
            actual = actual.siguiente
        return lista

    def _valor_prioridad(self, prioridad):
        # Define los valores de prioridad (ajústalos a tu modelo)
        prioridades = {"urgencia": 1, "adulto_mayor": 2, "embarazo": 2, "normal": 3}
        return prioridades.get(prioridad, 3)
