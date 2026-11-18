"""Pruebas del TAD ListaEnlazada."""
import unittest

from tad.lista_enlazada import ListaEnlazada


class TestListaEnlazada(unittest.TestCase):
    def setUp(self):
        self.lista = ListaEnlazada()

    def test_nueva_lista_esta_vacia(self):
        self.assertTrue(self.lista.esta_vacia())
        self.assertEqual(len(self.lista), 0)

    def test_agregar_al_final_conserva_el_orden(self):
        for x in ("a", "b", "c"):
            self.lista.agregar_al_final(x)
        self.assertEqual(list(self.lista), ["a", "b", "c"])

    def test_agregar_al_inicio(self):
        self.lista.agregar_al_final("b")
        self.lista.agregar_al_inicio("a")
        self.assertEqual(list(self.lista), ["a", "b"])

    def test_obtener_por_posicion(self):
        self.lista.agregar_al_final("x")
        self.lista.agregar_al_final("y")
        self.assertEqual(self.lista.obtener(1), "y")

    def test_posicion_invalida_lanza_error(self):
        with self.assertRaises(IndexError):
            self.lista.obtener(0)
        self.lista.agregar_al_final("x")
        with self.assertRaises(IndexError):
            self.lista.obtener(-1)
        with self.assertRaises(IndexError):
            self.lista.eliminar(5)

    def test_eliminar_primero_medio_y_ultimo(self):
        for x in (1, 2, 3, 4):
            self.lista.agregar_al_final(x)
        self.assertEqual(self.lista.eliminar(0), 1)   # primero
        self.assertEqual(self.lista.eliminar(1), 3)   # medio
        self.assertEqual(self.lista.eliminar(1), 4)   # último
        self.assertEqual(list(self.lista), [2])
        # La cola debe actualizarse: agregar después de eliminar el último sigue funcionando.
        self.lista.agregar_al_final(9)
        self.assertEqual(list(self.lista), [2, 9])

    def test_eliminar_hasta_vaciar(self):
        self.lista.agregar_al_final("solo")
        self.lista.eliminar(0)
        self.assertTrue(self.lista.esta_vacia())
        self.lista.agregar_al_final("nuevo")
        self.assertEqual(list(self.lista), ["nuevo"])


if __name__ == "__main__":
    unittest.main()
