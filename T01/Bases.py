encoding = "utf-8"
import Funciones as fx
from math import pi
import os


class BaseDatos:
    def crear_archivo(self, nombre):
        archivo = open(nombre, "w")
        for line in archivo:
            print(line)

    def __init__(self, nombre):
        self.incendios_apagados = []
        self.nombre=nombre
        self.lista = []
        archivo = open(nombre, "r")
        self.fila = ""

        for linea in archivo:
            x = linea.strip("\n")
            nueva = x.split(",")

            self.lista.append(nueva)
        archivo.close()

    def buscafilas(self, palabra, columna):
        for fila in range(len(self.lista)):
            if palabra in self.lista[fila][columna]:
                return fila

    def manipular_fecha(self, fechastring):
        dias = fechastring[:10]
        nuevosdias = dias.split("-")
        horas = fechastring[11:]
        nuevashoras = horas.split(":")
        for i in nuevashoras:
            nuevosdias.append(i)
        return nuevosdias

    def encontrar_indice(self, keyword):
        aux = ""
        aux = (self.lista[0])
        indice = aux.index(str(keyword))
        return indice

    def search(self, palabra, tipo):
        indice = self.encontrar_indice(tipo)
        for r in range(len(self.lista)):
            if palabra == self.lista[r][indice]:
                self.fila = r
                return True
        else:
            return False

    def es_anaf(self):
        indice = self.encontrar_indice("recurso_id:string")
        if self.lista[self.fila][indice] == "":
            return True
        else:
            return False

    def __str__(self):
        for fila in self.lista:
            for item in fila:
                print(item, end=(29 - len(str(item))) * " ")
            print()
        return ""


