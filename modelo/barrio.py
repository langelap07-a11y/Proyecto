from modelo.entidad import Entidad


class Barrio(Entidad):
    def __init__(self, id, nombre, sector):
        super().__init__(id)
        self._nombre = nombre
        self._sector = sector

    @property
    def nombre(self):
        return self._nombre

    @property
    def sector(self):
        return self._sector

    def to_dict(self):
        return {"id": self._id, "nombre": self._nombre, "sector": self._sector}

    def describir(self):
        return f"Barrio {self._nombre} ({self._sector})"
