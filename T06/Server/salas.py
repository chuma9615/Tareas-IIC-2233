import os
import threading
import numpy as np
import threading
import time as tm


class Sala():
    def __init__(self, name):
        self.name = name
        self.songs = {}
        self.info = {}
        self.time = 20
        self.load_songs()
        self.thread = threading.Thread(target=self.run,daemon=True)
        self.thread.start()

    def load_songs(self):
        path = (os.getcwd() + '/Songs/' + self.name)
        lista = [a for a in os.listdir(path) if
                 'Icon' not in a]  # Linea para borrar archivo extraño que aparecia en mi directorio (icon.r)
        for item in lista:
            archi = open(path + '/' + item, 'rb')
            self.songs[item] = archi.read()

    def run(self):
        cancion = np.random.choice(list(self.songs.keys()), 1, replace=False)
        self.info['cancion actual'] = cancion[0]
        while True:
            if self.time == 0:
                cancion = np.random.choice(list(self.songs.keys()), 1, replace=False)
                self.info['cancion actual'] = cancion[0]
                self.time = 20
                self.info['tiempo'] = self.time
            else:
                self.time-=1
                self.info['tiempo'] = self.time
            tm.sleep(1)

    def __repr__(self):
        return self.name

