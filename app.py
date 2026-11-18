"""EcoRutas - Rutas de recolección de basura (Python + Flask + MySQL de XAMPP)."""
import os

from flask import Flask, jsonify, request, send_from_directory
from werkzeug.exceptions import HTTPException

from dao.barrio_dao import BarrioDAO
from dao.reporte_dao import ReporteDAO
from dao.ruta_dao import RutaDAO
from modelo.parada import Parada
from modelo.reporte import Reporte
from modelo.ruta import Ruta

# La carpeta web se calcula desde la ubicación de este archivo,
# así funciona sin importar desde dónde ejecutes el programa.
BASE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(BASE, "web")

app = Flask(__name__, static_folder=None)

# Un DAO por entidad: app.py nunca escribe SQL, solo pide datos a los DAO.
barrio_dao = BarrioDAO()
ruta_dao = RutaDAO()
reporte_dao = ReporteDAO()

# Estados válidos de un reporte (se validan en el servidor, no solo en el navegador).
ESTADOS = ("Pendiente", "En atención", "Resuelto")


def a_json(lista):
    """Convierte cualquier lista de entidades en JSON (polimorfismo: to_dict())."""
    return jsonify([e.to_dict() for e in lista])


def error(mensaje, codigo=400):
    """Respuesta de error uniforme: {"error": "..."} con el código HTTP indicado."""
    return jsonify({"error": mensaje}), codigo


# ---------------- API ----------------
@app.get("/api/barrios")
def barrios():
    """GET /api/barrios -> lista de barrios/veredas."""
    return a_json(barrio_dao.listar())


@app.get("/api/rutas")
def listar_rutas():
    """GET /api/rutas[?barrio=ID] -> rutas con sus paradas."""
    id_barrio = request.args.get("barrio", type=int)
    return a_json(ruta_dao.listar(id_barrio))


@app.post("/api/rutas")
def crear_ruta():
    """POST /api/rutas -> crea una ruta; el campo `paradas` trae una dirección por línea."""
    f = request.form
    nombre = f.get("nombre", "").strip()
    dia = f.get("dia", "").strip()
    hora = f.get("hora", "").strip()
    vehiculo = f.get("vehiculo", "").strip()
    id_barrio = f.get("barrio", type=int)
    if not nombre or not dia or not hora or id_barrio is None:
        return error("Completa nombre, barrio, día y hora")

    ruta = Ruta(0, nombre, id_barrio, "", dia, hora, vehiculo)
    orden = 1  # el orden de las paradas es el orden de las líneas escritas
    for linea in f.get("paradas", "").splitlines():
        if linea.strip():
            ruta.agregar_parada(Parada(0, orden, linea.strip(), ""))
            orden += 1
    return jsonify({"id": ruta_dao.crear(ruta)}), 201


@app.delete("/api/rutas/<int:id_ruta>")
def eliminar_ruta(id_ruta):
    """DELETE /api/rutas/<id> -> elimina la ruta y (por CASCADE) sus paradas."""
    ruta_dao.eliminar(id_ruta)
    return jsonify({"ok": True})


@app.get("/api/reportes")
def listar_reportes():
    """GET /api/reportes -> reportes ciudadanos, el más reciente primero."""
    return a_json(reporte_dao.listar())


@app.post("/api/reportes")
def crear_reporte():
    """POST /api/reportes -> registra un reporte (barrio, dirección y tipo son obligatorios)."""
    f = request.form
    direccion = f.get("direccion", "").strip()
    tipo = f.get("tipo", "").strip()
    id_barrio = f.get("barrio", type=int)
    if not direccion or not tipo or id_barrio is None:
        return error("Completa barrio, dirección y tipo")
    reporte = Reporte(0, id_barrio, "", direccion, tipo, f.get("descripcion", "").strip())
    return jsonify({"id": reporte_dao.crear(reporte)}), 201


@app.put("/api/reportes/<int:id_reporte>")
def cambiar_estado(id_reporte):
    """PUT /api/reportes/<id> -> cambia el estado del reporte."""
    estado = request.form.get("estado", "")
    if estado not in ESTADOS:
        return error("Estado inválido")
    reporte_dao.cambiar_estado(id_reporte, estado)
    return jsonify({"ok": True})


@app.errorhandler(Exception)
def manejar_error(e):
    """Cualquier error inesperado (p. ej. MySQL caído) se devuelve como JSON 500, no como página HTML."""
    if isinstance(e, HTTPException):
        return e
    print("ERROR:", e)
    return error(str(e), 500)


# ---------------- Frontend (carpeta web/) ----------------
@app.get("/")
def inicio():
    """Sirve la página principal."""
    return send_from_directory(WEB, "index.html")


@app.get("/<path:ruta>")
def archivos(ruta):
    """Sirve css/js. send_from_directory impide salir de la carpeta web/ (seguridad)."""
    return send_from_directory(WEB, ruta)


if __name__ == "__main__":
    print("Carpeta web:", WEB, "->", "OK" if os.path.isfile(os.path.join(WEB, "index.html")) else "NO existe index.html")
    try:
        print("Conexión a MySQL correcta. Barrios registrados:", len(barrio_dao.listar()))
    except Exception as e:
        print("AVISO: no se pudo conectar a la base de datos ->", e)
        print("Revisa que MySQL esté iniciado en XAMPP y que importaste database/schema.sql")
    print("Aplicación lista en http://localhost:5000  (Ctrl+C para detener)")
    app.run(host="127.0.0.1", port=5000, debug=False)
