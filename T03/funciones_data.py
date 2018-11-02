from funciones_numericas import LEN, PROM, VAR, MEDIAN, DESV
from generador import gen
from functools import reduce
from diccionario import diccionario
from errores_personalizados import ImposibleProcesar


def extraer_columna(archivo, columna):
    with open(archivo + ".csv", "r") as file:
        encabezado = next(file).strip("\n").split(";")
        encabeza3 = [item.split(":")[0] for item in encabezado]
        fila = [True if columna in item else False for item in encabezado]
        numero = (fila.index(True))
        if columna not in encabeza3:
            raise ImposibleProcesar("Columna no existe")

        if "float" in encabezado[numero]:
            return [float(i.split(";")[numero]) for i in file]
        if "int" in encabezado[numero]:
            return [int(i.split(";")[numero]) for i in file]
        if "str" in encabezado[numero]:
            return [str(i.split(";")[numero]) for i in file]


def filtrar(columna, simbolo, valor):
    simb = ["<", ">", "==", ">=", "<=", "!="]
    if simbolo not in simb:
        raise TypeError("Simbolo no valido")
    if not isinstance(valor, int) and not isinstance(valor, float):
        raise TypeError("valor invalido")
    try:
        if simbolo == ">=":
            resultado = filter(lambda x: x >= valor, columna)
            return list(resultado)
        if simbolo == "<=":
            resultado = filter(lambda x: x <= valor, columna)
            return list(resultado)
        if simbolo == "==":
            resultado = filter(lambda x: x == valor, columna)
            return list(resultado)
        if simbolo == "<":
            resultado = filter(lambda x: x < valor, columna)
            return list(resultado)
        if simbolo == ">":
            resultado = filter(lambda x: x > valor, columna)
            return list(resultado)
    except TypeError:
        raise TypeError("Referencia invalida")


def asignar(variable, comando_o_dato):
    prohibidos = ["extraer_columna", "filtrar", "crear_funcion", "graficar", "operar", "evaluar", "LEN", "PROM", "VAR",
                  "MEDIAN", "DESV", "comparar columna", "comparar", "do_if", "gamma", "exponencial", "normal",
                  "asignar"]
    if variable in prohibidos or not isinstance(variable, str):
        raise ValueError("Este comando es propio de RQL")
    else:
        diccionario[variable] = comando_o_dato
    return "asignar"


def operar(columna, simbolo, valor):
    operandos = [">=<", "*", "**", "+", "/"]
    if simbolo not in operandos:
        raise TypeError("simbolo no valido")
    if not isinstance(valor, int) and not isinstance(valor, float):
        return TypeError("valor invalido")
    if simbolo == "*":
        resultado = map(lambda x: x * valor, columna)
        return list(resultado)
    if simbolo == "**":
        resultado = map(lambda x: x ** valor, columna)
        return list(resultado)
    if simbolo == "+":
        resultado = map(lambda x: x + valor, columna)
        return list(resultado)
    if simbolo == "-":
        resultado = map(lambda x: x - valor, columna)
        return list(resultado)
    if simbolo == "/":
        if valor == 0:
            raise ZeroDivisionError("Division por cero")
        resultado = map(lambda x: x / valor, columna)
        return list(resultado)
    if simbolo == ">=<":
        if valor < 0:
            raise TypeError("El valor en una aproximacion debe ser no negativo")
        resultado = map(lambda x: round(x, valor), columna)
        return list(resultado)
