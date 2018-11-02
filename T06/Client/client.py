import threading
import socket
import pickle
import time


PORT = 2020
HOST = "127.0.0.1"

# La clase Client manejará toda la comunicación desde el lado del cliente.
# Implementa el esquema de comunicación donde los primeros 4 bytes de cada
# mensaje indicarán el largo del mensaje enviado.

class Client:
    def __init__(self, port, host, name=None):
        print("Inicializando cliente...")
        self.salas = []
        self.host = host
        self.port = port
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name
        self.gui = None
        self.canciones = None
        self.puntos = 0
        self.inforooms = {}
        try:
            self.connect_to_server()
            self.listen()
        except:
            print("Conexión terminada")
            self.socket_cliente.close()
            exit()

    def connect_to_server(self):
        self.socket_cliente.connect((self.host, self.port))
        print("Cliente conectado exitosamente al servidor...")

    def ask_rooms(self):
        self.send(('send_rooms', ('nothing')))

    def listen(self):
        thread = threading.Thread(target=self.listen_thread, daemon=True, name="Listen Thread")
        thread.start()

    # El método send() enviará mensajes segun el protocolo size + tupla.
    # La tupla tiene dos elemntos: tipo de msg y msg.
    # Ejemplo: ("SIGNIN", (user, pass))
    def send(self, msg):
        msg_bytes = pickle.dumps(msg)
        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")
        self.socket_cliente.send(msg_length + msg_bytes)

    def listen_thread(self):
        while True:
            response_bytes_length = self.socket_cliente.recv(4)
            response_length = int.from_bytes(response_bytes_length, byteorder="big")
            print(response_length)
            response = b""

            # Recibimos datos hasta que alcancemos la totalidad de los datos
            # indicados en los primeros 4 bytes recibidos.
            while len(response) < response_length:
                try:
                    response += self.socket_cliente.recv(1000000000)
                except EOFError:
                    pass
                try:
                    if response != '':
                        received = pickle.loads(response)
                except:
                    pass
            if received:
                if received[0] == 'sendsongs':
                    print(received[2])
                    with open(received[2],'wb') as music:
                        music.write(received[1])
                else:
                    self.gui.handle_command(*received)

if __name__ == '__main__':
    a=Client(PORT,HOST,'chuma45')
