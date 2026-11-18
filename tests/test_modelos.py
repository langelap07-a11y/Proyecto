"""Pruebas de las clases del modelo (POO): herencia, composición y polimorfismo."""
import unittest

from modelo.barrio import Barrio
from modelo.entidad import Entidad
from modelo.parada import Parada
from modelo.reporte import Reporte
from modelo.ruta import Ruta


class TestModelos(unittest.TestCase):
    def test_entidad_es_abstracta(self):
        with self.assertRaises(TypeError):
            Entidad(1)

    def test_todas_las_clases_son_entidad(self):
        objetos = [
            Barrio(1, "Centro", "Urbano"),
            Parada(1, 1, "Calle 1"),
            Reporte(1, 1, "Centro", "Calle 1", "Otro", ""),
            Ruta(1, "Ruta 1", 1, "Centro", "Lunes", "06:00", "Camión"),
        ]
        for o in objetos:
            self.assertIsInstance(o, Entidad)
            self.assertIsInstance(o.to_dict(), dict)   # polimorfismo: to_dict()
            self.assertIsInstance(str(o), str)         # __str__ usa describir()

    def test_barrio_to_dict(self):
        self.assertEqual(Barrio(2, "San Rafael", "Urbano").to_dict(),
                         {"id": 2, "nombre": "San Rafael", "sector": "Urbano"})

    def test_ruta_contiene_paradas_en_orden(self):
        ruta = Ruta(1, "Ruta 1", 1, "Centro", "Lunes", "06:00", "Camión")
        ruta.agregar_parada(Parada(0, 1, "Calle A"))
        ruta.agregar_parada(Parada(0, 2, "Calle B", "Frente al parque"))
        datos = ruta.to_dict()
        self.assertEqual([p["direccion"] for p in datos["paradas"]], ["Calle A", "Calle B"])
        self.assertEqual(datos["paradas"][1]["referencia"], "Frente al parque")
        self.assertIn("2 paradas", ruta.describir())

    def test_parada_sin_referencia_queda_vacia(self):
        self.assertEqual(Parada(1, 1, "Calle A", None).referencia, "")

    def test_reporte_estado_inicial_pendiente(self):
        self.assertEqual(Reporte(1, 1, "Centro", "Calle 1", "Otro", "").to_dict()["estado"], "Pendiente")


if __name__ == "__main__":
    unittest.main()
