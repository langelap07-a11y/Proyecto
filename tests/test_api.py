"""Pruebas de la API Flask.

No necesitan MySQL: se reemplazan los DAO por versiones en memoria.
Así se prueba la lógica de app.py (validaciones, códigos HTTP, JSON) de forma aislada.
"""
import sys
import types
import unittest

# Si PyMySQL no está instalado (p. ej. en un entorno de pruebas), se crea un módulo falso
# solo para que `import pymysql` no falle; las pruebas nunca abren una conexión real.
try:
    import pymysql  # noqa: F401
except ImportError:
    falso = types.ModuleType("pymysql")
    falso.cursors = types.SimpleNamespace(DictCursor=object)
    sys.modules["pymysql"] = falso
    sys.modules["pymysql.cursors"] = falso.cursors

import app as aplicacion
from modelo.barrio import Barrio
from modelo.reporte import Reporte
from tad.lista_enlazada import ListaEnlazada


class BarrioFalso:
    def listar(self):
        lista = ListaEnlazada()
        lista.agregar_al_final(Barrio(1, "Centro", "Urbano"))
        return lista


class RutaFalsa:
    def __init__(self):
        self.rutas = []

    def listar(self, id_barrio=None):
        lista = ListaEnlazada()
        for r in self.rutas:
            if id_barrio is None or r.id_barrio == id_barrio:
                lista.agregar_al_final(r)
        return lista

    def crear(self, ruta):
        self.rutas.append(ruta)
        return len(self.rutas)

    def eliminar(self, id_ruta):
        self.eliminada = id_ruta


class ReporteFalso:
    def __init__(self):
        self.reportes = []
        self.estado = None

    def listar(self):
        lista = ListaEnlazada()
        for r in self.reportes:
            lista.agregar_al_final(r)
        return lista

    def crear(self, reporte):
        self.reportes.append(reporte)
        return len(self.reportes)

    def cambiar_estado(self, id_reporte, estado):
        self.estado = (id_reporte, estado)


class TestApi(unittest.TestCase):
    def setUp(self):
        aplicacion.barrio_dao = BarrioFalso()
        aplicacion.ruta_dao = RutaFalsa()
        aplicacion.reporte_dao = ReporteFalso()
        self.cliente = aplicacion.app.test_client()

    def test_pagina_principal(self):
        r = self.cliente.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"EcoRutas", r.data)

    def test_archivos_estaticos(self):
        self.assertEqual(self.cliente.get("/js/app.js").status_code, 200)
        self.assertEqual(self.cliente.get("/css/estilos.css").status_code, 200)

    def test_archivo_inexistente_da_404(self):
        self.assertEqual(self.cliente.get("/no-existe.txt").status_code, 404)

    def test_listar_barrios(self):
        r = self.cliente.get("/api/barrios")
        self.assertEqual(r.get_json(), [{"id": 1, "nombre": "Centro", "sector": "Urbano"}])

    def test_crear_ruta_con_paradas(self):
        r = self.cliente.post("/api/rutas", data={
            "nombre": "Ruta X", "barrio": "1", "dia": "Lunes", "hora": "06:00",
            "vehiculo": "Camión", "paradas": "Calle A\n\nCalle B\n"})
        self.assertEqual(r.status_code, 201)
        ruta = aplicacion.ruta_dao.rutas[0]
        # Las líneas vacías se ignoran y el orden se numera 1, 2, ...
        self.assertEqual([(p.orden, p.direccion) for p in ruta.paradas], [(1, "Calle A"), (2, "Calle B")])

    def test_crear_ruta_incompleta_da_400(self):
        r = self.cliente.post("/api/rutas", data={"nombre": "", "barrio": "1", "dia": "Lunes", "hora": "06:00"})
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.get_json())

    def test_filtrar_rutas_por_barrio(self):
        for barrio in ("1", "2"):
            self.cliente.post("/api/rutas", data={"nombre": "R" + barrio, "barrio": barrio,
                                                  "dia": "Lunes", "hora": "06:00"})
        self.assertEqual(len(self.cliente.get("/api/rutas").get_json()), 2)
        self.assertEqual(len(self.cliente.get("/api/rutas?barrio=2").get_json()), 1)

    def test_eliminar_ruta(self):
        r = self.cliente.delete("/api/rutas/7")
        self.assertEqual(r.get_json(), {"ok": True})
        self.assertEqual(aplicacion.ruta_dao.eliminada, 7)

    def test_crear_reporte(self):
        r = self.cliente.post("/api/reportes", data={
            "barrio": "1", "direccion": "Calle 4", "tipo": "No pasó el camión"})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(aplicacion.reporte_dao.reportes[0].direccion, "Calle 4")

    def test_crear_reporte_sin_direccion_da_400(self):
        r = self.cliente.post("/api/reportes", data={"barrio": "1", "direccion": " ", "tipo": "Otro"})
        self.assertEqual(r.status_code, 400)

    def test_listar_reportes(self):
        aplicacion.reporte_dao.reportes.append(Reporte(1, 1, "Centro", "Calle 4", "Otro", ""))
        self.assertEqual(self.cliente.get("/api/reportes").get_json()[0]["estado"], "Pendiente")

    def test_cambiar_estado_valido_e_invalido(self):
        ok = self.cliente.put("/api/reportes/3", data={"estado": "Resuelto"})
        self.assertEqual(ok.status_code, 200)
        self.assertEqual(aplicacion.reporte_dao.estado, (3, "Resuelto"))
        malo = self.cliente.put("/api/reportes/3", data={"estado": "Inventado"})
        self.assertEqual(malo.status_code, 400)

    def test_error_inesperado_se_devuelve_como_json_500(self):
        class Roto:
            def listar(self):
                raise RuntimeError("MySQL caído")
        aplicacion.barrio_dao = Roto()
        r = self.cliente.get("/api/barrios")
        self.assertEqual(r.status_code, 500)
        self.assertIn("MySQL", r.get_json()["error"])


if __name__ == "__main__":
    unittest.main()
