class ExcessOrFaltaDeParametros(Exception):
    def __init__(self):
        super().__init__("Argumento invalido, parametros incorrectos")


class ImposibleProcesar(Exception):
    def __init__(self, mensaje="imposible procesar"):
        super().__init__(mensaje)
