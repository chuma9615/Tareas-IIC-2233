#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv as csv
import numpy as np
from student_class import Alumno
from helper_class import AyudanteDocencia, AyudanteTarea, Mavrakis
from teacher_class import Profesor
import parameters
import math
import random


class Ramo:
    def __init__(self):
        """ Clase donde se simularan los eventos y contiene a todos los actores"""
        self.time = 0
        self.acciones = {"ayudantia": self.ayudantia, }
        self.mas_plazo_tarea = False
        self.lista_contenidos = ["POO", "HERENCIA", "LISTAS_SET_DICT", "ARBOL", "FUNCIONAL", "METACLASS",
                                 "SIMULACION", "THREADING", "GUI", "SERIALIZACION", "NETWORKING",
                                 "WEBSERVICES"]
        self.lista_contenidos_tareas = ["POO", "HERENCIA", "LISTAS_SET_DICT", "ARBOL", "FUNCIONAL", "METACLASS",
                                        "SIMULACION", "THREADING", "GUI", "SERIALIZACION", "NETWORKING",
                                        "WEBSERVICES"]
        self.lista_eventos = [("reunion_ayudantes_catedra", 3), ("reunion_ayudantes_tarea", 1), ("aentregar_tarea", 6),
                              ("ayudar", 5 + 7), ("ayudantia", 4), ("ayudantia", 4 + 7),
                              ("ayudantia", 4 + (7 * 2)),
                              ("ayudantia", 4 + (7 * 3)), ("ayudantia", 4 + (7 * 4)), ("ayudantia", 4 + (7 * 5)),
                              ("ayudantia", 4 + (7 * 6)), ("ayudantia", 4 + (7 * 7)), ("ayudantia", 4 + (7 * 8)),
                              ("ayudantia", 4 + (7 * 9)), ("ayudantia", 4 + (7 * 10)), ("ayudantia", 4 + (7 * 11)),
                              ("catedra", 6), ("catedra", 6 + 7), ("catedra", 6 + (7 * 2)),
                              ("catedra", 6 + (7 * 3)), ("catedra", 6 + (7 * 4)), ("catedra", 6 + (7 * 5)),
                              ("catedra", 6 + (7 * 6)), ("catedra", 6 + (7 * 7)), ("catedra", 6 + (7 * 8)),
                              ("catedra", 6 + (7 * 9)), ("catedra", 6 + (7 * 10)), ("catedra", 6 + (7 * 11))]
        self.lista_alumnos = []
        self.lista_ayudante_catedra = []
        self.lista_profesores = []
        self.lista_ayudante_tarea = []
        self.coordinacion = None
        self.tareas_realizadas = 0
        self.semanas_controles = []
        self.controles_realizados = 0
        self.contenido_controles = []
        self.alumnos_retirados = []
        self.promedio_actividades = []
        self.promedio_tareas = []
        self.promedio_controles = []
        self.promedio_examen = 0
        self.confianza_inicial = 0
        self.confianza_final = 0
        self.porcentaje_aprobacion = 0
        self.dificultad_tareas = []
        self.dificultad_actividades = {}

    def poblar(self):
        """ Metodo para poblar el sistema de simulacion"""
        self.lista_eventos = sorted(self.lista_eventos, key=lambda x: x[1])
        archivo = csv.reader(open('integrantes.csv', 'r'))
        next(archivo)
        for row in archivo:
            name, type, secc = row
            if 'Profesor' == type:
                self.lista_profesores.append(Profesor(name, secc))

            if type == "Docencia":
                self.lista_ayudante_catedra.append(AyudanteDocencia(name))

            if type == "Tareas":
                self.lista_ayudante_tarea.append(AyudanteTarea(name))

            if type == "Alumno":
                self.lista_alumnos.append(Alumno(name, secc))

            if type == "Coordinación":
                self.coordinacion = Mavrakis(name)
            for profesor in self.lista_profesores:
                profesor.alumnos = [alumno for alumno in self.lista_alumnos if alumno.seccion == profesor.seccion]
        self.confianza_inicial = np.mean([alumno.confianza for alumno in self.lista_alumnos])

    @property
    def materia_semana(self):
        """Property para saber los contenidos para act. , ayudantia y control"""
        return self.lista_contenidos[self.semana]

    @property
    def semana(self):
        """ Property para saber la semana actual"""
        return math.floor(self.time / 7)

    @property
    def tarea(self):
        """Property para saber de que semana es la tarea y sus contenidos"""
        return math.floor(self.semana / 2) + 1

    def reunion_ayudantes_tarea(self):
        """ Metodo para ver la dificultad de la tarea"""
        print("Los ayudantes de tarea se han reunido para acrodar la dificultad de la tarea")
        dif1 = parameters.parametros[self.lista_contenidos_tareas.pop(0)]
        dif2 = parameters.parametros[self.lista_contenidos_tareas.pop(0)]
        self.dificultad_tareas.append(7 + random.randint(1, 5) / ((dif1 + dif2) / 2))

    def reunion_ayudantes_catedra(self):
        """Metodo para realizar la reunion de los ayudantes de catedra, esto ocurre los lunes"""
        print("los ayudantes se han reunido para definir dificultad de actividad {}".format(self.materia_semana))
        self.dificultad_actividades[self.materia_semana] = 7 + random.randint(1, 5) / (
            parameters.parametros[self.materia_semana])
        if self.materia_semana != "WEBSERVICES":
            self.lista_eventos.append(("reunion_ayudantes_catedra", self.time + 7))

    def fiesta(self):
        """ Metodo para mandar de fiesta a los K"""
        print("FIESTA! Los alumnos han ido a fiesta")
        asistentes = np.random.choice(self.lista_alumnos, 50, False)
        for alumno in asistentes:
            alumno.fiesta = 0.15
            alumno.manejo_contenidos[self.materia_semana] -= 2 * (
                ((1 / parameters.parametros[self.materia_semana]) * ((alumno.horas * 0.3))) / 7)
        nuevafiesta = math.floor(random.expovariate(parameters.parametros["fiesta_mes"]))
        if self.time + nuevafiesta < 10 * 7:
            self.lista_eventos.append(("fiesta", self.time + nuevafiesta))

    def ayudar(self):
        """ Metodo para ejecutar las reuniones de los profesores"""
        print("Los profesores ha ayudado a los alumnos en su oficina en la semana")
        for profesor in self.lista_profesores:
            nomina = [alumno for alumno in profesor.alumnos if
                      alumno.promedio < 5.0 and alumno not in profesor.previous_week]
            if len(nomina) >= 10:
                nomina = np.random.choice(nomina, 10, False)
            profesor.ayudar(nomina)
        if self.semana < 11:
            self.lista_eventos.append(("ayudar", self.time + 7))

    def ayudantia(self):
        """ Metodo para simular una ayudantia, el curso se divide en 2 salas y se lleva a cabo la ayudantia"""
        for i in range(0, 5):
            for alumno in self.lista_alumnos:
                alumno.estudio_diario(self.materia_semana)
        print("Ha ocurrido la ayudantia en la semana {}".format(self.semana))
        ayudantes = np.random.choice(self.lista_ayudante_catedra, 2, False)
        contenido = self.materia_semana
        ayudante1 = ayudantes[0]
        ayudante2 = ayudantes[1]
        if contenido in ayudante1.area_dominio:
            for alumno in self.lista_alumnos[0:math.floor(len(self.lista_alumnos) / 2)]:
                alumno.manejo_contenidos[contenido] *= 1.1
        if contenido in ayudante2.area_dominio:
            for alumno in self.lista_alumnos[math.floor(len(self.lista_alumnos) / 2):]:
                alumno.manejo_contenidos[contenido] *= 1.1

    def catedra(self):
        """Metodo que simula la catedra primero actualizando las horas estudiadas y luego tomando controles y
        haciendo la actividad, finalmente se vuelven a calcular las horas disponibles para la semana """

        print("Paso Catedra de la semana {} ".format(self.semana))
        for i in range(0, 3):
            for alumno in self.lista_alumnos:
                alumno.estudio_diario(self.materia_semana)

        dificultad = self.dificultad_actividades[self.materia_semana]

        proba = random.random()
        if proba <= 0.5:
            if self.semana - 1 not in self.semanas_controles and self.controles_realizados < 5:
                self.semanas_controles.append(self.semana)
                self.controles_realizados += 1
                self.contenido_controles.append(self.materia_semana)
                for alumno in self.lista_alumnos:
                    alumno.entregar_control(self.materia_semana, dificultad)
                self.lista_eventos.append(("publicar_controles", self.time + 14, self.materia_semana))
        for alumno in self.lista_alumnos:
            alumno.entregar_actividad(self.materia_semana, dificultad)
        self.lista_eventos.append(("Publicar_Actividad", self.time + 14, self.materia_semana))

        for alumno in self.lista_alumnos:
            alumno.aumentar_nivel_programacion()
            alumno.simular_horas_estudio()

    def aentregar_tarea(self):
        """Metodo para simular la entrega de una tarea por parte de los alumnos, las tareas se entregan los dias
                jueves """
        print("Los alumnos han entregado las tareas {} en la semana {}".format(self.tarea, self.semana))
        for i in range(0, 3):
            for alumno in self.lista_alumnos:
                alumno.estudio_diario(self.materia_semana)
        for alumno in self.lista_alumnos:
            alumno.estudio_semanal_tarea(self.tarea)
        difi = self.dificultad_tareas.pop(0)
        for alumno in self.lista_alumnos:
            alumno.entregar_tarea(self.tarea, difi)
        if self.tarea == 6:
            self.lista_eventos.append(("Publicar tareas", self.time + 14, self.tarea))
        if self.tareas_realizadas <= 4:
            self.lista_eventos.append(("reunion_ayudantes_tarea", self.time))
            self.tareas_realizadas += 1
            self.lista_eventos.append(("aentregar_tarea", self.time + 14))
            self.lista_eventos.append(("Publicar tareas", self.time + 14, self.tarea))

    def examen(self):
        """ Este metodo rescata los contenido para los examenes y hace que los alumnos rindan el examen,
        primero calculando los pomedios de las notas y luego asignando las preguntas """
        notaspromedioactividad = {}
        for item in self.lista_contenidos:
            notaspromedioactividad[item] = [
                sum([alumno.notas_actividad[item][1] for alumno in self.lista_alumnos]) / len(self.lista_alumnos)]
        for item in self.contenido_controles:
            notaspromedioactividad[item].append(
                sum([alumno.notas_controles[item][1] for alumno in self.lista_alumnos]) / len(self.lista_alumnos))
        aux = [i for i in self.lista_contenidos]
        for tarea in range(1, 7):
            notaspromedioactividad[aux.pop(0)].append(
                sum([alumno.notas_tareas[tarea][1] for alumno in self.lista_alumnos]) / len(self.lista_alumnos))
            notaspromedioactividad[aux.pop(0)].append(
                sum([alumno.notas_tareas[tarea][1] for alumno in self.lista_alumnos]) / len(self.lista_alumnos))
        for item in self.lista_contenidos:
            notaspromedioactividad[item] = np.mean(notaspromedioactividad[item])
        preguntas = sorted(notaspromedioactividad.items(), key=lambda x: x[1])
        preguntas = [preguntas[i][0] for i in range(0, 6)] + [preguntas[i][0] for i in range(10, 12)]
        dificultad = 7 + random.randint(1, 5) / np.mean([parameters.parametros[i] for i in preguntas])
        print("Se va a rendir el examen en la semana {} , las preguntas a evaluar son".format(self.semana))
        contador = 1
        for i in preguntas:
            print("Pregunta {}, {}".format(contador, i))
            contador += 1
        for alumno in self.lista_alumnos:
            alumno.rendir_examen(preguntas, dificultad)

        self.promedio_examen = np.mean([alumno.examen for alumno in self.lista_alumnos])

    def botar_ramo(self):
        """Metodo que hace que los alumnos boten el ramo si cumplen las caracterisitcas"""
        for alumno in self.lista_alumnos:
            alumno.botar_ramo()
        self.alumnos_retirados = [alumno for alumno in self.lista_alumnos if alumno.botado]
        self.lista_alumnos = [alumno for alumno in self.lista_alumnos if not alumno.botado]

    def run(self):
        """ Metodo para simular el semestre de avanzacion programada"""
        self.poblar()
        fiesta_inicial = math.floor(random.expovariate(parameters.parametros["fiesta_mes"]))
        if fiesta_inicial < 10 * 7:
            self.lista_eventos.append(("fiesta", fiesta_inicial))
        while len(self.lista_eventos) != 0:
            self.lista_eventos = sorted(self.lista_eventos, key=lambda x: x[1])
            self.time = self.lista_eventos[0][1]
            accion = self.lista_eventos.pop(0)
            if accion[0] == "Publicar_Actividad":
                proba = random.random()
                if proba <= 0.1:
                    print("El dr Mavarakis ha atrasado la entrega de nota de actividad {}".format(accion[2]))
                    self.lista_eventos.append((accion[0], self.time + random.randint(2, 5), accion[2]))

                else:
                    if accion[2] == "ARBOL":
                        self.lista_eventos.append(("botar_ramo", self.time))
                    self.promedio_actividades.append(
                        round(np.mean([i.notas_actividad[accion[2]] for i in self.lista_alumnos]), 1))
                    print("Se han publicado las notas de las actividad {} con promedio {} ".format(accion[2], round(
                        np.mean([i.notas_actividad[accion[2]] for i in self.lista_alumnos]), 1)))
                    for alumno in self.lista_alumnos:
                        alumno.operar_confianza(accion[2], 1)
            if accion[0] == "publicar_controles":
                proba = random.random()
                if proba <= 0.1:
                    print("El dr Mavarakis ha atrasado la entrega de nota del contro {}".format(accion[2]))
                    self.lista_eventos.append((accion[0], self.time + random.randint(2, 5), accion[2]))
                else:
                    if len(self.promedio_controles) == 0:
                        self.promedio_controles = [0 for i in range(0, self.lista_contenidos.index(accion[2]))]
                    else:
                        a_generar = self.lista_contenidos.index(accion[2]) - \
                                    self.promedio_controles[len(self.promedio_controles) - 1][0]
                        lista = [self.promedio_controles[len(self.promedio_controles) - 1][1] for i in
                                 range(0, a_generar - 1)]
                        self.promedio_controles = self.promedio_controles + lista
                    self.promedio_controles.append((self.lista_contenidos.index(accion[2]),
                                                    round(
                                                        np.mean(
                                                            [i.notas_controles[accion[2]] for i in self.lista_alumnos]),
                                                        1)))
                    print("Se han publicado las notas del  control {} con promedio {}".format(accion[2], round(
                        np.mean([i.notas_controles[accion[2]] for i in self.lista_alumnos]), 1)))
                    for alumno in self.lista_alumnos:
                        alumno.operar_confianza(accion[2], 0, 0, 1)
            if accion[0] == "Publicar tareas":
                proba = random.random()
                if proba <= 0.1:
                    print("El dr Mavarakis ha atrasado la entrega de nota de la tarea {}".format(accion[2]))
                    self.lista_eventos.append((accion[0], self.time + random.randint(2, 5), accion[2]))
                else:
                    print("Se han public"
                          "ado las notas de la tarea {} con promedio {}".format(accion[2], round(
                        np.mean([i.notas_tareas[accion[2]] for i in self.lista_alumnos]), 1)))
                    self.promedio_tareas.append(
                        round(np.mean([i.notas_tareas[accion[2]] for i in self.lista_alumnos]), 1))
                    self.promedio_tareas.append(
                        round(np.mean([i.notas_tareas[accion[2]] for i in self.lista_alumnos]), 1))
                    for alumno in self.lista_alumnos:
                        alumno.operar_confianza(accion[2], 0, 1, 0)
            elif accion[0] != "publicar_controles" and accion[0] != "Publicar_Actividad":
                exe = getattr(self, accion[0])
                exe()

        for i in range(0, 5):
            for alumno in self.lista_alumnos:
                alumno.estudio_diario(random.choice(self.lista_contenidos))
        self.time += 5
        self.examen()
        self.confianza_final = np.mean([alumno.confianza for alumno in self.lista_alumnos])
        count = 0
        for alumno in self.lista_alumnos:
            if alumno.aprueba:
                count += 1
        self.porcentaje_aprobacion = count / (len(self.lista_alumnos) + len(self.alumnos_retirados))
