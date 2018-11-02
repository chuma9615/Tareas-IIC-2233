import threading
import socket
import pickle
import os
import time
import salas as sl
import user_management as uma

port = 2020
host = "0.0.0.0"


class Server:
    def __init__(self, port, host):
        print("Inicializando servidor...")

        # Inicializar socket principal del servidor.
        self.host = host
        self.port = port
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.update_bool = True
        self.bind_and_listen()
        self.accept_connections()
        self.clients = {}
        self.rooms = []
        self.inforooms = {}
        self.cargar_salas()

    # El método bind_and_listen() enlazará el socket creado con el host y puerto
    # indicado. Primero se enlaza el socket y luego que esperando por conexiones
    # entrantes, con un máximo de 5 clientes en espera.
    def bind_and_listen(self):
        self.socket_servidor.bind((self.host, self.port))
        self.socket_servidor.listen(5)
        print("Servidor escuchando en {}:{}...".format(self.host, self.port))

    # El método accept_connections() inicia el thread que aceptará clientes.
    # Aunque podríamos aceptar clientes en el thread principal de la instancia,
    # resulta útil hacerlo en un thread aparte que nos permitirá realizar la
    # lógica en la parte del servidor sin dejar de aceptar clientes. Por ejemplo,
    # seguir procesando archivos.
    def accept_connections(self):
        thread = threading.Thread(target=self.accept_connections_thread)
        thread.start()

    # El método accept_connections_thread() será arrancado como thread para
    # aceptar clientes. Cada vez que aceptamos un nuevo cliente, iniciamos un
    # thread nuevo encargado de manejar el socket para ese cliente.
    def accept_connections_thread(self):
        print("Servidor aceptando conexiones...")

        while True:
            client_socket, _ = self.socket_servidor.accept()
            listening_client_thread = threading.Thread(
                target=self.listen_client_thread,
                args=(client_socket,),
                daemon=True
            )
            listening_client_thread.start()

    # Usaremos el método send() para enviar mensajes hacia algún socket cliente.
    # Debemos implementar en este método el protocolo de comunicación donde los
    # primeros 4 bytes indicarán el largo del mensaje.
    @staticmethod
    def send(value, socket):
        msg_bytes = pickle.dumps(value)
        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")
        socket.send(msg_length + msg_bytes)
        print('Se ha terminado el envio')

    # El método listen_client_thread() sera ejecutado como thread que escuchará a un
    # cliente en particular. Implementa las funcionalidades del protocolo de comunicación
    # que permiten recuperar la informacion enviada.
    def listen_client_thread(self, client_socket):
        print("Servidor conectado a un nuevo cliente...")
        client_update =threading.Thread(target=self.update,args=(client_socket,),daemon=True)
        client_update.start()
        while True:
            response_bytes_length = client_socket.recv(4)
            response_length = int.from_bytes(response_bytes_length, byteorder="big")
            response = b""
            while len(response) < response_length:
                try:
                    response += client_socket.recv(256)
                except EOFError:
                    pass
            try:
                received = pickle.loads(response)
            except EOFError:
                received = ''

            if received != "":
                # El método `self.handle_command()` debe ser definido. Este realizará
                # toda la lógica asociado a los mensajes que llegan al servidor desde
                # un cliente en particular. Se espera que retorne la respuesta que el
                # servidor debe enviar hacia el cliente.
                response = self.handle_command(*received, client_socket)
    def update(self, client_socket):
        while True:
            if self.update_bool:
                for sala in self.rooms:
                    self.inforooms[sala.name]=sala.info
                self.send(('update',self.inforooms), client_socket)
                time.sleep(1)

    def cargar_salas(self):
        path = os.getcwd() + '/Songs'
        lista = [a for a in os.listdir(path) if
                 'DS_Store' not in a]
        for item in lista:
            self.rooms.append(sl.Sala(item))

    def handle_command(self, tipo, mensaje, client_socket):
        if tipo == 'singin':
            usuario = mensaje
            if usuario in self.clients.values():
                response = False
            elif usuario not in self.clients.values():
                self.clients[client_socket] = usuario
                if not uma.usuario_existe(usuario):
                    uma.guardar_usuarios(usuario)
                response = True

            if not response:
                self.send((tipo, response), client_socket)
            if response:
                self.send((tipo, response), client_socket)

        if tipo == 'points':
            print("se ha envidao señal de puntos ")
            self.send((tipo, uma.cargar_usuario(mensaje)), client_socket)

        if tipo == 'disconnect':
            del self.clients[client_socket]
            print("cliente desconectado de servidor")

        if tipo == 'send_rooms':
            self.send(('send_rooms', ([a for a in os.listdir(os.getcwd() + '/Songs') if
                                      'DS_Store' not in a], [(list(sala.songs.keys()), sala.name) for sala in self.rooms])),
                      client_socket)

        if tipo == 'sendsongs':
            self.update_bool = False
            for sala in self.rooms:
                if sala.name == mensaje:
                    for song in sala.songs.keys():
                        print('se ha envidao señal para enviar canciones ' + song)
                        time.sleep(0.1)
                        self.send(('sendsongs', sala.songs[song], song), client_socket)
            time.sleep(0.1)
            self.send(('endsongstransfer', None), client_socket)
            self.update_bool = True



if __name__ == "__main__":
    server = Server(port, host)
