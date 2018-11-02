#Readme Tarea 3
---
####Domingo Ramirez C.
##Librerias Usadas

Matplotlib

Numpy (Test only)

Unitest (Test only)

Functools (reduce)

##Alcances tarea
-Para ir guardando las variables asignadas se creo un modulo diccionario para asi poder referenciarlo desde multiples partes del programa

-Para la funcion de graficar, si se solicita mostrar dos graficos de un set de consultas este solo mostrara el ultimo, esta decision se tomo asi ya que era la unica forma de que al graficar el programa no se detuviera en esa linea (evitar que sea una blocking function usando plt.ion)

-Para testear las funciones y los errores se uso el metodo unittesting en el cual se asignaba un set de parametros y se comparaba con una respuesta fidedigna de la operacion a realizar (usando numpy en ciertos casos).

-al aparecer un error, para simplificaciones este lanza el comando que falla y la causa de falla

-en el main se utilizaron for in solo para iterar sobre el querry array, estando esto permitido ya que no es parte de la logica del programa

-en la funcion graficar normalizado, se usaron los valores negativos como tal

-se asumen la operacion de factoriales solo con numeros enteros

-

