from modelo.entidad import Entidad


class Reporte(Entidad):
    """Reporte ciudadano: la comunidad avisa cuando la recolección falla."""

    def __init__(self, id, id_barrio, barrio, direccion, tipo, descripcion, estado="Pendiente", fecha=""):
        super().__init__(id)
        self._id_barrio = id_barrio
        self._barrio = barrio
        self._direccion = direccion
        self._tipo = tipo
        self._descripcion = descripcion
        self._estado = estado
        self._fecha = fecha

    @property
    def id_barrio(self):
        return self._id_barrio

    @property
    def direccion(self):
        return self._direccion

    @property
    def tipo(self):
        return self._tipo

    @property
    def descripcion(self):
        return self._descripcion

    def to_dict(self):
        return {
            "id": self._id,
            "barrio": self._barrio,
            "direccion": self._direccion,
            "tipo": self._tipo,
            "descripcion": self._descripcion,
            "estado": self._estado,
            "fecha": self._fecha,
        }

    def describir(self):
        return f"Reporte #{self._id} - {self._tipo} en {self._direccion}"
