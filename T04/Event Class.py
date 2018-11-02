

class Catedra:
    def __init__(self,main, profesor, ayudantes, time, content):
        self.main = main
        self.profesor = profesor
        self.seccion = profesor.seccion
        self.ayudantes = ayudantes
        self.tiempo_inicial = time
        self.content = content

    def ejecutar(self):
        if self.main.control <5:
            for alumno in self.main.lista_alumnos:
                pass



class Actividad:
    def __init__(self, tipo, profesor, ayudantes, time):
        self.tiempo_inicial = time
        self.profesor = profesor
        self.seccion = profesor.seccion
        self.ayudantes = ayudantes
        self.tipo = tipo

class ConsultasProfesor:
    def __init__(self, time):
        self.tiempo_inicial = time

class Ayudantia:
    def __init__(self, Ayudante, materia, time):
        self.tiempo_inicial = time
        self.ayudante = Ayudante
        self.materia = materia

class ReunionDocencia:
    def __init__(self,time):
        self.tiempo_inicial = time

class ReunionTareas:
    def __init__(self,time):
        self.tiempo_inicial = time

class EntregarTarea:
    def __init__(self,time):
        self.tiempo_inicial = time

class BotarRamo:
    def __init__(self,time):
        self.tiempo_inicial = time

class Fiesta:
    def __init__(self,time):
        self.tiempo_inicial = time

class Futbol:
    def __init__(self,time):
        self.tiempo_inicial = time

class CorteAgua:
    def __init__(self,time):
        self.tiempo_inicial = time

class Examen:
    def __init__(self,time):
        self.tiempo_inicial = time