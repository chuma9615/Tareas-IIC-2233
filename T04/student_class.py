import numpy as np
import random
import parameters


class Alumno:
    """ Esta clase modela a los objetos de tipo estudiante"""

    def __init__(self, name, seccion):
        """


        :param name: Nombre y apellido del alumno
        :param seccion: Numero de seccion a la que pertenece
        """
        self.consulta = 0
        self.name = name
        self.botado = False
        self.seccion = seccion
        self.lista_contenidos = ["POO", "HERENCIA", "LISTAS_SET_DICT", "ARBOL", "FUNCIONAL", "METACLASS",
                                 "SIMULACION", "THREADING", "GUI", "SERIALIZACION", "NETWORKING",
                                 "WEBSERVICES"]
        self.lista_contenidos_tareas = ["POO", "HERENCIA", "LISTAS_SET_DICT", "ARBOL", "FUNCIONAL", "METACLASS",
                                        "SIMULACION", "THREADING", "GUI", "SERIALIZACION", "NETWORKING",
                                        "WEBSERVICES"]
        self.creditos = (np.random.choice((40, 50, 55, 60), 1, True, (
            parameters.parametros["prob_40_creditos"], parameters.parametros["prob_50_creditos"],
            parameters.parametros["prob_55_creditos"],
            parameters.parametros["prob_60_creditos"])))[0]
        self.horas = random.randint(parameters.rango_horas[int(self.creditos)][0],
                                    parameters.rango_horas[int(self.creditos)][1])
        self.personalidad = random.choice(("Eficiente", "Artistico", "Teorico"))
        self.confianza = random.uniform(parameters.parametros["nivel_inicial_confianza_inferior"],
                                        parameters.parametros["nivel_inicial_confianza_superior"])
        self.notas_actividad = {"POO": [], "HERENCIA": [], "LISTAS_SET_DICT": [], "ARBOL": [], "FUNCIONAL": [],
                                "METACLASS": [],
                                "SIMULACION": [], "THREADING": [], "GUI": [], "SERIALIZACION": [], "NETWORKING": [],
                                "WEBSERVICES": []}  # Nota esperada y nota obtenida corresponden a los items de la
        # lista dentro del diccionario
        self.notas_tareas = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        self.habilidad = {}
        self.escuchar_tip = None
        self.manejo_contenidos = {"POO": 0, "HERENCIA": 0, "LISTAS_SET_DICT": 0, "ARBOL": 0, "FUNCIONAL": 0,
                                  "METACLASS": 0,
                                  "SIMULACION": 0, "THREADING": 0, "GUI": 0, "SERIALIZACION": 0, "NETWORKING": 0,
                                  "WEBSERVICES": 0}
        self.horas_tarea = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self.nivel = random.uniform(2, 10)
        self.notas_controles = {}
        self.examen = 0
        self.fiesta = 0

    @property
    def promedio(self):
        """ Property para calcular promedio, si las tareas estan vacias se reemplazan con un 4"""
        if len(self.notas_tareas[1]) == 0 or len(self.notas_controles) == 0:
            return 0.3 * np.mean([self.notas_actividad[i][1] for i in self.lista_contenidos if
                                  len(self.notas_actividad[i]) != 0]) + 0.3 * 4 + 0.3 * self.examen + 0.1 * 4
        return 0.3 * np.mean([self.notas_actividad[i][1] for i in self.lista_contenidos if
                              len(self.notas_actividad[i]) != 0]) + 0.3 * np.mean(
            [self.notas_tareas[i][1] for i in range(1, 7) if
             len(self.notas_tareas[i]) != 0]) + 0.3 * self.examen + 0.1 * np.mean(
            [nota[1] for nota in self.notas_controles.values()])

    @property
    def aprueba(self):
        if self.promedio >= 3.95:
            return True
        else:
            return False

    def simular_horas_estudio(self):
        """Metodo que asigna horas que va a estudiar un alumno por semana"""
        self.horas = random.randint(parameters.rango_horas[int(self.creditos)][0],
                                    parameters.rango_horas[int(self.creditos)][1])

    def escuchar_tip(self):
        """Metodo para definir si el alumno escucha el tip que da un profesor en clase"""
        proba = random.random()
        if proba <= 50:
            self.escuchar_tip = True

    def nota_esperada(self, actividad):
        """
        Metodo para calcular la nota esperada por el alumno en cada evaluacion

        :param actividad: string
        :return: float
        """

        if actividad == "POO":
            if 0 <= (self.horas * 0.3) <= 2:
                self.notas_actividad[actividad].append(round(random.uniform(1.1, 3.9), 1))
            elif 2 < (self.horas * 0.3) <= 4:
                self.notas_actividad[actividad].append(round(random.uniform(4, 5.9), 1))
            elif 4 < (self.horas * 0.3) <= 6:
                self.notas_actividad[actividad].append(round(random.uniform(6, 6.9), 1))
            elif 6 < (self.horas * 0.3):
                self.notas_actividad[actividad].append(7)
        if actividad == "LISTAS_SET_DICT" or actividad == "GUI":

            if 0 <= (self.horas * 0.3) <= 1:
                self.notas_actividad[actividad].append(round(random.uniform(1.1, 3.9), 1))
            elif 1 < (self.horas * 0.3) <= 4:
                self.notas_actividad[actividad].append(round(random.uniform(4, 5.9), 1))
            elif 4 < (self.horas * 0.3) <= 6:
                self.notas_actividad[actividad].append(round(random.uniform(6, 6.9), 1))
            elif 6 < (self.horas * 0.3):
                self.notas_actividad[actividad].append(7)
        if actividad == "HERENCIA":

            if 0 <= (self.horas * 0.3) <= 3:
                self.notas_actividad[actividad].append(round(random.uniform(1.1, 3.9), 1))
            elif 3 < (self.horas * 0.3) <= 6:
                self.notas_actividad[actividad].append(round(random.uniform(4, 5.9), 1))
            elif 6 < (self.horas * 0.3) <= 7:
                self.notas_actividad[actividad].append(round(random.uniform(6, 6.9), 1))
            elif 7 < (self.horas * 0.3):
                self.notas_actividad[actividad].append(7)

        if actividad == "ARBOL" or actividad == "THREADING" or actividad == "NETWORKING":
            if 0 <= (self.horas * 0.3) <= 2:
                self.notas_actividad[actividad].append(round(random.uniform(1.1, 3.9), 1))
            elif 2 < (self.horas * 0.3) <= 5:
                self.notas_actividad[actividad].append(round(random.uniform(4, 5.9), 1))
            elif 5 < (self.horas * 0.3) <= 7:
                self.notas_actividad[actividad].append(round(random.uniform(6, 6.9), 1))
            elif 7 < (self.horas * 0.3):
                self.notas_actividad[actividad].append(7)

        if actividad == "METACLASS" or actividad == "SERIALIZACION":

            if 0 <= (self.horas * 0.3) <= 4:
                self.notas_actividad[actividad].append(round(random.uniform(1.1, 3.9), 1))
            elif 4 < (self.horas * 0.3) <= 7:
                self.notas_actividad[actividad].append(round(random.uniform(4, 5.9), 1))
            elif 7 < (self.horas * 0.3) <= 9:
                self.notas_actividad[actividad].append(round(random.uniform(6, 6.9), 1))
            elif 9 < (self.horas * 0.3):
                self.notas_actividad[actividad].append(7)

        if actividad == "FUNCIONAL":
            if 0 <= (self.horas * 0.3) <= 3:
                self.notas_actividad[actividad].append(round(random.uniform(1.1, 3.9), 1))
            elif 3 < (self.horas * 0.3) <= 7:
                self.notas_actividad[actividad].append(round(random.uniform(4, 5.9), 1))
            elif 7 < (self.horas * 0.3) <= 8:
                self.notas_actividad[actividad].append(round(random.uniform(6, 6.9), 1))
            elif 8 < (self.horas * 0.3):
                self.notas_actividad[actividad].append(7)

        if actividad == "SIMULACION":
            if 0 <= (self.horas * 0.3) <= 3:
                self.notas_actividad[actividad].append(round(random.uniform(1.1, 3.9), 1))
            elif 3 < (self.horas * 0.3) <= 6:
                self.notas_actividad[actividad].append(round(random.uniform(4, 5.9), 1))
            elif 6 < (self.horas * 0.3) <= 8:
                self.notas_actividad[actividad].append(round(random.uniform(6, 6.9), 1))
            elif 8 < (self.horas * 0.3):
                self.notas_actividad[actividad].append(7)

        if actividad == "WEBSERVICES":
            if 0 <= (self.horas * 0.3) <= 2:
                self.notas_actividad[actividad].append(round(random.uniform(1.1, 3.9), 1))
            elif 2 < (self.horas * 0.3) <= 7:
                self.notas_actividad[actividad].append(round(random.uniform(4, 5.9), 1))
            elif 7 < (self.horas * 0.3) <= 8:
                self.notas_actividad[actividad].append(round(random.uniform(6, 6.9), 1))
            elif 8 < (self.horas * 0.3):
                self.notas_actividad[actividad].append(7)

    def nota_esperada_tarea(self, actividad):
        """
        Metodo para calcular la nota esperada por el alumno en cada tarea

        :param actividad: string
        :return: float
        """

        if actividad == "POO":
            if 0 <= (self.horas * 0.3) <= 2:
                return round(random.uniform(1.1, 3.9), 1)
            elif 2 < (self.horas * 0.3) <= 4:
                return round(random.uniform(4, 5.9), 1)
            elif 4 < (self.horas * 0.3) <= 6:
                return round(random.uniform(6, 6.9), 1)
            elif 6 < (self.horas * 0.3):
                return 7
        if actividad == "LISTAS_SET_DICT" or actividad == "GUI":

            if 0 <= (self.horas * 0.3) <= 1:
                return round(random.uniform(1.1, 3.9), 1)
            elif 1 < (self.horas * 0.3) <= 4:
                return round(random.uniform(4, 5.9), 1)
            elif 4 < (self.horas * 0.3) <= 6:
                return round(random.uniform(6, 6.9), 1)
            elif 6 < (self.horas * 0.3):
                return 7
        if actividad == "HERENCIA":

            if 0 <= (self.horas * 0.3) <= 3:
                return round(random.uniform(1.1, 3.9), 1)
            elif 3 < (self.horas * 0.3) <= 6:
                return round(random.uniform(4, 5.9), 1)
            elif 6 < (self.horas * 0.3) <= 7:
                return round(random.uniform(6, 6.9), 1)
            elif 7 < (self.horas * 0.3):
                return 7

        if actividad == "ARBOL" or actividad == "THREADING" or actividad == "NETWORKING":
            if 0 <= (self.horas * 0.3) <= 2:
                return round(random.uniform(1.1, 3.9), 1)
            elif 2 < (self.horas * 0.3) <= 5:
                return round(random.uniform(4, 5.9), 1)
            elif 5 < (self.horas * 0.3) <= 7:
                return round(random.uniform(6, 6.9), 1)
            elif 7 < (self.horas * 0.3):
                return 7

        if actividad == "METACLASS" or actividad == "SERIALIZACION":

            if 0 <= (self.horas * 0.3) <= 4:
                return round(random.uniform(1.1, 3.9), 1)
            elif 4 < (self.horas * 0.3) <= 7:
                return round(random.uniform(4, 5.9), 1)
            elif 7 < (self.horas * 0.3) <= 9:
                return round(random.uniform(6, 6.9), 1)
            elif 9 < (self.horas * 0.3):
                return 7

        if actividad == "FUNCIONAL":
            if 0 <= (self.horas * 0.3) <= 3:
                return round(random.uniform(1.1, 3.9), 1)
            elif 3 < (self.horas * 0.3) <= 7:
                return round(random.uniform(4, 5.9), 1)
            elif 7 < (self.horas * 0.3) <= 8:
                return round(random.uniform(6, 6.9), 1)
            elif 8 < (self.horas * 0.3):
                return 7

        if actividad == "SIMULACION":
            if 0 <= (self.horas * 0.3) <= 3:
                return round(random.uniform(1.1, 3.9), 1)
            elif 3 < (self.horas * 0.3) <= 6:
                return round(random.uniform(4, 5.9), 1)
            elif 6 < (self.horas * 0.3) <= 8:
                return round(random.uniform(6, 6.9), 1)
            elif 8 < (self.horas * 0.3):
                return 7

        if actividad == "WEBSERVICES":
            if 0 <= (self.horas * 0.3) <= 2:
                return round(random.uniform(1.1, 3.9), 1)
            elif 2 < (self.horas * 0.3) <= 7:
                return round(random.uniform(4, 5.9), 1)
            elif 7 < (self.horas * 0.3) <= 8:
                return round(random.uniform(6, 6.9), 1)
            elif 8 < (self.horas * 0.3):
                return 7

    def operar_confianza(self, actividad, es_actividad=0, es_tarea=0, es_control=0, ):
        """
        Metodo para ir sumando o restando confianza al alumno luego de una entrega de notas

        :param es_actividad: int (solo en el caso de que haya nota actividad)
        :param es_tarea: int (solo en el caso de que haya nota actividad)
        :param es_control: int (solo en el caso de que haya nota actividad)
        :return: None
        """

        if es_actividad != 0:
            nota_esperada = self.notas_actividad[actividad][0]
            nota_final = self.notas_actividad[actividad][1]

        if es_control != 0:
            nota_esperada = self.notas_controles[actividad][0]
            nota_final = self.notas_controles[actividad][1]

        if es_tarea != 0:
            nota_esperada = self.notas_tareas[actividad][0]
            nota_final = self.notas_tareas[actividad][1]

        self.confianza += 3 * es_actividad * (nota_final - nota_esperada) + 5 * es_tarea * (
            (nota_final - nota_esperada)) + es_control * (nota_final - nota_esperada)
        if self.confianza < 1:
            self.confianza = 1

    def estudio_diario(self, contenido):
        """
        Metodo para simular el estudio diario del alumno
        :param contenido: Contendo Actividad
        :return: None
        """
        self.manejo_contenidos[contenido] += ((1 / parameters.parametros[contenido]) * ((self.horas * 0.3))) / 7

    def estudio_semanal_tarea(self, tarea):
        """
            Simular el estudio de la tarea por semana

        :param tarea: numero de tarea
        :return: None
        """
        self.horas_tarea[tarea] += 0.7 * self.horas

    def aumentar_nivel_programacion(self):
        """Metodo para aumentar el nivel de programacion"""
        self.nivel *= (1.05 + self.consulta - self.fiesta)
        self.consulta = 0
        self.fiesta = 0

    def entregar_tarea(self, numero, exigencia):
        """
         Metodo para que el alumno entregue la tarea
        :param numero: Numero de tarea
        :param exigencia: Dificultad asignada por ayudantes
        :return:
        """
        """if numero == 1:
            b = self.nota_esperada_tarea(self.lista_contenidos_tareas.pop(0))
            self.lista_contenidos_tareas.pop(0)
            print(self.lista_contenidos[numero-1])
            self.notas_tareas[numero].append(b)
            progresopep8 = 0.5 * self.horas_tarea[numero] + 0.5 * self.nivel
            progresocontenido = 0.7 *  + self.manejo_contenidos[self.lista_contenidos[numero]] + 0.1 * self.nivel + 0.5 * self.horas_tarea[numero]
            progresofuncionalidad = 0.5 *  + self.manejo_contenidos[self.lista_contenidos[numero]] + 0.1 * self.nivel + 0.4 *  self.horas_tarea[numero]
            progresofinal = 0.4 * progresofuncionalidad + 0.4 * progresocontenido + 0.2 * progresopep8
            notafinal = max((progresofinal / exigencia) * 7, 1)
            notafinal = min(notafinal, 7)
            self.notas_tareas[numero].append(notafinal)"""
        if True:  # numero != 1:
            a = self.nota_esperada_tarea(self.lista_contenidos_tareas.pop(0))
            b = self.nota_esperada_tarea(self.lista_contenidos_tareas.pop(0))

            self.notas_tareas[numero].append((a + b) / 2)
            progresopep8 = 0.5 * self.horas_tarea[numero] + 0.5 * self.nivel
            progresocontenido = 0.7 * (((self.manejo_contenidos[self.lista_contenidos[numero - 1]]) + (
                self.manejo_contenidos[self.lista_contenidos[numero]])) / 2) + 0.1 * self.nivel + 0.5 * \
                                                                                                  self.horas_tarea[
                                                                                                      numero]
            progresofuncionalidad = 0.5 * (((self.manejo_contenidos[self.lista_contenidos[numero - 1]]) + (
                self.manejo_contenidos[self.lista_contenidos[numero]])) / 2) + 0.1 * self.nivel + 0.4 * \
                                                                                                  self.horas_tarea[
                                                                                                      numero]
            if self.personalidad == "Eficiente":
                progresofinal = 0.4 * progresofuncionalidad * 1.1 + 0.4 * progresocontenido * 1.1 + 0.2 * progresopep8 * 1.1
            if self.personalidad == "Artistico":
                progresofinal = 0.4 * progresofuncionalidad + 0.4 * progresocontenido + 0.2 * progresopep8 * 1.2
            if self.personalidad == "Teorico":
                progresofinal = 0.4 * progresofuncionalidad * 0.9 + 0.4 * progresocontenido * 0.9 + 0.2 * progresopep8 * 0.9
            notafinal = max((progresofinal / exigencia) * 7, 1)
            notafinal = min(notafinal, 7)
            self.notas_tareas[numero].append(notafinal)

    def entregar_actividad(self, actividad, exigencia):
        """
        Metodo para que el alumno realize la actividad de la semana
        :param actividad: str Nombre actividad
        :param exigencia: str  Exigencia impuesta
        :return:
        """
        self.nota_esperada(actividad)
        progresopep8 = 0.7 * self.manejo_contenidos[actividad] + 0.2 * self.nivel + 0.1 * self.confianza
        progresofuncional = 0.3 * self.manejo_contenidos[actividad] + 0.6 * self.nivel + 0.1 * self.confianza
        progresocontenido = 0.7 * self.manejo_contenidos[actividad] + 0.2 * self.nivel + 0.1 * self.confianza
        progresofinal = 0.4 * progresofuncional + 0.4 * progresocontenido + 0.2 * progresopep8
        notafinal = max((progresofinal / exigencia) * 7, 1)
        notafinal = min(notafinal, 7)
        if self.personalidad == "Eficiente":
            if actividad == "FUNCIONAL" or actividad == "THREADING":
                self.notas_actividad[actividad].append(min(notafinal + 1, 7))
            else:
                self.notas_actividad[actividad].append(notafinal)
        if self.personalidad == "Artistico":
            if actividad == "WEBSERVICES" or actividad == "GUI":
                self.notas_actividad[actividad].append(min(notafinal + 1, 7))
            else:
                self.notas_actividad[actividad].append(notafinal)

        if self.personalidad == "Teorico":
            if actividad == "METACLASS":
                self.notas_actividad[actividad].append(min(notafinal + 1, 7))
            else:
                self.notas_actividad[actividad].append(notafinal)

    def entregar_control(self, actividad, exigencia):
        """ Metodo para que cada alumno realice el control asignado
            :param actividad: str Nombre actividad
            :param exigencia: str  Exigencia impuesta
            :return: None
        """
        self.notas_controles[actividad] = [self.nota_esperada_tarea(actividad)]
        progresofuncional = 0.7 * self.manejo_contenidos[actividad] + 0.05 * self.nivel + 0.25 * self.confianza
        progresocontenidos = 0.3 * self.manejo_contenidos[actividad] + 0.2 * self.nivel + 0.5 * self.confianza
        progresofinal = 0.3 * progresofuncional + 0.7 * progresocontenidos
        notafinal = max((progresofinal / exigencia) * 7, 1)
        notafinal = min(notafinal, 7)
        self.notas_controles[actividad].append(notafinal)

    def rendir_examen(self, contenidos, exigencia):
        """
        Metodo para que cada alumno realice el examen
        :param contenidos: list contenidos examen elegidos por performance alumnos
        :param exigencia: float de exigencia impuesta por los profesores
        :return: None
        """
        progresopreguntas = []
        for contenido in contenidos:
            progresoscontenido = 0.5 * self.manejo_contenidos[contenido] + 0.1 * self.nivel + 0.4 * self.confianza
            progresofuncionalidad = 0.3 * self.manejo_contenidos[contenido] + 0.2 * self.nivel + 0.5 * self.confianza
            progresopreguntas.append(0.3 * progresofuncionalidad + 0.7 * progresoscontenido)
        self.examen = min(max(np.mean(progresopreguntas) * 7 / (exigencia), 1), 7)

        # print([nota[1] for  nota in self.notas_controles.values()])
        # print([self.notas_actividad[i][1] for i in self.lista_contenidos if
        # len(self.notas_actividad[i]) != 0])
        # print([self.notas_tareas[i][1] for i in range(1,7) if
        # len(self.notas_tareas[i]) != 0])
        # print(self.promedio)

    def botar_ramo(self):
        """Metodo para analizar la opcion de bota de ramo, se reajusto la funcion para arecarla lo mas posible a la realidad"""
        s = self.confianza * 0.8 + 0.5 * np.mean([self.notas_tareas[2][1] + self.notas_tareas[1][1] +
                                                  self.notas_actividad["POO"][1] + self.notas_actividad["HERENCIA"][1] +
                                                  self.notas_actividad["LISTAS_SET_DICT"][1] +
                                                  self.notas_actividad["ARBOL"][1]])
        if s < 11:
            print(self.name + " ha Botado el ramo")
            self.botado = True