class Incendio(BaseDatos):
    def __init__(self, id):
        self.id = id
        super().__init__("incendios.csv")
        aux = super().encontrar_indice("id:string")
        self.incendio_individual = ""
        for r in range(len(self.lista)):
            if str(id) == self.lista[r][aux]:
                self.incendio_individual = self.lista[r]
        self.radio = 1
        self.superficie_afectada = pi * (self.radio ** 2)
        self.potencia = int(self.incendio_individual[self.encontrar_indice("potencia:int")])
        self.puntos_poder = int(self.superficie_afectada * self.potencia)
        self.fechaincendio = self.manipular_fecha(
            self.incendio_individual[self.encontrar_indice("fecha_inicio:string")])
        self.lat = float(self.incendio_individual[self.encontrar_indice("lat:float")])
        self.lon = float(self.incendio_individual[self.encontrar_indice("lon:float")])
        if len(recursos.lista[0])==9:
            recursos.lista[0].append("distancia a objetivo")
            recursos.lista[0].append("estado actual")
            recursos.lista[0].append("Incendio asignado")
            recursos.lista[0].append("Minutos en uso")

            for item in recursos.lista[1:]:
                item.append(fx.distancia(self.lat, self.lon, float(item[recursos.encontrar_indice("lat:float")]),
                                         float(item[recursos.encontrar_indice("lon:float")])))
                item.append("Standby")
                item.append("")
                item.append(0)
        elif len(recursos.lista[0])!=9:
            for item in recursos.lista[1:]:
                item[9]=(fx.distancia(self.lat, self.lon, float(item[recursos.encontrar_indice("lat:float")]),
                                         float(item[recursos.encontrar_indice("lon:float")])))



    def simular(self, fechaactual, tipo_extincion):
        meteo_incidente = []
        meslargo = {1, 3, 5, 7, 8, 10}
        mescorto = {4, 6, 9, 11}
        self.radio = 0
        viento = 0
        lluvia = 0
        temp = 0
        fechai = meteorologia.encontrar_indice("fecha_inicio:string")
        fechat = meteorologia.encontrar_indice("fecha_termino:string")
        numbes = ""
        fechaactual = list(map(int, fechaactual))
        list(map(str, fechaactual))
        self.fechaincendio = list(map(int, self.fechaincendio))
        presente = None
        aux2 = ""
        if fx.fecha1_mayor_fecha2(self.fechaincendio,fechaactual):
            print()
            print("Este incendio aun no comienza")
            print()
            return
        while self.puntos_poder > 0:
            for item in meteorologia.lista[1:]:
                if self.fechaincendio == list(map(int, self.manipular_fecha(item[fechai]))) and fx.traslapado(self.lat,
                                                                                                              self.lon,
                                                                                                              self.radio,
                                                                                                              float(
                                                                                                                  item[
                                                                                                                      meteorologia.encontrar_indice(
                                                                                                                          "lat:float")]),
                                                                                                              float(
                                                                                                                  item[
                                                                                                                      meteorologia.encontrar_indice(
                                                                                                                          "lon:float")]),
                                                                                                              int(item[
                                                                                                                      meteorologia.encontrar_indice(
                                                                                                                          "radio:int")])):
                    meteo_incidente.append(item[meteorologia.encontrar_indice("id:string")])
                    if item[(meteorologia.encontrar_indice("tipo:string"))] == "VIENTO":
                        print("empezo viento")
                        viento = (float(item[meteorologia.encontrar_indice("valor:float")])) * 36
                    if item[(meteorologia.encontrar_indice("tipo:string"))] == "TEMPERATURA":
                        print("empezo temperatura")
                        t = float(item[meteorologia.encontrar_indice("valor:float")])
                        if t == 30:
                            temp = 0
                        if t > 30:
                            temp = t - 30
                        if t < 30:
                            temp = t - 30
                    if item[(meteorologia.encontrar_indice("tipo:string"))] == "LLUVIA":
                        lluvia = 50 * (float(item[meteorologia.encontrar_indice("valor:float")]))
                        print("empezo lluvia")

                if self.fechaincendio == list(map(int, self.manipular_fecha(item[fechat]))) and item[
                    meteorologia.encontrar_indice("id:string")] in meteo_incidente:
                    if item[meteorologia.encontrar_indice("tipo:string")] == "VIENTO":
                        viento = 0
                        print("paro vineto")
                    if item[meteorologia.encontrar_indice("tipo:string")] == "TEMPERATURA":
                        temp = 0
                        print("paro temperatura")
                    if item[meteorologia.encontrar_indice("tipo:string")] == "LLUVIA":
                        lluvia = 0
                        print("paro lluvia")

            if self.fechaincendio[4] <= 60:
                self.fechaincendio[4] += 1
                self.radio += (500 / 60) + (viento / 60) + (temp / 60) + (lluvia / 60)
            if self.fechaincendio[4] == 60 and self.fechaincendio[3] <= 23:
                # self.radio += 500- 60*(500/60)
                self.fechaincendio[3] += 1
                self.fechaincendio[4] = 0
            if self.fechaincendio[3] == 24:
                print(self.fechaincendio)
                if self.fechaincendio[1] == 2 and fx.bisiesto(self.fechaincendio[0]):
                    if self.fechaincendio[2] <= 29:
                        self.fechaincendio[3] = 0
                        self.fechaincendio[2] += 1
                    if self.fechaincendio[2] == 30:
                        self.fechaincendio[1] += 1
                        self.fechaincendio[2] = 1
                elif self.fechaincendio[1] == 2 and not fx.bisiesto(self.fechaincendio[0]):
                    if self.fechaincendio[2] <= 28:
                        self.fechaincendio[3] = 0
                        self.fechaincendio[2] += 1
                    if self.fechaincendio[2] == 29:
                        self.fechaincendio[1] += 1
                        self.fechaincendio[2] = 1
                elif self.fechaincendio[1] in meslargo:
                    # if self.fechaincendio[2]==0 and self.fechaincendio[1]==8:
                    #   self.fechaincendio[2]=1
                    if self.fechaincendio[2] <= 31:
                        self.fechaincendio[3] = 0
                        self.fechaincendio[2] += 1
                    if self.fechaincendio[2] == 32:
                        self.fechaincendio[1] += 1
                        self.fechaincendio[2] = 1
                elif self.fechaincendio[1] in mescorto:
                    if self.fechaincendio[2] <= 30:
                        self.fechaincendio[3] = 0
                        self.fechaincendio[2] += 1
                    if self.fechaincendio[2] == 31:
                        self.fechaincendio[1] += 1
                        self.fechaincendio[2] = 1
                elif self.fechaincendio[1] == 12:
                    self.fechaincendio[3] = 0
                    self.fechaincendio[2] += 1
                    if self.fechaincendio[1] == 12 and self.fechaincendio[2] == 32:
                        self.fechaincendio[0] += 1
                        self.fechaincendio[1] = 1
                        self.fechaincendio[2] = 1
            self.superficie_afectada = pi * (self.radio ** 2)
            self.puntos_poder = int(self.superficie_afectada * self.potencia)

            if self.fechaincendio == fechaactual:  # Para verificar que se termino el calculo del incendio y comenzar a enviar recursos
                presente = True
            if self.fechaincendio != fechaactual:
                presente = False
            if presente:
                if tipo_extincion == 2:
                    aux = sorted(recursos.lista[1:], key=lambda x: (x[9]))
                    print(aux)

                    aux2 = aux[:100]
                if tipo_extincion == 1:
                    aux = sorted(recursos.lista[1:], key=lambda x: (x[9]))
                    aux2 = aux[:2]
                if tipo_extincion == 3:
                    aux = sorted(recursos.lista[1:], key=lambda x: (x[recursos.encontrar_indice("costo:int")]))
                    aux2 = aux[:10]

            if aux2 != "":
                for item in aux2:
                    filageneral = recursos.buscafilas(item[recursos.encontrar_indice('id:string')],
                                                      recursos.encontrar_indice('id:string'))
                    columnavelocidad = recursos.encontrar_indice("velocidad:int")
                    if int(item[9]) > 0 and (recursos.lista[filageneral][10]=="Standby"):

                        recursos.lista[filageneral][12]=int(recursos.lista[filageneral][12])+1
                        recursos.lista[filageneral][10] = "Standby"
                        recursos.lista[filageneral][11] = self.id
                        recursos.lista[filageneral][9] =  int(recursos.lista[filageneral][9]) - int(recursos.lista[filageneral][columnavelocidad])
                    if item[9] <= 0:
                        recursos.lista[filageneral][10] = "Standby"
                        recursos.lista[filageneral][12] = int(recursos.lista[filageneral][12]) + 1
                        self.puntos_poder -= (int(item[recursos.encontrar_indice("tasa_extincion:int")]))
                        print("se esta apagando")
        print()
        print("incendio apagado")
        print()
        incendios_apagados=open("incendios apagados.txt","a")
        print(self.incendio_individual+aux2, file=incendios_apagados)
        incendios_apagados.close

        if tipo_extincion==2:
            directorio_tarea=os.getcwd()
            os.chdir(os.getcwd() + "/Reportes Estrategias de Extincion")
            estrategia_usada=open(str(self.id)+"Tiempo de extincion.txt","w")
            for line in aux2:
                line = list(map(str, line))
                a = ","
                q = a.join(line)
                print(q, file=estrategia_usada)
            estrategia_usada.close()
            os.chdir(directorio_tarea)

        if tipo_extincion==1:
            directorio_tarea=os.getcwd()
            os.chdir(os.getcwd() + "/Reportes Estrategias de Extincion")
            estrategia_usada=open(str(self.id)+"Cantidad de recursos.txt","w")
            for line in aux2:
                line = list(map(str, line))
                a = ","
                q = a.join(line)
                print(q, file=estrategia_usada)
            estrategia_usada.close()
            os.chdir(directorio_tarea)

        if tipo_extincion==3:
            directorio_tarea=os.getcwd()
            os.chdir(os.getcwd() + "/Reportes Estrategias de Extincion")
            estrategia_usada=open(str(self.id)+"Costo economico.txt","w")
            for line in aux2:
                line = list(map(str, line))
                a = ","
                q = a.join(line)
                print(q, file=estrategia_usada)
            estrategia_usada.close()
            os.chdir(directorio_tarea)


        guardar = open("recursos.csv", "w")
        for line in recursos.lista:
            line=list(map(str, line))
            a = ","
            q = a.join(line)
            print(q, file=guardar)
        guardar.close()

    def __str__(self):
        print(" ".join(self.incendio_individual))

        return ""


