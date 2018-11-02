import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
import sys

if __name__ == "__main__":
    print("Bienvenido a Avanzacion Programada")
    print()
    print()
    print("Que desea simular?")
    print()
    print("1. Simulacion con parametros por defecto")
    print("2. Simulacion multiple con parametros varios")
    opcion = input("-->")

    if opcion == "1":
        import Ramo

        ramo = Ramo.Ramo()
        ramo.run()
        print()

        aux = [i[1] if isinstance(i, tuple) else i for i in ramo.promedio_controles]
        lenaux = len(aux) - 1
        aux2 = aux + [aux[lenaux] for i in range(lenaux, 14)]

        x = np.arange(15)
        plt.plot(x, ramo.promedio_actividades + [ramo.promedio_actividades[11] for i in range(11, 14)])
        plt.plot(x, ramo.promedio_tareas + [ramo.promedio_tareas[11] for i in range(11, 14)])
        plt.plot(x, aux2)
        plt.plot(x, [0 for i in range(0, 14)] + [ramo.promedio_examen])
        plt.legend(['Promedio Actividades', 'Promedio Tareas', 'Promedio Controles', "Promedio Examen"], loc='best')
        plt.suptitle("Notas Promedio por Semana")
        plt.xlabel("Semanas")
        plt.ylabel("Notas")
        plt.xlim(0, 14)
        plt.ylim(0, 7)
        plt.show()
        exit = False
        print("Tiempo de estadisticas!")
        while not exit:
            print("Que deseas hacer?")
            print("1. Consultar cualidades alumno")
            print("2. Consultar notas alumno")
            print("3. Salir")
            opcion = input("-->")
            if opcion == "1":
                print("Que alumno desea Consultar?")
                print()
                opcion = input("-->")
                try:
                    name = [alumno for alumno in ramo.lista_alumnos if alumno.name == opcion]
                    print("Nivel de programacion: {}".format(name[0].nivel))
                    print("Confianza: {}".format(name[0].confianza))
                    print("Manejo contenido")
                    for item in ramo.lista_contenidos:
                        print("{} : {}".format(item, name[0].manejo_contenidos[item]))
                except IndexError:
                    print()
                    print("Alumno no encontrado, recuerde usar tildes")

            if opcion == "3":
                exit = True

            if opcion == "2":
                print("Que alumno desea Consultar?")
                print()
                opcion = input("-->")
                try:
                    name = [alumno for alumno in ramo.lista_alumnos if alumno.name == opcion]
                    print("Promedio Final: {}".format(name[0].promedio))
                    print()
                    print("Notas Actividades")
                    for item in ramo.lista_contenidos:
                        print("Actividad {}: {}".format(item, name[0].notas_actividad[item][1]))
                    print()
                    print("Notas Tareas")
                    for item in range(1, 7):
                        print("Tarea {}: {}".format(item, name[0].notas_tareas[item][1]))
                    print()
                    print("Notas Controles")
                    for item in ramo.contenido_controles:
                        print("Control {}: {}".format(item, name[0].notas_controles[item][1]))
                    print()
                except IndexError:
                    print()
                    print("Alumno no encontrado, recuerde usar tildes")

        tabla = [["Mes con mas aprobacion", "3"],
                 ["Cantidad de alumnos que botaron el ramo", len(ramo.alumnos_retirados)],
                 ["Confianza inicial promedio", ramo.confianza_inicial],
                 ["Confianza final promedio", ramo.confianza_final]]
        porcentaje = []
        for item in ramo.lista_contenidos:
            porcentaje.append(["Porcentaje aprobacion Actividad " + item, 100 * sum(
                [1 for alumno in ramo.lista_alumnos if alumno.notas_actividad[item][1] >= 4]) / (
                                   len(ramo.lista_alumnos))])
        for item in ramo.contenido_controles:
            porcentaje.append(["Porcentaje aprobacion Control " + item, 100 * sum(
                [1 for alumno in ramo.lista_alumnos if alumno.notas_controles[item][1] >= 4]) / (
                                   len(ramo.lista_alumnos))])
        for item in range(1, 7):
            porcentaje.append(["Porcentaje aprobacion Tarea " + str(item), 100 * sum(
                [1 for alumno in ramo.lista_alumnos if alumno.notas_tareas[item][1] >= 4]) / (
                                   len(ramo.lista_alumnos))])

        tabla = tabla + porcentaje
        print(tabulate(tabla))

    if opcion == "2":
        while True:
            print("Que tipo de simulacion deseas realizar?")
            print()
            print("1. Simular un escenario en particular")
            print("2. Simular todos los escenarios para optimizar porcentaje de aprobacion")
            opcion = input("-->")
            if opcion == "1":
                while True:
                    import parameters

                    try:
                        numero = int(input("Ingresa el numero de escenario a simular"))
                        keys = list(parameters.escenarios.keys())
                        for key in keys:
                            if parameters.escenarios[key][numero] != "-":
                                parameters.parametros[key] = float(parameters.escenarios[key][numero])
                        import Ramo

                        ramo = Ramo.Ramo()
                        ramo.run()
                        print()

                        aux = [i[1] if isinstance(i, tuple) else i for i in ramo.promedio_controles]
                        lenaux = len(aux) - 1
                        aux2 = aux + [aux[lenaux] for i in range(lenaux, 14)]

                        x = np.arange(15)
                        plt.plot(x, ramo.promedio_actividades + [ramo.promedio_actividades[11] for i in range(11, 14)])
                        plt.plot(x, ramo.promedio_tareas + [ramo.promedio_tareas[11] for i in range(11, 14)])
                        plt.plot(x, aux2)
                        plt.plot(x, [0 for i in range(0, 14)] + [ramo.promedio_examen])
                        plt.legend(['Promedio Actividades', 'Promedio Tareas', 'Promedio Controles', "Promedio Examen"],
                                   loc='best')
                        plt.suptitle("Notas Promedio por Semana")
                        plt.xlabel("Semanas")
                        plt.ylabel("Notas")
                        plt.xlim(0, 14)
                        plt.ylim(0, 7)
                        plt.show()
                        exit = False
                        print("Tiempo de estadisticas!")
                        while not exit:
                            print("Que deseas hacer?")
                            print("1. Consultar cualidades alumno")
                            print("2. Consultar notas alumno")
                            print("3. Salir")
                            opcion = input("-->")
                            if opcion == "1":
                                print("Que alumno desea Consultar?")
                                print()
                                opcion = input("-->")
                                try:
                                    name = [alumno for alumno in ramo.lista_alumnos if alumno.name == opcion]
                                    print("Nivel de programacion: {}".format(name[0].nivel))
                                    print("Confianza: {}".format(name[0].confianza))
                                    print("Manejo contenido")
                                    for item in ramo.lista_contenidos:
                                        print("{} : {}".format(item, name[0].manejo_contenidos[item]))
                                except IndexError:
                                    print()
                                    print("Alumno no encontrado, recuerde usar tildes")

                            if opcion == "3":
                                tabla = [["Cantidad de alumnos que botaron el ramo", len(ramo.alumnos_retirados)],
                                         ["Confianza inicial promedio", ramo.confianza_inicial],
                                         ["Confianza final promedio", ramo.confianza_final]]
                                porcentaje = []
                                for item in ramo.lista_contenidos:
                                    porcentaje.append(["Porcentaje aprobacion Actividad " + item, 100 * sum(
                                        [1 for alumno in ramo.lista_alumnos if
                                         alumno.notas_actividad[item][1] >= 4]) / (
                                                           len(ramo.lista_alumnos))])
                                for item in ramo.contenido_controles:
                                    porcentaje.append(["Porcentaje aprobacion Control " + item, 100 * sum(
                                        [1 for alumno in ramo.lista_alumnos if
                                         alumno.notas_controles[item][1] >= 4]) / (
                                                           len(ramo.lista_alumnos))])
                                for item in range(1, 7):
                                    porcentaje.append(["Porcentaje aprobacion Tarea " + str(item), 100 * sum(
                                        [1 for alumno in ramo.lista_alumnos if alumno.notas_tareas[item][1] >= 4]) / (
                                                           len(ramo.lista_alumnos))])

                                tabla = tabla + porcentaje
                                print(tabulate(tabla))
                                exit = sys.exit()

                            if opcion == "2":
                                print("Que alumno desea Consultar?")
                                print()
                                opcion = input("-->")
                                try:
                                    name = [alumno for alumno in ramo.lista_alumnos if alumno.name == opcion]
                                    print("Promedio Final: {}".format(name[0].promedio))
                                    print()
                                    print("Notas Actividades")
                                    for item in ramo.lista_contenidos:
                                        print("Actividad {}: {}".format(item, name[0].notas_actividad[item][1]))
                                    print()
                                    print("Notas Tareas")
                                    for item in range(1, 7):
                                        print("Tarea {}: {}".format(item, name[0].notas_tareas[item][1]))
                                    print()
                                    print("Notas Controles")
                                    for item in ramo.contenido_controles:
                                        print("Control {}: {}".format(item, name[0].notas_controles[item][1]))
                                    print()
                                except IndexError:
                                    print()
                                    print(
                                        "Alumno no encontrado, esto puede ser debido a que alumno retiro curso o por error de tipeo, recuerde usar tildes")

                        tabla = [["Mes con mas aprobacion", "3"],
                                 ["Cantidad de alumnos que botaron el ramo", len(ramo.alumnos_retirados)],
                                 ["Confianza inicial promedio", ramo.confianza_inicial],
                                 ["Confianza final promedio", ramo.confianza_final]]
                        porcentaje = []
                        for item in ramo.lista_contenidos:
                            porcentaje.append(["Porcentaje aprobacion Actividad " + item, 100 * sum(
                                [1 for alumno in ramo.lista_alumnos if alumno.notas_actividad[item][1] >= 4]) / (
                                                   len(ramo.lista_alumnos))])
                        for item in ramo.contenido_controles:
                            porcentaje.append(["Porcentaje aprobacion Control " + item, 100 * sum(
                                [1 for alumno in ramo.lista_alumnos if alumno.notas_controles[item][1] >= 4]) / (
                                                   len(ramo.lista_alumnos))])
                        for item in range(1, 7):
                            porcentaje.append(["Porcentaje aprobacion Tarea " + str(item), 100 * sum(
                                [1 for alumno in ramo.lista_alumnos if alumno.notas_tareas[item][1] >= 4]) / (
                                                   len(ramo.lista_alumnos))])

                        tabla = tabla + porcentaje
                        print(tabulate(tabla))
                    except ValueError:
                        print("Valor ingresado incorrecto")

            if opcion == "2":
                import parameters

                lista_simulaciones = []
                keys = list(parameters.escenarios.keys())
                for i in range(0, len(parameters.escenarios["prob_40_creditos"])):
                    for key in keys:
                        if parameters.escenarios[key][i] != "-":
                            parameters.parametros[key] = float(parameters.escenarios[key][i])
                    import Ramo

                    ramo = Ramo.Ramo()
                    ramo.run()
                    lista_simulaciones.append(("Escenario " + str(i), ramo.porcentaje_aprobacion))
                orden = sorted(lista_simulaciones, key=lambda x: x[1], reverse=True)
                print("\n" * 10)
                print("El escenario con mayor porcentaje de aprobacion fue el {}".format(orden[0][0]))
                sys.exit()

    else:
        pass
