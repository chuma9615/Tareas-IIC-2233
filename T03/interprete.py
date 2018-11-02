from funciones_data import extraer_columna, filtrar, asignar, operar
from funciones_numericas import LEN, PROM, VAR, MEDIAN, DESV
from funciones_basicas import crear_funcion, graficar, evaluar
from funciones_bool import comparar_columna, comparar
from diccionario import diccionario
import matplotlib
from errores_personalizados import ExcessOrFaltaDeParametros


def interprete(querry):
    comandos = {"extraer_columna": extraer_columna, "filtrar": filtrar, "operar": operar, "evaluar": evaluar,
                "LEN": LEN, "PROM": PROM, "VAR": VAR, "MEDIAN": MEDIAN, "DESV": DESV,
                "comparar_columna": comparar_columna, "comparar": comparar, "asignar": asignar,
                "crear_funcion": crear_funcion, "graficar": graficar, "do_if": " "}
    if querry[0] not in comandos:
        return querry
    querry = [item if not isinstance(item, list) else interprete(item) for item in querry]
    una_entrada = ["LEN", "PROM", "VAR", "MEDIAN", "DESV"]
    dos_entradas = ["extraer_columna"]
    tres_entradas = ["filtrar", "operar", "comparar"]
    cuatro_entradas = ["comparar_columna"]
    datos = querry[1:]

    if querry[0] == "crear_funcion":
        nombre = querry[1]
        if not isinstance(nombre, list):
            if querry[1] in diccionario:
                nombre = diccionario[querry[1]]
        if nombre == "exponencial":
            if len(datos) != 2:
                raise ExcessOrFaltaDeParametros
            dat1 = querry[1]
            dat2 = querry[2]
            try:
                if not isinstance(dat1, list):
                    if querry[1] in diccionario:
                        dat1 = diccionario[querry[1]]
                if not isinstance(dat2, list):
                    if querry[2] in diccionario:
                        dat2 = diccionario[querry[2]]
            except TypeError:
                pass
            try:
                a = comandos[querry[0]].__call__(dat1, dat2)
                return a
            except ValueError:
                return ("ERROR: {} \n valor no apropiado".format(querry))

        if nombre == "gamma" or nombre == "normal":
            if len(datos) != 3:
                raise ExcessOrFaltaDeParametros
            dat1 = querry[1]
            dat2 = querry[2]
            dat3 = querry[3]
            if not isinstance(dat1, list):
                if querry[1] in diccionario:
                    dat1 = diccionario[querry[1]]
            if not isinstance(dat2, list):
                if querry[2] in diccionario:
                    dat2 = diccionario[querry[2]]
            if not isinstance(dat3, list):
                if querry[3] in diccionario:
                    dat3 = diccionario[querry[3]]
            try:
                a = comandos[querry[0]].__call__(dat1, dat2, dat3)
                return a
            except ValueError:
                return ("ERROR: {} \n valor no apropiado".format(querry[0]))

    if querry[0] in una_entrada:
        if len(datos) != 1:
            raise ExcessOrFaltaDeParametros
        dat1 = querry[1]
        try:
            if querry[1] in diccionario:
                dat1 = diccionario[querry[1]]
        except TypeError:
            pass
        try:
            a = comandos[querry[0]].__call__(dat1)
            return a
        except ValueError:
            return ("ERROR: {} \n valor no apropiado".format(querry[0]))
        except TypeError:
            raise TypeError("Referencia invalida")
            return ("ERROR: {} \n Referencia invalida".format((querry[0])))

    if querry[0] in dos_entradas:
        if len(datos) != 2:
            raise ExcessOrFaltaDeParametros
        dat1 = querry[1]
        dat2 = querry[2]
        try:
            if not isinstance(dat1, list):
                if querry[1] in diccionario:
                    dat1 = diccionario[querry[1]]
            if not isinstance(dat2, list):
                if querry[2] in diccionario:
                    dat2 = diccionario[querry[2]]
        except TypeError:
            pass
        try:
            a = comandos[querry[0]].__call__(dat1, dat2)
            return a
        except ValueError:
            return ("ERROR: {} \n valor no apropiado".format(querry[0:1]))

    if querry[0] == "graficar":
        if len(datos) != 2:
            raise ExcessOrFaltaDeParametros
        dat1 = querry[1]
        dat2 = querry[2]
        try:
            if not isinstance(dat1, list):
                if querry[1] in diccionario:
                    dat1 = diccionario[querry[1]]
            if not isinstance(dat2, list):
                if querry[2] in diccionario:
                    dat2 = diccionario[querry[2]]
        except TypeError:
            pass
        try:
            a = comandos[querry[0]].__call__(dat1, dat2)
            return "graficar"
        except ValueError:
            return ("ERROR: {} \n valor no apropiado".format(querry[0:1]))

    if querry[0] == "asignar":
        if len(datos) != 2:
            raise ExcessOrFaltaDeParametros
        dat1 = querry[1]
        dat2 = querry[2]
        try:
            if not isinstance(dat2, list):
                if querry[2] in diccionario:
                    dat2 = diccionario[querry[2]]
        except TypeError:
            pass
        try:
            a = comandos[querry[0]].__call__(dat1, dat2)
            return a
        except ValueError:
            return ("ERROR: {} \n valor no apropiado".format(querry[0:1]))

    if querry[0] in cuatro_entradas:
        if len(datos) != 4:
            raise ExcessOrFaltaDeParametros
        dat1 = querry[1]
        dat2 = querry[2]
        dat3 = querry[3]
        dat4 = querry[4]
        try:
            if not isinstance(dat1, list):
                if querry[1] in diccionario:
                    dat1 = diccionario[querry[1]]
            if not isinstance(dat2, list):
                if querry[2] in diccionario:
                    dat2 = diccionario[querry[2]]
            if not isinstance(dat3, list):
                if querry[3] in diccionario:
                    dat3 = diccionario[querry[3]]
            if not isinstance(dat4, list):
                if querry[4] in diccionario:
                    dat4 = diccionario[querry[4]]
        except TypeError:
            pass
        try:
            a = comandos[querry[0]].__call__(dat1, dat2, dat3, dat4)
            return a
        except ValueError:
            return ("ERROR: {} \n valor no apropiado".format(querry[0:1]))

    if querry[0] in "evaluar":
        if len(datos) != 4:
            raise ExcessOrFaltaDeParametros
        dat1 = querry[1]
        dat2 = querry[2]
        dat3 = querry[3]
        dat4 = querry[4]
        try:
            if not isinstance(dat1, list):
                if querry[1] in diccionario:
                    dat1 = diccionario[querry[1]]
            if not isinstance(dat2, list):
                if querry[2] in diccionario:
                    dat2 = diccionario[querry[2]]
            if not isinstance(dat3, list):
                if querry[3] in diccionario:
                    dat3 = diccionario[querry[3]]
            if not isinstance(dat4, list):
                if querry[4] in diccionario:
                    dat3 = diccionario[querry[4]]
        except TypeError:
            pass
        try:
            a = comandos[querry[0]].__call__(dat1, dat2, dat3, dat4)
            return list(a)
        except ValueError:
            return ("ERROR: {} \n valor no apropiado".format(querry[0:1]))

    if querry[0] in tres_entradas:
        if len(datos) != 3:
            raise ExcessOrFaltaDeParametros
        dat1 = querry[1]
        dat2 = querry[2]
        dat3 = querry[3]
        try:
            if not isinstance(dat1, list):
                if querry[1] in diccionario:
                    dat1 = diccionario[querry[1]]
            if not isinstance(dat2, list):
                if querry[2] in diccionario:
                    dat2 = diccionario[querry[2]]
            if not isinstance(dat3, list):
                if querry[3] in diccionario:
                    dat3 = diccionario[querry[3]]
        except TypeError:
            pass
        try:
            a = comandos[querry[0]].__call__(dat1, dat2, dat3)
            return a
        except ValueError:
            return "ERROR: {} \n valor no apropiado".format(querry)

    if querry[0] == "do_if":
        if len(datos) != 3:
            raise ExcessOrFaltaDeParametros
        dat1 = querry[1]
        dat2 = querry[2]
        dat3 = querry[3]
        if dat2:
            return dat1
        if not dat2:
            return dat3

    else:
        return "ERROR: {} \n valor no apropiado".format(querry[0])