class Persona(BaseDatos):
    def __init__(self, nombre, password):
        super().__init__("usuarios.csv")
        self.nombre = nombre
        self.password = password

    def search(self, palabra, columna):
        for r in range(len(self.lista) - 1):
            if palabra in self.lista[r][columna]:
                return r


class Plebe(Persona):
    def __init__(self, persona, password):
        super().__init__(persona, password)
        self.id=usuarios.lista[usuarios.buscafilas(persona,usuarios.encontrar_indice("nombre:string"))][usuarios.encontrar_indice("recurso_id:string")]


    def menu(self):
        print("Que desea hacer?")
        print("1. Ver detalle incendio")
        print("2. Ver detalle recurso")
        opcion = int(input("-->"))
        if opcion == 1:
            print("El Incendio actual es")
            self.visualizar_incendio()
        if opcion == 2:
            print("El Recurso actual es")
            self.visualizar_recurso()

    def visualizar_recurso(self, archivo=None):
        columnarecurso = recursos.encontrar_indice("id:string")
        nombre = self.encontrar_indice("nombre:string")
        columnausuarios = super().encontrar_indice("recurso_id:string")
        filausuarios = (self.buscafilas(self.nombre, nombre))
        for item in recursos.lista:
            if item[columnarecurso] == self.lista[filausuarios][columnausuarios]:
                aux = []
                aux.append(recursos.lista[0])
                aux.append(item)
                fx.printer(aux)
    def visualizar_incendio(self):
        try:
            if recursos.lista[int(self.id)+1][11]=="":
                    print("No se ha asignado incendio a este recurso")
                    print()
                    print()
            else:
                a=recursos.lista[int(self.id)+1][11]
                b=incendios.lista[int(a)+1]
                aux=[]
                aux.append(incendios.lista[0])
                aux.append(b)
                fx.printer(aux)
                print()
                print()
                print()

        except:
            print("No se ha asignado incendio a este recurso")
            print()
            print()


