from abc import ABC, abstractmethod


class Entidad(ABC):
    """Clase abstracta base de todos los objetos del sistema (herencia + abstracción)."""

    def __init__(self, id):
        self._id = id            # encapsulamiento: atributo "privado" con getter

    @property
    def id(self):
        return self._id

    @abstractmethod
    def to_dict(self):
        """Cada clase hija decide cómo se convierte en diccionario/JSON (polimorfismo)."""

    @abstractmethod
    def describir(self):
        """Texto corto para mostrar en consola."""

    def __str__(self):
        return self.describir()
