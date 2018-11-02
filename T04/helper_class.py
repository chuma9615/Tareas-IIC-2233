import numpy as np
import random


class AyudanteDocencia:
    def __init__(self, name):
        """
        Clase para simular ayudantes de docencia
        :param name: Str con el nombre del ayudante
        """
        self.name = name
        self.area_dominio = np.random.choice(("POO", "HERENCIA", "LISTAS_SET_DICT", "ARBOL", "FUNCIONAL", "METACLASS",
                                              "SIMULACION", "THREADING", "GUI", "SERIALIZACION", "NETWORKING",
                                              "WEBSERVICES"), 3, False)

    def enviar_notas(self):
        pass

    def __repr__(self):
        return self.name


class AyudanteTarea:
    def __init__(self, name):
        """
        Clase para simular ayudantes de tarea
        :param name: Str con el nombre del ayudante
        """
        self.name = name

    def __repr__(self):
        return self.name


class Mavrakis:
    def __init__(self, name):
        """
        Clase para modelar al malvado dr. Mavrakis
        :param name: str Nombre del dr mavrakis
        """
        self.name = name

    def __repr__(self):
        return self.name
