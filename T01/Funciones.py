encoding = "utf-8"
import math
from collections import defaultdict , deque


def bisiesto(a):
    if a % 4 == 0 and a % 100 != 0 or a % 400 == 0:
        return True
    else:
        return False


def fecha():
    meslargo = {1, 3, 5, 7, 8, 10, 12}
    mescorto = {4, 6, 9, 11}
    while True:
        try:
            dia = int(input("Ingrese dia"))
            mes = int(input("Ingrese mes"))
            anno = int(input("Ingrese año"))
            hora = int(input("Ingrese hora (formato 24 horas"))
            minu = int(input("ingrese minutos"))
            fechafinal = [anno, mes, dia, hora, minu, 00]
            fechaprint = str(anno) + "-" + str(mes) + "-" + str(dia) + " " + str(hora) + ":" + str(minu)
            if hora >= 24 or minu >= 60:
                print("Hora incorrecta \n")

            else:
                if mes == 2:
                    if bisiesto(anno):
                        if dia > 29:
                            print("fecha incorrecta \n")

                        if dia <= 29:
                            return fechafinal

                    if not bisiesto(anno):
                        if dia > 28:
                            print("fecha incorrecta \n")
                        if dia <= 28:
                            return fechafinal

                if mes in mescorto:
                    if dia > 30:
                        print("fecha incorrecta \n")
                    if dia <= 30:
                        return fechafinal

                if mes in meslargo:
                    if dia > 31:
                        print("fecha incorrecta \n")
                    if dia <= 31:
                        return fechafinal
                if mes > 12:
                    print("fecha incorrecta \n")
        except:
            print("Datos mal ingresados")


def printer(lista):
    for fila in lista:
        for item in fila:
            print(item, end=(29 - len(str(item))) * " ")
        print()


def traslapado(Lat1, Lon1, r1, Lat2, Lon2, r2):
    dist = math.sqrt((Lat1 - Lat2) ** 2 + (Lon1 - Lon2) ** 2)
    dist *= 110000  # mts
    if (r1 + r2) >= dist:
        return True
    elif (r1 + r2) < dist:
        return False

def distancia(Lat1, Lon1, Lat2, Lon2):
    dist = math.sqrt((Lat1 - Lat2) ** 2 + (Lon1 - Lon2) ** 2)
    dist *= 110000  # mts
    return dist

def fecha1_mayor_fecha2(fecha1,fecha2):
    if int(fecha1[0])>int(fecha2[0]):
        return True
    elif int(fecha1[0])<int(fecha2[0]):
        return False
    else:
        if int(fecha1[1])>int(fecha2[1]):
            return True
        elif int(fecha1[1]) < int(fecha2[1]):
            return False
        else:
            if int(fecha1[2])>int(fecha2[2]):
                return True
            elif int(fecha1[2]) < int(fecha2[2]):
                return False
            else:
                if int(fecha1[3]) > int(fecha2[3]):
                    return True
                elif int(fecha1[3]) < int(fecha2[3]):
                    return False
                else:
                    if int(fecha1[4]) > int(fecha2[4]):
                        return True
                    elif int(fecha1[4]) < int(fecha2[4]):
                        return False


'''lista1=["2017","02","4","10","2","00"]
lista2=["2017","02","4","10","1","00"]
print(fecha1_mayor_fecha2(lista1,lista2))'''

