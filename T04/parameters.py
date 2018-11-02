import csv


def dic_parametros():
    """Funcion para extraer los parametros por defecto del enunciado, retorna un parametros"""
    archivo = csv.reader(open('Parametros_creditos.csv', 'r'))
    next(archivo)
    d = {}
    for row in archivo:
        k, v, rmin, rmax = row
        d[k] = float(v)
    archivo = csv.reader(open('Parametros_dificultad.csv', 'r'))
    next(archivo)
    for row in archivo:
        k, v = row
        try:
            d[k] = int(v)
        except ValueError:
            d[k] = float(v)
    return d


def horas():
    """metodo para cargar horas de estudio"""
    archivo = csv.reader(open('Parametros_creditos.csv', 'r'))
    next(archivo)
    d = {}
    aux = [40, 50, 55, 60]
    for row in archivo:
        k, v, rmin, rmax = row
        d[int(aux.pop(0))] = [int(rmin), int(rmax)]
    return d


def dic_escenarios():
    """Metodo para cargar escenarios"""
    archivo = csv.reader(open('escenarios.csv', 'r'))
    next(archivo)
    d = {}
    mycsv = list(archivo)
    for fila in mycsv:
        d[fila[0]] = fila[1:]
    return d


parametros = dic_parametros()
rango_horas = horas()
a = list(parametros.keys())
escenarios = dic_escenarios()
