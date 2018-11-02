from abc import ABCMeta, abstractmethod
import listaligada as li
import csv
import os
import random,shutil,sys


class Infeccion(metaclass=ABCMeta):
    def __init__(self, contagiosidad, mortalidad, resistencia, visibilidad):
        self.contagiosidad = contagiosidad
        self.mortalidad = mortalidad
        self.resistencia = resistencia
        self.visibilidad = visibilidad


class Virus(Infeccion):
    def __init__(self):
        super().__init__(1.5, 1.2, 1.5, 0.5)
        self.nombre = "Virus"

    def __repr__(self):
        return self.nombre


class Bacteria(Infeccion):
    def __init__(self):
        super().__init__(1, 1, 0.5, 0.7)
        self.nombre = "Bacteria"

    def __repr__(self):
        return self.nombre


class Parasito(Infeccion):
    def __init__(self):
        super().__init__(0.5, 1.5, 1, 0.45)
        self.nombre = "Parasito"

    def __repr__(self):
        return self.nombre


class Pais:
    def __init__(self, nombre, aeropuerto=None, vecinos=None, poblacion=None, status="limpio"):
        self.nombre = nombre
        self.aeropuertos = li.ListaLigada()
        self.vecinos = li.ListaLigada()
        self.poblacion = poblacion
        self.status = status
        self.infectados = 0
        self.infectados_dia = 0
        self.sanos = self.poblacion
        self.muertos = 0
        self.muertos_dia = 0
        self.mascarillas = False
        self.infeccion = None
        self.aeropuerto_cerrado = False
        self.frontera_cerrada = False
        self.cura = False
        self.cura_descubierta = False
        self.proposiciones = li.ListaLigada()

    def __str__(self):
        return self.nombre

        '''print("{0} , {1} poblacion, codigo {2} \n".format(self.nombre, self.poblacion, id(self)))
        print("Sus vecinos son ")
        for item in self.vecinos:
            print("vecino {0}, id {1}".format(item.nombre,id(item)))
        print()
        print("Sus aeropuertos conectan con ")
        for a in self.aeropuertos:
            print("aeropuerto {0}, id {1} ".format(a.nombre,id(a)))
        print()
        print()

        return '' '''

    def updatecontador(self):
        self.infectados_dia = 0
        self.muertos_dia = 0

    def checkmuerto(self):
        if self.muertos >= self.poblacion:
            self.status = "muerto"
            #self.updatecontador()
            self.proposiciones=li.ListaLigada()
            print("{} ha muerto".format(self.nombre))

    def infectar(self, tablero, infeccion=None):
        self.updatecontador()
        if infeccion != None:
            self.infeccion = infeccion
        elif self.infectados > 0 and self.sanos > 0:
            a = random.randint(0, 6)
            if self.mascarillas:
                por_infectar = int(self.infectados * a * 0.3 * self.infeccion.contagiosidad)
                print("se van a infectar {0} en {1}".format(por_infectar,self.nombre))
                if self.sanos >= por_infectar:
                    self.infectados += por_infectar
                    self.sanos -= por_infectar
                elif self.sanos < por_infectar:
                    por_infectar = self.sanos
                    self.infectados += por_infectar
                    self.sanos = 0
                tablero.infecciones_dia += por_infectar
                self.infectados_dia += por_infectar

            elif not self.mascarillas:
                por_infectar = int(self.infectados * a * self.infeccion.contagiosidad)
                print("se van a infectar {0} en {1}".format(por_infectar, self.nombre))
                # self.infectados += int(self.infectados * a * self.infeccion.contagiosidad)
                if self.sanos >= por_infectar:
                    self.infectados += por_infectar
                    self.sanos -= por_infectar
                elif self.sanos < por_infectar:
                    por_infectar = self.sanos
                    self.infectados += por_infectar
                    self.sanos = 0
                tablero.infecciones_dia += por_infectar
                self.infectados_dia += por_infectar

            if not self.frontera_cerrada:
                if int(self.poblacion / 2) <= self.infectados or int(
                                self.poblacion / 4) <= self.muertos:  # condicion para sugerir cerrar Frontera
                    propo = self.emitir_proposicion(0.8, "Cerrar Frontera")
                    tablero.colaprioridades.append(propo)

            if not self.mascarillas:
                if int(self.poblacion / 3) < self.infectados:
                    propo = self.emitir_proposicion(0.5, "Entregar Mascarillas")
                    tablero.colaprioridades.append(propo)

            if self.aeropuerto_cerrado == False:
                if int(self.poblacion * 0.8) < self.infectados or int(
                                self.poblacion * 0.2) < self.muertos:  # condicion para sugerir cerrar aeropuertos
                    propo = self.emitir_proposicion(0.5, "Cerrar Aeropuertos")
                    tablero.colaprioridades.append(propo)

            if self.frontera_cerrada:
                if int(self.poblacion / 2) > self.infectados or int(
                                self.poblacion / 4) > self.muertos:  # condicion para sugerir abrir fronteras
                    propo = self.emitir_proposicion(0.7, "Abrir Frontera")
                    tablero.colaprioridades.append(propo)

            if self.aeropuerto_cerrado:
                if int(self.poblacion / 3) > self.infectados:
                    propo = self.emitir_proposicion(0.8,
                                                    "Abrir Aeropuertos")  # condicion para sugerir abrir aeropuertos
                    tablero.colaprioridades.append(propo)

            if self.cura_descubierta:
                propo = self.emitir_proposicion(1, "Abrir Aeropuertos y Fronteras")  # condicion para sugerir abrir todo
                tablero.colaprioridades.append(propo)

        if self.infectados == 0 and self.status == "limpio":
            self.infectados = 1
            self.infectados_dia += 1
            self.sanos -= 1
            print("se infecto 1 persona por primera vez")
            tablero.infecciones_dia += self.infectados
            tablero.infecciones += 1
            self.status = "infectado"

    def matar(self, tablero):
        if self.infectados > 0:
            azar = random.randint(0, 100)
            proba = min(max(0.2, ((tablero.dias ** 2) / 1000) * self.infeccion.mortalidad), 1)
            if azar <= proba * 100:
                a = int(self.infectados * proba)
                print("han muerto {0} en {1}".format((a), self.nombre))
                self.muertos += int(self.infectados * proba)
                tablero.muertes_dia += a
                self.infectados -= a
                self.muertos_dia += a
        self.checkmuerto()

    def emitir_proposicion(self, factor, encabezado):
        prioridad = (factor * self.infectados) / self.poblacion
        proposicion = li.ListaLigada()
        proposicion.append(self)
        proposicion.append(prioridad)
        proposicion.append(encabezado)
        proposicion.append(self.nombre)
        self.proposiciones.append(proposicion)
        return proposicion

    def infectar_vecinos(self, tablero):
        proba = (min(
            ((0.7 * self.infectados) / ((self.poblacion - self.muertos) * (len(self.aeropuertos) + len(self.vecinos)))),
            1))
        for pais in self.vecinos:
            if pais.status == "limpio":
                # proba = min(((0.07 * self.infectados) / ( (self.poblacion - self.muertos) *(len(
                # self.aeropuertos)+len(self.vecinos)) )),1)
                if self.frontera_cerrada:
                    return

                if not self.frontera_cerrada and not pais.frontera_cerrada:
                    guia = random.randint(0, 100)
                    # for pais in self.vecinos:
                    if guia <= proba * 100:
                        pais.infectar(tablero, self.infeccion)
                        tablero.paises_infectados_dia.append(pais.nombre)
                        #print(tablero.paises_infectados_dia)

        for pais in self.aeropuertos:
            if pais.status == "limpio":
                # proba = min(((0.07 * self.infectados) / ( (self.poblacion - self.muertos) *(len(
                # self.aeropuertos)+len(self.vecinos)) )),1)
                if self.aeropuerto_cerrado:
                    return

                if not self.aeropuerto_cerrado and not pais.aeropuerto_cerrado:
                    guia = random.randint(0, 100)
                    if guia <= proba * 100:
                        pais.infectar(tablero, self.infeccion)
                        tablero.paises_infectados_dia.append(pais.nombre)
                        #print(tablero.paises_infectados_dia)

    def curar(self):
        if self.cura:
            proba = 0.25 * self.infeccion.resistencia
            azar = random.randint(0, 100)
            if azar <= proba:
                por_curar = int(self.infectados * 0.25)
                self.infectados -= por_curar
                print("Se ha curado {} gente".format(por_curar))
                self.sanos += por_curar


