from datetime import timedelta

from dao.conexion import Conexion
from modelo.parada import Parada
from modelo.ruta import Ruta
from tad.lista_enlazada import ListaEnlazada


def _hora(valor):
    """MySQL devuelve TIME como timedelta; lo convertimos a 'HH:MM'."""
    if isinstance(valor, timedelta):
        total = int(valor.total_seconds())
        return f"{total // 3600:02d}:{(total % 3600) // 60:02d}"
    return str(valor)[:5]


class RutaDAO:
    """Acceso a las tablas `ruta` y `parada`."""

    def listar(self, id_barrio=None):
        """Lista las rutas (con sus paradas ordenadas). Si se pasa id_barrio, filtra por ese barrio."""
        lista = ListaEnlazada()
        sql = ("SELECT r.id, r.nombre, r.id_barrio, b.nombre AS barrio, r.dia_semana, r.hora_inicio, r.vehiculo "
               "FROM ruta r JOIN barrio b ON b.id = r.id_barrio ")
        params = ()
        if id_barrio is not None:
            sql += "WHERE r.id_barrio = %s "
            params = (id_barrio,)
        sql += "ORDER BY b.nombre, r.hora_inicio"
        # Se usan parámetros (%s) y no concatenación: evita inyección SQL.

        con = Conexion.obtener()
        try:
            with con.cursor() as cur:
                cur.execute(sql, params)
                filas = cur.fetchall()
                for f in filas:
                    ruta = Ruta(f["id"], f["nombre"], f["id_barrio"], f["barrio"],
                                f["dia_semana"], _hora(f["hora_inicio"]), f["vehiculo"])
                    # Composición: cada Ruta carga sus propias paradas, ya ordenadas.
                    cur.execute("SELECT id, orden, direccion, referencia FROM parada "
                                "WHERE id_ruta = %s ORDER BY orden", (ruta.id,))
                    for p in cur.fetchall():
                        ruta.agregar_parada(Parada(p["id"], p["orden"], p["direccion"], p["referencia"]))
                    lista.agregar_al_final(ruta)
        finally:
            con.close()
        return lista

    def crear(self, ruta):
        """Inserta la ruta y todas sus paradas en una sola transacción."""
        con = Conexion.obtener()
        try:
            with con.cursor() as cur:
                cur.execute("INSERT INTO ruta (nombre, id_barrio, dia_semana, hora_inicio, vehiculo) "
                            "VALUES (%s, %s, %s, %s, %s)",
                            (ruta.nombre, ruta.id_barrio, ruta.dia_semana, ruta.hora_inicio, ruta.vehiculo))
                id_ruta = cur.lastrowid
                for p in ruta.paradas:
                    cur.execute("INSERT INTO parada (id_ruta, orden, direccion, referencia) "
                                "VALUES (%s, %s, %s, %s)",
                                (id_ruta, p.orden, p.direccion, p.referencia))
            con.commit()
            return id_ruta
        except Exception:
            con.rollback()
            raise
        finally:
            con.close()

    def eliminar(self, id_ruta):
        """Borra la ruta; sus paradas se eliminan solas (ON DELETE CASCADE en el esquema)."""
        con = Conexion.obtener()
        try:
            with con.cursor() as cur:
                cur.execute("DELETE FROM ruta WHERE id = %s", (id_ruta,))
            con.commit()
        finally:
            con.close()
