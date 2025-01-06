import unittest

from casa_encantada.datos import Localizacion, Resultado, Global
from casa_encantada.lexico import Comando, comando
from casa_encantada.main import procesar_cadena


class TestLocalizacion(unittest.TestCase):

    def test_no_hay_metodo(self):
        loc = Localizacion("", "")
        c = Comando("verbo", "nombre", "AIR", "PUERTA")
        self.assertEqual(loc.run_command(c), Resultado.NO_HECHO)  # add assertion here

    def test_comando_norte(self):
        loc1 = Localizacion("1", "")
        loc2 = Localizacion("2", "")
        loc1.conectar(0, loc2)
        estado = Global.get_instance()
        estado.set_localizacion(loc1)
        c = Comando("verbo", "nombre", "N", "*")
        self.assertEqual(loc1.run_command(c), Resultado.REINICIA)  # add assertion here
        self.assertEqual(estado.localizacion().nombre, "2")  # add assertion here

    def test_direcciones_dos_sentidos(self):
        loc1 = Localizacion("1", "")
        loc2 = Localizacion("2", "")
        loc1.conectar(0, loc2)
        self.assertEqual(len(loc2.conexiones), 1)  # add assertion here
        self.assertTrue(1 in loc2.conexiones)

    def test_procesar_cadena(self):
        self.assertListEqual(procesar_cadena("hola caracola"), ["hola", "caraco"])

####################

class Test_Lexico(unittest.TestCase):

    def test_comando_2_PALABRAS(self):
        c = comando("recoger", "pila")
        self.assertEqual(c.verbo, "recoger")  # add assertion here
        self.assertEqual(c.token_verbo, "COGER")

    def test_comando_1_PALABRa(self):
        c = comando("recoger")

        self.assertEqual(c.token_verbo, "COGER")
        self.assertEqual(c.token_nombre, "*")


if __name__ == '__main__':
    unittest.main()
