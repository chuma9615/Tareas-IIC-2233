encoding="utf-8"

import Bases as bs
import Funciones as fx
import os

path2 = os.getcwd() + "/Reportes Estrategias de Extincion"  #Creador de carpeta
if not os.path.exists(path2):
    os.mkdir("Reportes Estrategias de Extincion")

print("Bienvenido al SuperLuchin!, Ingrese usuario y contraseña \n")

usuarios = bs.BaseDatos("usuarios.csv")
meteorologia = bs.BaseDatos("meteorologia.csv")
recursos = bs.BaseDatos("recursos.csv")
incendios = bs.BaseDatos("incendios.csv")


a = False
b = False


while True:
    if a is False or b is False:
        while a is False or b is False:


            usuario = input("Usuario->")
            password = input("Password-->")
            fecha = fx.fecha()

            if usuarios.search(usuario, "nombre:string") is False:
                a = False
                print("Usuario incorrecto")

            if usuarios.search(password, "contraseña:string") is False:
                b = False
                print("Clave incorrecta")
            else:
                a = True
                b = True
    if usuarios.es_anaf() is True:
        anaf = bs.ANAF(usuario,password)
        print("Que desea hacer? \n")
        print("1. Escribir nuevos datos")
        print("2. Consultar datos")
        print("3. Desplegar incendios activos")
        print("4. Estrategia de extincion")
        print("5. Cerrar sesion")
        print("6. Cambiar Fecha")
        print("7. Desplegar incendios apagados")
        print("8. Mostrar recursos mas utilizados")
        opcion = input("-->")
        if opcion=="5":
            a=False
            b=False
        elif opcion=="7":
            try:
                anaf.incendi_apagados()
            except:
                print("No se han apagado incendios aun")
        elif opcion=="8":
            try:
                anaf.recursos_mas_usados()
            except:
                print("No se han apagado incendios aun")

        elif opcion=="6":
            fecha = fx.fecha()

        elif opcion == "1":
            print("En que base de datos desea agregar datos?\n")
            print("1. Usuarios")
            print("2. Meteorologia")
            print("3. Incendios")
            tipobase = input("-->")
            if tipobase == "1":
                anaf.edit(usuarios,"usuarios.csv")
            elif tipobase == "2":
                anaf.edit(meteorologia,"meteorologia.csv")
            elif tipobase == "3":
                anaf.edit(incendios,"incendios.csv")
            else:
                print("Opcion no valida")

        elif opcion == "2":
            print("Que datos desea consultar?\n")
            print("1. Usuarios")
            print("2. Recursos")
            print("3. Incendios")
            consulta = input("-->")
            if consulta == "1":
                print(usuarios,)
            elif consulta == "2":
                print(recursos)
            elif consulta == "3":
                print(incendios)
            else:
                print("Opcion no valida")

        elif opcion == "3":
            for r in range(1, len(incendios.lista) - 1):
                aux = bs.Incendio(r)
                if aux.puntos_poder != 0:
                    print(aux)



        elif opcion == "4":
            print()
            ide=""
            while ide=="":
                try:
                    print("ingrese id del incendio")
                    ide = int(input("-->"))
                except:
                    print("id no valida")
            print()
            print("que tipo de estrategia de extincion desea utilizar? \n")
            print("1. Cantidad de recursos")
            print("2. Tiempo de extincion")
            print("3. Costo economico")
            opcion = int(input("-->"))
            if opcion == 1:
                incendio_actual = bs.Incendio(ide)
                incendio_actual.simular(fecha,1)
            elif opcion == 2:
                incendio_actual = bs.Incendio(ide)
                incendio_actual.simular(fecha,2)
            elif opcion == 3:
                incendio_actual = bs.Incendio(ide)
                incendio_actual.simular(fecha,3)
            else:
                print("Opcion no valida")
        else:
            print("Opcion no valida")

    if usuarios.es_anaf() is not True:
        persona = bs.Plebe(usuario, password)
        persona.visualizar_recurso()
        persona.menu()
