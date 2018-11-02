###Readme Tarea 2
##Explicacion listaligada
1. el init lo construi de manera que pudiera aceptar un rango variable al inicializar la instancia
2. la funcion len retorna la suma de los elementos appendados a la lista 
3. la funcion setitem funciona retornando error si el indice esta fuera del rango del len, en el caso contrario va iterando los nodos de manera repetitiva hasta llegar al item correspondiente y de ahi editarlo
4. la funcion delitem es de manera similar a la anterios con la salvedad de que si se escoge el item 0 este se borra y se reemplaza el nodo 1 como nodo cabeza
5. el metodo pop itera sobre los nodo y retorna el nodo correspondiente al indice entregado por el usuario
6. append va al ultimo nodo y le asigna como link a el nodo que se esta uniendo, dejando al nuevo nodo como cola
7. get item funcionda de la misma manera que pop solo que no borra el item de la lista
7. la funcion repr retorna una version grafica de la lista con espacios y corchetes tal como las listas originales
8. iter utiliza una clase auxiliar que tiene el metodo iter y next que va recorriendo la lista y permite operar sobre esta

#Alcances tarea
Tuve que imlementar dos metodos poblar ya que no pude resolver el problema de invertir las columnas para que se agregaran las conexiones bidirwccionales, sin embargo mi programa funciona bien con esta implementacion.

Para las muertes asumi que si se cumplia la probabilidad, es decir, el numero al azar era menor o igual a la probabilidad, el porcentaje de la poblacion igual a la pribabilidad es el que se muere, esto se resolvio asi para ahorrar tiempo de ejecucion del programa

se asume que si un pais cierra sus fronteras y la cura ha sido descubierta, este no las vuelve a abrir a menos que la cura se haya insertado en su pais, para asi hacer mas sangriento el juego y que atraiga al malvado dr. makaravis.

las tasas de vida y muerte son acumuladas en el tiempo

las muertes e infecciones diarias son un informe por dia desde el inicio de la infeccion sobre los sucesos de las personas.

los gobiernos son solo un set de funciones dentro de un pais para asi agregar simplicidad al programa