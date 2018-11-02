# Implementación del cliente que envía los datos json,
# Poner atención en la serialización y transformación a bytes.

import socket
import sys
import pickle

MAX_SIZE = 1000
server_host = "192.168.1.101"  # Aquí debe ir la dirección ip del servidor
port = 12345


class Persona:
    def __init__(self, nombre, mail):
        self.nombre = nombre
        self.mail = mail


# Enviaremos esta instancia de la clase Persona
p1 = Persona("Juan Perez", "jp@algo.com")
message = pickle.dumps(p1)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((server_host, port))
except socket.gaierror as err:
    print("Error: No pudo conectarse {}".format(err))
    sys.exit()

s.sendall(message)
data = pickle.loads(s.recv(MAX_SIZE))
print(data.nombre)
print(data.mail)
s.close()