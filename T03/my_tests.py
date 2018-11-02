from funciones_data import filtrar, asignar, operar
from funciones_numericas import PROM, VAR, MEDIAN, DESV  # listo
from funciones_basicas import evaluar, graficar, exponencial
from funciones_bool import comparar_columna
from interprete import interprete
import unittest
import numpy as np
from diccionario import diccionario
from errores_personalizados import ExcessOrFaltaDeParametros, ImposibleProcesar


class Testear_Funcionalidad(unittest.TestCase):
    def test_PROM(self):
        self.assertEqual(PROM([4, 8, 2, 6, 4, 32, 98746, 3, 1]),
                         np.mean([4, 8, 2, 6, 4, 32, 98746, 3, 1]))  # testeando funcion prom y comparando con
        # funcion prom de numpy

    def test_VAR(self):
        self.assertEqual(VAR([4, 8, 2, 6, 4, 32, 98746, 3, 1]), np.var([4, 8, 2, 6, 4, 32, 98746, 3, 1],
                                                                       ddof=1))  # Var si calcula correctamente la varianza de una muestra (ddof=1)

    def test_MEDIAN(self):
        self.assertEqual(MEDIAN([4, 8, 2, 6, 4, 32, 98746, 3, 1]),
                         np.median([4, 8, 2, 6, 4, 32, 98746, 3,
                                    1]))  # testeo de la funcion median comparado con modulo numpy

    def test_DESV(self):
        self.assertEqual(DESV([4, 8, 2, 6, 4, 32, 98746, 3, 1]), np.std([4, 8, 2, 6, 4, 32, 98746, 3, 1],
                                                                        ddof=1))  # Desv si calcula correctamente la
        # varianza de una muestra (ddof=1)

    def test_filtrar(self):
        self.assertEqual(filtrar([1, 1, 1, 3, 3, 3, 4, 5], ">", 4), [5])  # Testeando la funcion filtrar

    def test_evaluar(self):
        self.assertEqual(round(interprete(["VAR", ["evaluar", ["crear_funcion", "normal", 0, 0.5], -3, 5, 0.1]]), 3),
                         0.055)  # Evaluar si devuelve el valor que se espera

    def test_do_if(self):
        self.assertEqual(interprete(["do_if", ["PROM", [1, 2, 3]], True, ["PROM", [2, 2]]]),
                         2)  # Evaluar Do if y su funcionamiento

    def test_asignar(self):  # Testear funcion asignar
        asignar("x", 10)
        self.assertEqual(diccionario["x"], 10)

    def test_comparar_columna(self):
        self.assertTrue(comparar_columna([i for i in range(0, 100)], ">", "PROM", [i for i in range(0, 30)]))


class Testear_Errores(
    unittest.TestCase):  # En ciertos casos de los errores debemos llamar a las funciones
    # mediante el interprete para asi probar su robustez

    def test_error_de_tipo(self):
        with self.assertRaises(TypeError) as context:
            filtrar([1, 1, 1, 3, 3, 3, 4, 5], ">", "lkdsm")
        self.assertTrue("valor invalido" in str(
            context.exception))  # Aqui se prueba que al agregar argumentos incorrectos a una funcion esta lanza un
        # error de tipo

    def test_argumento_invalido(self):
        with self.assertRaises(ExcessOrFaltaDeParametros) as context:
            interprete(["PROM", 1, 2, 3, 4])
            self.assertTrue("Argumento invalido, parametros incorrectos" in str(
                context.exception))  # Aqui se testea el error de argumento invalido con excepciones personalizadas

    def test_division_por_cero(self):
        with self.assertRaises(ZeroDivisionError) as context:
            operar([1, 2, 3, 4], "/", 0)
            self.assertTrue("Division por cero" in str(context.exception))  # Testeando la division por cero

    def test_imposible_procesar(self):
        with self.assertRaises(ImposibleProcesar) as context:
            exponencial(-4, 3)
            self.assertTrue("mayor o igual a cero" in str(context.exception))

    def test_referencia_invalida(self):
        with self.assertRaises(TypeError) as context:
            interprete(["PROM", "x"])
            self.assertTrue("Referencia Invalida" in str(context.exception))


suite = unittest.TestLoader().loadTestsFromTestCase(Testear_Funcionalidad)

unittest.TextTestRunner().run(suite)
suite = unittest.TestLoader().loadTestsFromTestCase(Testear_Errores)
unittest.TextTestRunner().run(suite)
