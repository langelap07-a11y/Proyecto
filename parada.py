from modelo.entidad import Entidad


class Parada(Entidad):
    def __init__(self, id, orden, direccion, referencia=""):
        super().__init__(id)
        self._orden = orden
        self._direccion = direccion
        self._referencia = referencia or ""

    @property
    def orden(self):
        return self._orden

    @property
    def direccion(self):
        return self._direccion

    @property
    def referencia(self):
        return self._referencia

    def to_dict(self):
        return {"orden": self._orden, "direccion": self._direccion, "referencia": self._referencia}

    def describir(self):
        return f"{self._orden}. {self._direccion}"
