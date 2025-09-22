# implementacion de lista doblemente enlazada para gestionar turnos de pacientes
# cada nodo tiene referencia al siguiente y al anterior
# la lista se mantiene ordenada por prioridad del paciente

class NodoTurno:
    def __init__(self, turno):
        self.turno = turno
        self.siguiente = None #nodo que guarda el turno, siguiente y el anterior
        self.anterior = None

class ListaDobleTurnos:
    def __init__(self):
        self.cabeza = None #cabeza y cola de la lista
        self.cola = None

#cuendo se registra un paciente se agrega a la lista doble
    def agregar(self, turno):
        nuevo = NodoTurno(turno)

        # verificar Si está vacía
        if self.cabeza is None:
            self.cabeza = self.cola = nuevo
            return

        # Insertar ordenado por prioridad
        actual = self.cabeza #se compara las prioridades
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

    def atender(self): # se toma el primer turno de la lista
        if self.cabeza is None:
            return None

        turno = self.cabeza.turno
        self.cabeza = self.cabeza.siguiente  #avanza al siguiente
        if self.cabeza:
            self.cabeza.anterior = None
        else:
            self.cola = None
        return turno

    def recorrer(self):
        actual = self.cabeza
        lista = []
        while actual:
            lista.append(actual.turno) # lista python
            actual = actual.siguiente
        return lista

    def _valor_prioridad(self, prioridad): 
        prioridades = {
            "nivel_1": 1,  # Muy alta
            "nivel_2": 2,  # Alta
            "nivel_3": 3,  # Media  orden numerico
            "nivel_4": 3,  # Baja
            "nivel_5": 3,  # Muy baja
        }
        return prioridades.get(prioridad, 99)