class ANAF(Persona):
    def __init__(self, name, passw):
        super().__init__(name, passw)
        nuevostring = ""

    def recursos_mas_usados(self):
            aux = sorted(recursos.lista[1:], key=lambda x: (int(x[12])), reverse=True)
            fx.printer(aux)

    def incendi_apagados(self):
        a=open("incendios apagados.txt",)
        for linea in a:
            print(linea)
        a.close()


    def edit(self, file, nombre ):
        nuevostring = ""
        for item in file.lista[0]:
            if item =="id:string":
                nuevodato = int(file.lista[len(file.lista)-1][file.encontrar_indice("id:string")])+1
                nuevodato =str(nuevodato) + ","
                nuevostring += nuevodato
            else:
                print(item + "\n")
                nuevodato = input("Agregue dato")
                nuevodato += ","
                nuevostring += nuevodato


        print("Dese guardar estos datos?")
        print("1. Si")
        print("2. No \n")
        opcion = input("-->")
        if opcion == "1":
            guardar = open(nombre, "a")
            guardar.write(nuevostring[0:(len(nuevostring) - 1)] + "\n")
            guardar.close()
        else:
            pass


usuarios = BaseDatos("usuarios.csv")
meteorologia = BaseDatos("meteorologia.csv")
recursos = BaseDatos("recursos.csv")
incendios = BaseDatos("incendios.csv")
