import json

def guardar_usuarios(name):
    with open('usuarios.json') as arch:
        diccio = json.load(arch)
        diccio[name]=0
        arch.close()
    with open('usuarios.json','w') as arch:
        json.dump(diccio,arch)

def actualizar_usuarios(name,puntos):
    with open('usuarios.json') as arch:
        diccio = json.load(arch)
        diccio[name]=puntos
        arch.close()
    with open('usuarios.json','w') as arch:
        json.dump(diccio,arch)

def usuario_existe(usuario):
    with open('usuarios.json') as arch:
        diccio = json.load(arch)
        if usuario in diccio.keys():
            return True
        return False

def cargar_usuario(usuario):
    with open('usuarios.json') as arch:
        diccio = json.load(arch)
        return diccio[usuario]