class Tablero:
    def __init__(self):
        self.infeccion = None
        self.paises = li.ListaLigada()
        self.poblacion_inicial = 0
        self.colaprioridades = li.ListaLigada()
        self.poblar()
        self.poblar2()
        self.dias = 0
        self.poblacion_actual = self.poblacion_inicial
        self.paises_infectados_dia = li.ListaLigada()
        self.muertes_dia = 0
        self.infecciones_dia = 0
        self.aeropuertos_cerrados_dia = li.ListaLigada()
        self.fronteras_cerradas_dia = li.ListaLigada()
        self.mascaras_dia = li.ListaLigada()
        self.muertes = 0
        self.infecciones = 0
        self.buscar_cura = False
        self.avance_cura = 0
        self.cura_encontrada = False
        self.paises_infectados = li.ListaLigada()
        self.estadisticaspordia = li.ListaLigada("En el dia 0 se murieron 0 personas y se infectaron 1 personas")

        #print(self.poblacion_inicial)

    def update(self):
        if len(self.paises_infectados_dia) > 0:
            for item in self.paises_infectados_dia:
                self.paises_infectados.append(item)
        self.muertes += self.muertes_dia
        self.infecciones += self.infecciones_dia
        self.infecciones -= self.muertes_dia

    def guardar_tablero(self):
        name = input("nombre de partida")
        path2 = os.getcwd() + "/Partidas Guardadas/"+name  # Creador de carpeta
        if not os.path.exists(path2):
            os.mkdir("Partidas Guardadas/"+name)
        oripath = os.getcwd()
        path1 = os.getcwd()+"/random_airports.csv"
        path2 = os.getcwd() + "/Partidas Guardadas/"+name+"/random_airports.csv"
        os.rename(path1,path2)
        shutil.copyfile(oripath+"/borders.csv",oripath+"/Partidas Guardadas/"+name+"/borders.csv")
        shutil.copyfile(oripath + "/population.csv", oripath + "/Partidas Guardadas/" + name + "/population.csv")
        guardar = li.ListaLigada()
        guardar.append(self.infeccion)
        guardar.append(self.poblacion_inicial)
        guardar.append(self.dias)
        guardar.append(self.poblacion_actual)
        guardar.append(len(self.paises_infectados_dia))
        for pais in self.paises_infectados_dia:
                guardar.append(pais)
        guardar.append(self.muertes_dia)
        guardar.append(self.infecciones_dia)
        guardar.append(len(self.aeropuertos_cerrados_dia))
        for pais in self.aeropuertos_cerrados_dia:
            guardar.append(pais)
        guardar.append(len(self.fronteras_cerradas_dia))
        for pais in self.fronteras_cerradas_dia:
            guardar.append(pais)
        guardar.append(len(self.mascaras_dia))
        for pais in self.mascaras_dia:
            guardar.append(pais)
        guardar.append(self.muertes)
        guardar.append(self.infecciones)
        guardar.append(self.buscar_cura)
        guardar.append(self.avance_cura)
        guardar.append(self.cura_encontrada)
        guardar.append(len(self.paises_infectados))
        for pais in self.paises_infectados:
            guardar.append(pais)
        guardar.append(len(self.estadisticaspordia))
        for item in self.estadisticaspordia:
            guardar.append(item)
        #print(guardar)
        os.chdir(os.getcwd() +"/Partidas Guardadas/"+name)
        archivo=open(name+".txt","w")
        print(guardar , file =archivo)
        archivo.close()
        os.chdir(oripath)

        infopaises=li.ListaLigada()
        infopais=li.ListaLigada()
        for pais in self.paises:
            infopais.append(pais.nombre)
            infopais.append(pais.status)
            infopais.append(pais.infectados)
            infopais.append(pais.infectados_dia)
            infopais.append(pais.sanos)
            infopais.append(pais.muertos)
            infopais.append(pais.muertos_dia)
            infopais.append(pais.mascarillas)
            if pais.infeccion!=None:
                infopais.append(pais.infeccion.nombre)
            if pais.infeccion == None:
                infopais.append(pais.infeccion)
            infopais.append(pais.aeropuerto_cerrado)
            infopais.append(pais.frontera_cerrada)
            infopais.append(pais.cura)
            infopais.append(pais.cura_descubierta)
            #for i in pais.proposiciones:
            #    infopais.append(i)
            infopaises.append(infopais)
            infopais=li.ListaLigada()
        #print(infopais)
        os.chdir(os.getcwd() +"/Partidas Guardadas/"+name)
        archivo=open(name+"_paises.txt","w")
        for line in infopaises:
            print(line , file =archivo)
        archivo.close()
        os.chdir(oripath)

    def cargar_tablero(self,nombre):
        oripath=os.getcwd()
        os.chdir(os.getcwd() + "/Partidas Guardadas/"+nombre)
        archivo = open(nombre + ".txt", "r")
        lista=''
        for line in archivo:
            line=line.strip("[")
            line=line.strip("]")
            line=line.split(",")
            lista=li.ListaLigada(*line)
        #print(lista)
        if lista[0] == "Virus":
            self.infeccion=Virus()
        if lista[0] == "Bacteria":
            self.infeccion=Bacteria()
        if lista[0] == "Parasito":
            self.infeccion=Parasito()
        self.poblacion_inicial=int(lista[1])
        self.dias=int(lista[2])
        self.poblacion_actual=int(lista[3])
        aux=int(lista[4])
        num=5
        for i in range(5,5+aux):
            self.paises_infectados_dia.append(lista[i])
            num+=1
        self.muertes_dia=lista[num]
        self.infecciones_dia=lista[num+1]
        aux=int(lista[num+2])
        num=num+3
        for i in range(num,num+aux):
            self.aeropuertos_cerrados_dia.append(lista[i])
            num+=1
        aux=int(lista[num])
        num=num+1
        for i in range(num,num+aux):
            self.fronteras_cerradas_dia.append(lista[i])
            num+=1
        aux=int(lista[num])
        num=num+1
        for i in range(num,num+aux):
            self.mascaras_dia.append(lista[i])
            num+=1
        self.muertes=int(lista[num])
        self.infecciones=int(lista[num+1])
        if lista[num+2] == "False":
            self.buscar_cura = False
        if lista[num+2] == "True":
            self.buscar_cura = True
        self.avance_cura = float(lista[num+3])
        if lista[num+4] == "False":
            self.cura_encontrada = False
        if lista[num+4] == "True":
            self.cura_encontrada = True
        aux=int(lista[num+5])
        num=num+6
        for i in range(num,num+aux):
            self.paises_infectados.append(lista[i])
            num+=1
        num+=1
        for i in range(num,len(lista)):
            self.estadisticaspordia.append(lista[i])

        archivo = open(nombre + "_paises.txt", "r")
        lista=li.ListaLigada()
        for line in archivo:
            line=line.strip("[")
            line=line.strip("]")
            line=line.replace("'","")
            line=line.split(",")
            pais=li.ListaLigada(*line)
            lista.append(pais)
        #print(lista)
        for pais in self.paises:
            for linea in lista:
                #for item in linea:
                 #   print()
                if pais.nombre == linea[0]:
                    pais.status = linea[1][1:]
                    pais.infectados = int(linea[2])
                    pais.infectados_dia = int(linea[3])
                    pais.sanos = int(linea[4])
                    pais.muertos = int(linea[5])
                    pais.muertos_dia = int(linea[6])
                    if linea[7] == " False":
                        pais.mascarillas = False
                    if linea[7] == " True":
                        pais.mascarillas = True
                    #print("esta es la infeccion {}".format(linea[7]))
                    if linea[8] == " None":
                        pais.infeccion = None
                    elif linea[8] == " Virus":
                        pais.infeccion = Virus()
                    elif linea[8] == " Bacteria":
                        pais.infeccion = Bacteria()
                    elif linea[8] == " Parasito":
                        pais.infeccion = Parasito()
                    if linea[9] == " False":
                        pais.aeropuerto_cerrado = False
                    if linea[9] == " True":
                        pais.aeropuerto_cerrado = True
                    if linea[10] == " False":
                        pais.frontera_cerrada = False
                    if linea[10] == " True":
                        pais.frontera_cerrada = True
                    if linea[11] == " True":
                        pais.cura = True
                    if linea[11] == " False":
                        pais.cura = False
                    if linea[12] == " True":
                        pais.cura_descubierta = True
                    if linea[12] == " False":
                        pais.cura_descubierta = False
        os.chdir(oripath)

        '''for pais in self.paises:
            print("{0} , {1} poblacion, codigo {2} \n".format(pais.nombre, pais.poblacion, id(pais)))
            print("Sus vecinos son ")
            for item in pais.vecinos:
                print("vecino {0}, id {1}".format(item.nombre, id(item)))
            print()
            print("Sus aeropuertos conectan con ")
            for a in pais.aeropuertos:
                print("aeropuerto {0}, id {1} ".format(a.nombre, id(a)))
            print()
            print()
            print(pais.poblacion)
            print(pais.status)
            print(pais.infectados)
            print(pais.infectados_dia)
            print(pais.sanos)
            print(pais.muertos)
            print(pais.muertos_dia)
            print(pais.mascarillas)
            print(pais.infeccion)
            print(pais.aeropuerto_cerrado)
            print(pais.frontera_cerrada)
            print(pais.cura)
            print(pais.cura_descubierta)
            print()
        print(self.infeccion)
        print(self.poblacion_inicial)

        print(self.dias)# = 0
        print(self.poblacion_actual)
        print(self.paises_infectados_dia)
        print(self.muertes_dia)
        print(self.infecciones_dia) # = 0
        print(self.aeropuertos_cerrados_dia) # = li.ListaLigada()
        print(self.fronteras_cerradas_dia) # = li.ListaLigada()
        print(self.mascaras_dia) # = li.ListaLigada()
        print(self.muertes) # = 0
        print(self.infecciones) # = 0
        print(self.buscar_cura) # = False
        print(self.avance_cura) # = 0
        print(self.cura_encontrada) # = False
        print(self.paises_infectados)
        print(self.estadisticaspordia)'''

    def estadisticas(self):
        print("Que estadistica desea consultar")
        print("1. Resumen del dia")
        print("2. Resumen por pais")
        print("3. Estadistica Global")
        print("4. Muertes e infecciones diarias")
        print("5. Promedio muerte e infeccion")
        opcion = input("-->")
        if opcion == "5":
            print("La tasa de vida acumulada es {}".format((self.poblacion_inicial - self.muertes - self.infecciones)/self.poblacion_inicial))
            print()
            print("La tasa de muerte acumulada es {}".format(self.muertes/self.poblacion_inicial))
        if opcion == "4":
            for item in self.estadisticaspordia:
                print(item)
        if opcion == "3":
            print(
                "Hasta la fecha han muerto {0} personas, hay {1} personas infectadas, hay {2} personas vivas y {3} "
                "personas sanas".format(
                    self.muertes, self.infecciones, (self.poblacion_inicial - self.muertes),
                    (self.poblacion_inicial - self.muertes - self.infecciones)))
        if opcion == "2":
            pais = input("Ingrese pais  -->")
            pais=pais.title()
            for item in self.paises:
                if item.nombre == pais:
                    print(item.status)
                    print()
                    print("Hoy han muerto {0} personas y se han infectado {1} personas".format(item.muertos_dia,
                                                                                               item.infectados_dia))
                    print()
                    print("Las proposiciones de este dia fueron")
                    print()
                    for propo in item.proposiciones:
                        print("{0} con prioridad {1}".format(propo[2], propo[1]))
                    print()

        if opcion == "1":
            print("Hoy murieron {0} personas y se infectaron {1}".format(self.muertes_dia, self.infecciones_dia))
            if len(self.paises_infectados_dia) == 0:
                print("No se infectaron paises hoy")
                print()
            elif len(self.paises_infectados_dia) > 0:
                print("Hoy se infecto")
                for item in self.paises_infectados_dia:
                    print(item)
            if len(self.aeropuertos_cerrados_dia) == 0:
                print("No se cerraron aeropuertos hoy")
                print()

            elif len(self.aeropuertos_cerrados_dia) > 0:
                print("Hoy se cerraron los aeropuertos de")
                for item in self.aeropuertos_cerrados_dia:
                    print(item)

            if len(self.fronteras_cerradas_dia) == 0:
                print("No se cerraron fronteras hoy")
                print()

            elif len(self.fronteras_cerradas_dia) > 0:
                print("Hoy se cerraron las fronteras de")
                for item in self.fronteras_cerradas_dia:
                    print(item)

            if len(self.mascaras_dia) == 0:
                print("No se entregaron mascarillas hoy")
                print()

            elif len(self.mascaras_dia) > 0:
                print("Hoy se entregaron mascarillas en")
                for item in self.mascaras_dia:
                    print(item)

    def poblar(self):
        listaaux = li.ListaLigada()
        listacompilada = li.ListaLigada()
        l_conexion_pais = li.ListaLigada()
        listafronteras = li.ListaLigada()
        with open("population.csv", newline='') as f:  # Linea extraida de la libreria online de python
            reader = csv.reader(f)
            for row in reader:
                aux2 = li.ListaLigada(*row)
                listaaux.append(aux2)
            del listaaux[0]
        for item in listaaux:
            self.poblacion_inicial += int(item[1])
            pais = Pais(item[0], None, None, int(item[1]))
            self.paises.append(pais)
        listaaux = li.ListaLigada()
        with open("borders.csv", newline='') as g:
            reader = csv.reader(g)
            for row in reader:
                row = row[0].split(";")
                row = ",".join(row)
                row = row.split(",")

                aux2 = li.ListaLigada(*row)
                listaaux.append(aux2)
            ultimo = li.ListaLigada()
            ultimo.append(
                "neverland")  # Estas 3 lineas son para que mi algoritmo agarre el ultimo item de la lista bien
            listaaux.append(ultimo)
            del listaaux[0]
            actual = ''
            for item in listaaux:
                if actual == '':  # Para asi poder compilar las fronteras del primer pais de la lista
                    actual = item[0]
                    listacompilada.append(actual)
                    l_conexion_pais.append(item[1])
                elif actual != '':
                    if actual == item[0]:
                        l_conexion_pais.append(item[1])
                    if actual != item[0]:
                        listacompilada.append(l_conexion_pais)
                        listafronteras.append(listacompilada)
                        l_conexion_pais = li.ListaLigada()
                        listacompilada = li.ListaLigada()
                        actual = item[0]
                        listacompilada.append(actual)
                        l_conexion_pais.append(item[1])
        for pais in self.paises:
            for pais2 in listafronteras:
                if pais.nombre == pais2[0]:
                    # pais.vecinos = pais2[1]  Note to self: si es mejor operar con los vecinos como str, descomentar
                    #  esta loinea y borrar abajo
                    for paisfronterizo in pais2[1]:
                        for paistotal in self.paises:
                            if paisfronterizo == paistotal.nombre:
                                pais.vecinos.append(paistotal)
        with open("random_airports.csv", newline='') as f:  # Linea extraida de la libreria online de python
            listacompilada = li.ListaLigada()
            l_conexion_pais = li.ListaLigada()
            listaaux = li.ListaLigada()
            listafronteras = li.ListaLigada()
            reader = csv.reader(f)
            for row in reader:
                aux2 = li.ListaLigada(*row)
                listaaux.append(aux2)
            del (listaaux[0])
            ultimo = li.ListaLigada()
            ultimo.append(
                "neverland")  # Estas 3 lineas son para que mi algoritmo agarre el ultimo item de la lista bien
            listaaux.append(ultimo)
            actual = ''
            for item in listaaux:
                if actual == '':  # Para asi poder compilar las fronteras del primer pais de la lista
                    actual = item[0]
                    listacompilada.append(actual)
                    l_conexion_pais.append(item[1])
                elif actual != '':
                    if actual == item[0]:
                        l_conexion_pais.append(item[1])
                    if actual != item[0]:
                        listacompilada.append(l_conexion_pais)
                        listafronteras.append(listacompilada)
                        l_conexion_pais = li.ListaLigada()
                        listacompilada = li.ListaLigada()
                        actual = item[0]
                        listacompilada.append(actual)
                        l_conexion_pais.append(item[1])
        for pais in self.paises:
            for pais2 in listafronteras:
                if pais.nombre == pais2[0]:
                    # pais.vecinos = pais2[1]  Note to self: si es mejor operar con los vecinos como str, descomentar esta linea y borrar abajo
                    for paisfronterizo in pais2[1]:
                        for paistotal in self.paises:
                            if paisfronterizo == paistotal.nombre:
                                pais.aeropuertos.append(paistotal)

    def poblar2(self):
        listaaux = li.ListaLigada()
        listacompilada = li.ListaLigada()
        l_conexion_pais = li.ListaLigada()
        listafronteras = li.ListaLigada()
        with open("borders.csv", newline='') as g:
            reader = csv.reader(g)
            for row in reader:
                row = row[0].split(";")
                row = ",".join(row)
                row = row.split(",")

                aux2 = li.ListaLigada(*row)
                listaaux.append(aux2)
            ultimo = li.ListaLigada()
            ultimo.append(
                "neverland")  # Estas 3 lineas son para que mi algoritmo agarre el ultimo item de la lista bien
            listaaux.append(ultimo)
            del listaaux[0]
            actual = ''
            for item in listaaux:
                if actual == '':  # Para asi poder compilar las fronteras del primer pais de la lista
                    actual = item[1]
                    listacompilada.append(actual)
                    l_conexion_pais.append(item[0])
                elif actual != '':
                    if actual == item[1]:
                        l_conexion_pais.append(item[0])
                    if actual != item[1]:
                        listacompilada.append(l_conexion_pais)
                        listafronteras.append(listacompilada)
                        l_conexion_pais = li.ListaLigada()
                        listacompilada = li.ListaLigada()
                        actual = item[1]
                        listacompilada.append(actual)
                        l_conexion_pais.append(item[0])
        for pais in self.paises:
            for pais2 in listafronteras:
                if pais.nombre == pais2[0]:
                    # pais.vecinos = pais2[1]  Note to self: si es mejor operar con los vecinos como str, descomentar
                    #  esta loinea y borrar abajo
                    for paisfronterizo in pais2[1]:
                        for paistotal in self.paises:
                            if paisfronterizo == paistotal.nombre and paistotal not in pais.vecinos:
                                pais.vecinos.append(paistotal)
        with open("random_airports.csv", newline='') as f:  # Linea extraida de la libreria online de python
            listaaux = li.ListaLigada()
            l_conexion_pais = li.ListaLigada()
            listaaux = li.ListaLigada()
            listafronteras = li.ListaLigada()
            reader = csv.reader(f)
            for row in reader:
                aux2 = li.ListaLigada(*row)
                listaaux.append(aux2)
            del (listaaux[0])
            ultimo = li.ListaLigada()
            ultimo.append(
                "neverland")  # Estas 3 lineas son para que mi algoritmo agarre el ultimo item de la lista bien
            listaaux.append(ultimo)
            actual = ''
            for item in listaaux:
                if actual == '':  # Para asi poder compilar las fronteras del primer pais de la lista
                    actual = item[1]
                    listacompilada.append(actual)
                    l_conexion_pais.append(item[0])
                elif actual != '':
                    if actual == item[1]:
                        l_conexion_pais.append(item[0])
                    if actual != item[1]:
                        listacompilada.append(l_conexion_pais)
                        listafronteras.append(listacompilada)
                        l_conexion_pais = li.ListaLigada()
                        listacompilada = li.ListaLigada()
                        actual = item[1]
                        listacompilada.append(actual)
                        l_conexion_pais.append(item[0])
        for pais in self.paises:
            for pais2 in listafronteras:
                if pais.nombre == pais2[0]:
                    # pais.vecinos = pais2[1]  Note to self: si es mejor operar con los vecinos como str, descomentar esta linea y borrar abajo
                    for paisfronterizo in pais2[1]:
                        for paistotal in self.paises:
                            if paisfronterizo == paistotal.nombre and paistotal not in pais.aeropuertos:
                                pais.aeropuertos.append(paistotal)

    def simular(self):
        print("Estamos en el dia {}".format(self.dias))
        print()
        self.cura()
        #print("paises infectados")
        #print(self.paises_infectados)
        self.aeropuertos_cerrados_dia = li.ListaLigada()
        self.fronteras_cerradas_dia = li.ListaLigada()
        self.mascaras_dia = li.ListaLigada()
        self.colaprioridades = li.ListaLigada()
        self.paises_infectados_dia = li.ListaLigada()
        self.muertes_dia = 0
        self.infecciones_dia = 0
        #print("las muertes globales son {0}, las infecciones globales son {1}".format(self.muertes, self.infecciones))
        self.dias += 1
        for pais in self.paises:
            #print(pais.__dict__)
            if pais.status == "infectado" and pais.nombre not in self.paises_infectados_dia:
                pais.infectar(self)
                #print(
                    #"stats del pais {0} infectados, {1} muertos, {2} sanos y {3} de poblacion inicial, nombre {4}".format(
                     #   pais.infectados, pais.muertos, pais.sanos, (pais.infectados + pais.muertos + pais.sanos),
                      #  pais.nombre))
                pais.curar()
                pais.infectar_vecinos(self)
                pais.matar(self)
                #print(
                    #"stats del pais {0} infectados, {1} muertos, {2} sanos y {3} de poblacion inicial, nombre {4}".format(
                     #   pais.infectados, pais.muertos, pais.sanos, (pais.infectados + pais.muertos + pais.sanos),
                      #  pais.nombre))
        self.poblacion_actual -= self.muertes_dia
        self.priorizar()
        self.estadisticaspordia.append(
            "En el dia " + str(self.dias) + " se murieron " + str(self.muertes_dia) + " personas y se infectaron " + str(
                self.infecciones_dia) + " personas")
        self.check()
    def infectar(self, opcion=None):
        check=True
        opcion=int(opcion)
        while check:
            print("En que pais deseas comenzar la infeccion")
            name = input("-->")
            name=name.title()
            for pais in self.paises:
                if pais.nombre==name:
                    check=False
        for pais in self.paises:
            if pais.nombre == name:
                if opcion == 1:
                    infeccion = Virus()
                    pais.infeccion = infeccion
                    self.infeccion = infeccion
                    pais.infectar(self)
                if opcion == 2:
                    infeccion = Bacteria()
                    pais.infeccion = infeccion
                    self.infeccion = infeccion
                    pais.infectar(self)
                if opcion == 3:
                    infeccion = Parasito()
                    pais.infeccion = infeccion
                    self.infeccion = infeccion
                    pais.infectar(self)

    def priorizar(self):
        if len(self.colaprioridades) == 0:
            return

        a = self.colaprioridades
        c = sorted(a, key=lambda a: a[1], reverse=True)
        b = li.ListaLigada()
        for lista in c:
            aux2 = li.ListaLigada(*lista)
            b.append(aux2)
        #print(b)
        for i in range(0, 3):
            try:
                if b[i][2] == "Abrir Frontera":
                    print("se ha abierto la frontera de {}".format(b[i][0].nombre))
                    b[i][0].frontera_cerrada = False

                if b[i][2] == "Cerrar Frontera":
                    print("se ha cerrado la frontera de {}".format(b[i][0].nombre))
                    b[i][0].frontera_cerrada = True
                    self.fronteras_cerradas_dia.append(b[i][0].nombre)

                if b[i][2] == "Cerrar Aeropuertos":
                    print("se ha cerrado el aeropuerto de {}".format(b[i][0].nombre))
                    b[i][0].aeropuerto_cerrado = True
                    self.aeropuertos_cerrados_dia.append(b[i][0].nombre)

                if b[i][2] == "Abrir Aeropuertos":
                    print("se ha abierto el aeropuerto de {}".format(b[i][0].nombre))
                    b[i][0].aeropuerto_cerrado = False

                if b[i][2] == "Entregar Mascarillas":
                    b[i][0].mascarillas = True
                    self.mascaras_dia.append(b[i][0].nombre)

                if b[i][2] == "Abrir Aeropuertos y Fronteras":
                    print("se ha abierto todo de {}".format(b[i][0].nombre))
                    b[i][0].frontera_cerrada = False
                    b[i][0].aeropuerto_cerrado = False

            except IndexError:
                print()

    def cura(self):
        if not self.buscar_cura:
            proba = (self.infeccion.visibilidad * self.infecciones * (self.muertes)**2) / (self.poblacion_inicial)**3
            azar = random.randint(0, 100)
            #print("la proba es {0} y el azar es {1}".format(proba, azar))
            if proba * 100 >= azar:
                print("Se ha comenzado a trabajar en la cura")
                self.buscar_cura = True

        if self.buscar_cura:
            if self.avance_cura >= 1:
                if not self.cura_encontrada:
                    print("se ha encontrado la cura")
                    self.cura_encontrada = True
                    indice = random.randint(0, len(self.paises) - 1)
                    self.paises[indice].cura_descubierta = True
                    self.paises[indice].cura = True
                    print("la cura se inserto en {}".format(self.paises[indice]))
                    return
                if self.cura_encontrada:
                    paises_ya_curados = li.ListaLigada()  # esto es para ir guardando los paises vecinos que ya se curaron y no repetirlos
                    for pais in self.paises:
                        if pais.cura == True and pais not in paises_ya_curados:
                            for pa in pais.aeropuertos:
                                if not pa.aeropuerto_cerrado:
                                    pa.cura = True
                                    print("la cura se extendio a {0}".format(pa))
                                    paises_ya_curados.append(pa)

            elif self.avance_cura < 1:
                self.avance_cura += (self.poblacion_inicial - self.muertes - self.infecciones) / (
                    2 * self.poblacion_inicial)

    def check(self):
        sanos=self.poblacion_inicial - self.muertes - self.infecciones
        infecciones=0
        for pais in self.paises:
            infecciones+=pais.infectados
        if sanos ==0:
            print("Enhorabuena! has matado a toda la poblacion")
            sys.exit()

        if infecciones == 0 and sanos>0:
            print("Lo sentimos, has perdido")
            sys.exit()