import math
import numpy
from functools import reduce

from generador import gen


def LEN(datos):  # recibe listas
    return len(datos)


def PROM(datos):
    numero = reduce(lambda x, y: x + y, gen(datos))
    return numero / LEN(list(datos))


def DESV(datos):
    promedio = PROM((datos))
    return ((sum(map(lambda x: (x - promedio) ** 2, gen(datos)))) / (LEN(datos) - 1)) ** 0.5


def VAR(datos):
    return DESV(datos) ** 2


def MEDIAN(datos):
    indice = (len(datos) / 2) - 1
    if 0 == len(datos) % 2:
        num1 = datos[int(indice)]
        num2 = datos[int(indice) + 1]
        return (num1 + num2) / 2
    else:
        return datos[int(indice + 0.5)]
