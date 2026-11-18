"""DAO de Barrio: único punto que habla con la tabla `barrio`."""
from dao.conexion import Conexion
from modelo.barrio import Barrio
from tad.lista_enlazada import ListaEnlazada


class BarrioDAO:
    def listar(self):
        """Devuelve todos los barrios ordenados por nombre, en una ListaEnlazada."""
        lista = ListaEnlazada()
        con = Conexion.obtener()
        try:
            with con.cursor() as cur:
                cur.execute("SELECT id, nombre, sector FROM barrio ORDER BY nombre")
                for f in cur.fetchall():
                    lista.agregar_al_final(Barrio(f["id"], f["nombre"], f["sector"]))
        finally:
            con.close()  # siempre se cierra la conexión, aunque haya error
        return lista
