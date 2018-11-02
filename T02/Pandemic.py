import sys, os
import listaligada as li
import Infecciones_y_paises as inf
import connections_generator as generador

path2 = os.getcwd() + "/Partidas Guardadas"  #Creador de carpeta
if not os.path.exists(path2):
    os.mkdir("Partidas Guardadas")


print("Bienvenido a Pandemic, el juego diseñado para destruir a la humanidad")
print()
print("Que desea hacer?")
print("1. Jugar nueva partida")
print("2. Cargar partida")
opcion=input("-->")
if opcion == "1":
    generador.generate_connections()
    mundo = inf.Tablero()
    #print(mundo.paises[0].vecinos)
    #print(mundo.paises[0].aeropuertos)
    print("Elige tu infeccion predilecta para eliminar a la humanidad")
    print("1. Virus")
    print("2. Bacteria")
    print("3. Parasito")
    infeccion=(input("-->"))
    check=True
    opcione=li.ListaLigada("1","2","3")
    while check:
        if infeccion not in opcione:
            print("esa opcion no esta disponible")
            infeccion = (input("-->"))
        if infeccion in opcione:
            check=False
    mundo.infectar(infeccion)
if opcion =="2":
    check=True
    while check:
        try:
            name=input("Ingresa el nombre de la partida")
            origi=os.getcwd()
            os.chdir(os.getcwd()+ "/Partidas Guardadas/" +name)
            mundo=inf.Tablero()
            os.chdir(origi)
            mundo.cargar_tablero(name)
            check=False
        except FileNotFoundError:
            print("La partida ingresada no existe")

while True:
    print("Que deseas hacer?")
    print("1. Pasar de dia")
    print("2. Ver estadisticas")
    print("3. Guardar estado")
    print("4. Salir del juego")
    opcion=input("-->")
    if opcion == "3":
        mundo.guardar_tablero()
    if opcion == "4":
        sys.exit()
    if opcion == "1":
        mundo.simular()
        mundo.update()
    if opcion =="2":
        mundo.estadisticas()



