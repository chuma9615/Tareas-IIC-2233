class Nodo:
    def __init__(self, valor=None):
        self.siguiente = None
        self.valor = valor

    def __str__(self):
        return self.valor


class _IteradorListaEnlazada:
    def __init__(self, prim):
        self.actual = prim

    def __next__(self):
        if self.actual == None:
            raise StopIteration("No hay más elementos en la lista")
        dato = self.actual.valor
        self.actual = self.actual.siguiente
        return dato


class ListaLigada:
    def __init__(self, *args):
        self.cola = None
        self.cabeza = None
        self.len = 0
        for arg in args:
            self.append(arg)

    def __len__(self):
        return self.len

    def __setitem__(self, key, value):
        aux = Nodo(value)

        if not (0 <= key < self.len):
            raise IndexError("Índice fuera de rango")

        if key == 0:
            aux.siguiente = self.cabeza.siguiente
            self.cabeza = aux

        else:
            n_ant = self.cabeza
            n_act = n_ant.siguiente
            for pos in range(1, key):
                n_ant = n_act
                n_act = n_ant.siguiente

            n_act.valor = aux.valor
            aux.siguiente = n_act.siguiente

    def __delitem__(self, key):
        if not (0 <= key < self.len):
            raise IndexError("Índice fuera de rango")

        if key == 0:
            self.cabeza = self.cabeza.siguiente

        else:
            n_ant = self.cabeza
            n_act = n_ant.siguiente
            for pos in range(1, key):
                n_ant = n_act
                n_act = n_ant.siguiente
            n_ant.siguiente = n_act.siguiente
        self.len -= 1

    def pop(self, i=None):  # atributo inspirado en http://librosweb.es/libro/algoritmos_python/capitulo_16/la_clase_listaenlazada.html

        if i is None:
            i = self.len - 1

        if not (0 <= i < self.len):
            raise IndexError("Índice fuera de rango")

        if i == 0:
            valor = self.cabeza.valor
            self.cabeza = self.cabeza.siguiente

        else:
            n_ant = self.cabeza
            n_act = n_ant.siguiente
            for pos in range(1, i):
                n_ant = n_act
                n_act = n_ant.siguiente

            valor = n_act.valor
            n_ant.siguiente = n_act.siguiente

        self.len -= 1

        return valor

    def append(self, valor):
        if not self.cabeza:
            # Revisamos si el nodo cabeza tiene un nodo asignado.
            # Si no tiene nodo, creamos un nodo
            self.cabeza = Nodo(valor)
            self.cola = self.cabeza
            self.len += 1
        else:
            # Si ya tiene un nodo
            self.cola.siguiente = Nodo(valor)
            self.cola = self.cola.siguiente
            self.len += 1

    def __getitem__(self, posicion):
        nodo = self.cabeza

        for i in range(posicion):
            if nodo:
                nodo = nodo.siguiente
        if not nodo:
            return "posicion no encontrada"
        else:
            return nodo.valor

    def __repr__(self):
        if len(self) ==0:
            return "[]"
        rep = '['
        nodo_actual = self.cabeza

        while nodo_actual:
            if type(nodo_actual.valor) == str:
                rep += '{0}, '.format("'" + str(nodo_actual.valor) + "'")
                nodo_actual = nodo_actual.siguiente
            else:
                rep += '{0}, '.format(nodo_actual.valor)
                nodo_actual = nodo_actual.siguiente

        return rep[:-2] + "]"

    def __iter__(self):
        return _IteradorListaEnlazada(self.cabeza)


