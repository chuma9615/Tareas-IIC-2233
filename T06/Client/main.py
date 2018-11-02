from PyQt5 import uic, QtMultimedia
from PyQt5.QtWidgets import QApplication, QLabel, QListWidgetItem, QListWidget
import sys
import os
import client

import time

formulario = uic.loadUiType('gui/GUIstacked.ui')


class MainWindow(formulario[0], formulario[1]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setCurrentIndex(0)
        self.boton_conectar.clicked.connect(self.conectar)
        self.lista_salas.itemDoubleClicked.connect(self.clicklista)
        self.Opcion1.clicked.connect(self.prueba)
        self.cancion = None
        self.cliente = None
        self.sala_actual = None
        self.show()

    def prueba(self):
        self.setCurrentIndex(1)

    def conectar(self):
        if self.warning.text() == 'Nombre ya en uso':
            self.cliente.name = self.texto_usuario.text().lower()
            self.cliente.send(('singin', (self.cliente.name)))
        if self.texto_usuario.text() == '':
            self.warning.setText("Usuario Invalido")

        elif self.texto_usuario.text() != '' and self.warning.text() != 'Nombre ya en uso':
            self.cliente = client.Client(client.PORT, client.HOST, self.texto_usuario.text().lower())
            self.cliente.gui = self
            self.cliente.send(('singin', (self.cliente.name)))
            self.Nombre.setText(self.cliente.name)

    def clicklista(self, name):
        self.status.setText('Cargando sala')
        self.sala_actual = name.text()
        self.pasar_canciones(name.text())




    def handle_command(self, tipo, mensaje):
        if tipo == 'update':
            self.cliente.inforooms = mensaje

        if tipo == 'singin':
            if mensaje:
                self.cliente.ask_rooms()
                self.setCurrentIndex(1)
                self.cliente.send(('points', (self.cliente.name)))
            if not mensaje:
                self.warning.setText('Nombre ya en uso')

        if tipo == 'send_rooms':
            self.cliente.salas = mensaje[0]
            self.cliente.canciones = mensaje[1]
            for item in self.cliente.salas:
                ite = QListWidgetItem("{}".format(item))
                # ite.clicked.connect(lambda:self.clicklista(ite.text))
                self.lista_salas.addItem(ite)
            self.lista_salas.show()

        if tipo == 'points':
            self.cliente.puntos = mensaje
            self.Puntuacion.setText(str(self.cliente.puntos))

        if tipo == 'endsongstransfer':
            self.sala()

    def pasar_canciones(self, name):
        for sala in self.cliente.canciones:
            if sala[1] == name:
                if sala[0][0] not in os.listdir(os.getcwd()):
                    self.cliente.send(('sendsongs', (name)))
                else:
                    self.sala()

    def sala(self):
        self.setCurrentIndex(2)
        self.status.setText(' ')
        self.nombresala.setText(self.sala_actual)
        self.tocarcancion()

    def tocarcancion(self):
        self.cancion = QtMultimedia.QSound(self.cliente.inforooms[self.sala_actual]['cancion actual'],self)
        self.cancion.play()


    def closeEvent(self, event):
        if self.cliente != None:
            self.cliente.send(('disconnect', (self.cliente.name, self.cliente.puntos)))
        event.accept()


if __name__ == '__main__':
    app = QApplication([])
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
