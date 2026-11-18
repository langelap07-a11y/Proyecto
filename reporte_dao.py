from dao.conexion import Conexion
from modelo.reporte import Reporte
from tad.lista_enlazada import ListaEnlazada


class ReporteDAO:
    """Acceso a la tabla `reporte` (reportes ciudadanos)."""

    def listar(self):
        """Lista todos los reportes, del más reciente al más antiguo."""
        lista = ListaEnlazada()
        con = Conexion.obtener()
        try:
            with con.cursor() as cur:
                cur.execute("SELECT rp.id, rp.id_barrio, b.nombre AS barrio, rp.direccion, rp.tipo, "
                            "rp.descripcion, rp.estado, rp.fecha "
                            "FROM reporte rp JOIN barrio b ON b.id = rp.id_barrio "
                            "ORDER BY rp.fecha DESC, rp.id DESC")
                for f in cur.fetchall():
                    # datetime -> texto legible para el frontend
                    fecha = f["fecha"].strftime("%Y-%m-%d %H:%M") if f["fecha"] else ""
                    lista.agregar_al_final(Reporte(f["id"], f["id_barrio"], f["barrio"], f["direccion"],
                                                   f["tipo"], f["descripcion"], f["estado"], fecha))
        finally:
            con.close()
        return lista

    def crear(self, reporte):
        """Inserta un reporte nuevo (estado y fecha los pone MySQL por defecto)."""
        con = Conexion.obtener()
        try:
            with con.cursor() as cur:
                cur.execute("INSERT INTO reporte (id_barrio, direccion, tipo, descripcion) VALUES (%s, %s, %s, %s)",
                            (reporte.id_barrio, reporte.direccion, reporte.tipo, reporte.descripcion))
                nuevo_id = cur.lastrowid
            con.commit()
            return nuevo_id
        finally:
            con.close()

    def cambiar_estado(self, id_reporte, estado):
        """Actualiza el estado: Pendiente, En atención o Resuelto."""
        con = Conexion.obtener()
        try:
            with con.cursor() as cur:
                cur.execute("UPDATE reporte SET estado = %s WHERE id = %s", (estado, id_reporte))
            con.commit()
        finally:
            con.close()
