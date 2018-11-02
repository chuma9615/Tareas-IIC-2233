class Profesor:
    def __init__(self, name, seccion):
        """

        :param name: str con el nombre del profesor
        :param seccion: int con la seccion a la que pertenece
        """
        self.name = name
        self.seccion = seccion
        self.previous_week = []
        self.alumnos = []

    def ayudar(self, nomina):
        """ Metodo que genera que el profesor ayude al alumno que acude a su oficina"""
        for alumno in nomina:
            alumno.consulta = 0.08
        self.previous_week = nomina

    def __repr__(self):
        return self.name
