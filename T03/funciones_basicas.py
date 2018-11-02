from generador import gen
import numpy as np
from functools import reduce
import matplotlib.pyplot as plt
from errores_personalizados import ImposibleProcesar

plt.ion()  # Comando necesario para no detener el proceso al graficar mediante plt.show() ya que al cerrar el grafico


#  mi funcion graficar no retornaba el strign "graficar" necesario para mostrar en consola


def rango(min, max, step):
    r = min
    while r <= max:
        yield r
        r += step


def rango2(min, max, step):
    r = min
    while r >= max:
        print(r)
        yield r
        r += step


def factorial(n):  # Para usarla en la funcion gamma
    if n < 0:
        n = n * -1
        return reduce(lambda x, y: x * y, range(1, n + 1)) * -1

    if n == 0:
        return 1
    return reduce(lambda x, y: x * y, range(1, n + 1))


def normal(mu, sigma, x):
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))


def exponencial(v, x):
    if x < 0:
        raise ImposibleProcesar("El valor de x debe ser mayor o igual a cero")

    if v <= 0:
        raise ImposibleProcesar("El valor del parametro exponencial debe der mayor a cero")
    return v * np.exp(-v * x)


def gamma(v, k, x):
    if x < 0:
        raise ImposibleProcesar("El valor de x debe ser mayor o igual a cero")
    return ((v ** k) / (factorial(k - 1))) * (x ** (k - 1)) * np.exp(-v * x)


def crear_funcion(nombre_modelo, *parametros):
    nombres = ["gamma", "exponencial", "normal"]
    if nombre_modelo not in nombres:
        raise ValueError
    if not isinstance(parametros[0], float) and not isinstance(parametros[1], float):
        if not isinstance(parametros[0], int) and not isinstance(parametros[1], int):
            raise TypeError("Parametros con mal formato")
    if nombre_modelo == "gamma":
        if len(parametros) != 2:
            raise TypeError("Error de parametros")
    if nombre_modelo == "normal":
        if len(parametros) != 2:
            raise TypeError("Error de parametros")
        mu = parametros[0]
        sigma = parametros[1]
        return (normal, mu, sigma)
    if nombre_modelo == "exponencial":
        if len(parametros) != 1:
            raise TypeError("Error de parametros")
        v = parametros[0]
        return (exponencial, v)
    if nombre_modelo == "gamma":
        if len(parametros) != 2:
            raise TypeError("Error de parametros")
        v = parametros[0]
        k = parametros[1]
        return (gamma, v, k)


def graficar(columna, opcion):
    if not isinstance(columna, list):
        raise ImposibleProcesar("solo se pueden graficar columnas")
    if opcion == "numerico":
        plt.close()
        plt.plot(columna)
        plt.show()
        # return "graficar"

    if opcion == "normalizado":
        plt.close()
        suma = sum(columna)
        columna2 = (map(lambda x: x / suma, range(0, len(columna))))
        plt.plot(np.array(list(columna2)), columna)
        plt.show()
        # return "graficar"

    if "rango:" in opcion:
        try:
            inf = opcion.split(":")[1].strip(" ").split(",")
            if len(inf) != 3:
                raise ValueError
            info = [float(i) for i in inf]
        except ValueError:
            raise ValueError("En el rango hay items que no son numeros")
        if info[0] > info[1] and info[2] >= 0:
            raise ValueError("El step debe ser negativo en este caso")
        if info[0] < info[1] and info[2] < 0:
            raise ValueError("El step debe ser positivo en este caso")
        func = rango(info[0], info[1], info[2])
        if info[0] > info[1] and info[2] < 0:
            print("{0},{1},{2}".format(info[0], info[1], info[2]))
            func = rango2(info[0], info[1], info[2])
        xaxis = [x for x in func]
        if len(xaxis) != len(columna):
            raise ValueError("Los ejes deben tener la misma dimension")
        plt.plot(xaxis, columna)
        plt.show()
        return "graficar"

    else:
        try:
            plt.plot(opcion, columna)
            plt.show()
            return "graficar"
        except ValueError as err:
            return err


def evaluar(funcion, inicio, final, intervalo):  # al usar esta funcion convertir a list!!!!!!
    if funcion[0].__name__ == "normal":
        for i in rango(inicio, final, intervalo):
            yield funcion[0].__call__(funcion[1], funcion[2], i)
    if funcion[0].__name__ == "gamma":
        for i in rango(inicio, final, intervalo):
            yield funcion[0].__call__(funcion[1], funcion[2], i)
    if funcion[0].__name__ == "exponencial":
        for i in rango(inicio, final, intervalo):
            yield funcion[0].__call__(funcion[1], i)
