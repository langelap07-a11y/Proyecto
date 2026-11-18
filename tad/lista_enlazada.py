"""TAD: Lista enlazada simple.

Guarda las paradas de cada ruta (en orden) y las listas de resultados.
Operaciones: agregar_al_final, agregar_al_inicio, obtener, eliminar, esta_vacia, len().
"""


class ListaEnlazada:

    class _Nodo:
        def __init__(self, dato):
            self.dato = dato
            self.siguiente = None

    def __init__(self):
        self._cabeza = None
        self._cola = None
        self._tamano = 0

    def agregar_al_final(self, dato):
        nuevo = self._Nodo(dato)
        if self._cabeza is None:
            self._cabeza = nuevo
            self._cola = nuevo
        else:
            self._cola.siguiente = nuevo
            self._cola = nuevo
        self._tamano += 1

    def agregar_al_inicio(self, dato):
        nuevo = self._Nodo(dato)
        nuevo.siguiente = self._cabeza
        self._cabeza = nuevo
        if self._cola is None:
            self._cola = nuevo
        self._tamano += 1

    def obtener(self, posicion):
        self._validar(posicion)
        actual = self._cabeza
        for _ in range(posicion):
            actual = actual.siguiente
        return actual.dato

    def eliminar(self, posicion):
        self._validar(posicion)
        if posicion == 0:
            eliminado = self._cabeza.dato
            self._cabeza = self._cabeza.siguiente
            if self._cabeza is None:
                self._cola = None
        else:
            anterior = self._cabeza
            for _ in range(posicion - 1):
                anterior = anterior.siguiente
            eliminado = anterior.siguiente.dato
            anterior.siguiente = anterior.siguiente.siguiente
            if anterior.siguiente is None:
                self._cola = anterior
        self._tamano -= 1
        return eliminado

    def esta_vacia(self):
        return self._tamano == 0

    def _validar(self, posicion):
        if posicion < 0 or posicion >= self._tamano:
            raise IndexError(f"Posición inválida: {posicion}")

    def __len__(self):
        return self._tamano

    def __iter__(self):
        actual = self._cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente
