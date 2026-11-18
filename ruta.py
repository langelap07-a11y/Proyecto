from modelo.entidad import Entidad
from tad.lista_enlazada import ListaEnlazada


class Ruta(Entidad):
    """Ruta de recolección. Contiene sus paradas en un TAD ListaEnlazada (composición)."""

    def __init__(self, id, nombre, id_barrio, barrio, dia_semana, hora_inicio, vehiculo):
        super().__init__(id)
        self._nombre = nombre
        self._id_barrio = id_barrio
        self._barrio = barrio
        self._dia_semana = dia_semana
        self._hora_inicio = hora_inicio
        self._vehiculo = vehiculo
        self._paradas = ListaEnlazada()

    def agregar_parada(self, parada):
        self._paradas.agregar_al_final(parada)

    @property
    def nombre(self):
        return self._nombre

    @property
    def id_barrio(self):
        return self._id_barrio

    @property
    def dia_semana(self):
        return self._dia_semana

    @property
    def hora_inicio(self):
        return self._hora_inicio

    @property
    def vehiculo(self):
        return self._vehiculo

    @property
    def paradas(self):
        return self._paradas

    def to_dict(self):
        return {
            "id": self._id,
            "nombre": self._nombre,
            "idBarrio": self._id_barrio,
            "barrio": self._barrio,
            "dia": self._dia_semana,
            "hora": self._hora_inicio,
            "vehiculo": self._vehiculo,
            "paradas": [p.to_dict() for p in self._paradas],
        }

    def describir(self):
        return f"{self._nombre} - {self._dia_semana} {self._hora_inicio} ({len(self._paradas)} paradas)"
