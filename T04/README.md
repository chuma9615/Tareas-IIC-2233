#README TAREA 4
Domingo Ramirez.


19.308.306-4

##Modulos utilizados

-Numpy

-Sys

-Math

-Random

-CSV

-matplotlib

-Tabulate

##Supuestos
-para cargar los parametros por defecto se usaron dos archivos csv, Parametros_creditos.csv y Parametros_dificultad.csv

-la simulacion parte el viernes

-las tareas se entregan los jueves

-reuniones de docensia son los 

-clases son los jueves y ayudantias los martes

-los ayudantes se reunen el mismo dia de entrefa a definir la dificultad de la tarea y actividad

-La probabilidad de distribucion de personalidad para los alumnos era constante

-La probabilidad de escuchar un tip en la clase es del 50%

-se decidio que al calcular la nota esperada los decimales se redondean hacia el proximo valor entero

-para calcular las notas de las tareas se calcula el promedio de avance de los dos contenidos

-Los beneficios/descuentos de nota por personalidad se asignan al hacer cada evaluacion.

-Para hacer mas real el examen se hizo que los alumnos estudiaran 5 dias antes materias al azar del curso por dia

-se reformulo la funcion que modela cuanta gente bota el ramo para ajustarlo mas a la realidad tomando como referencia este semestre (32 retiros). la formula se ajusto como sigue 
		
		s = 0.8 * Confianza + 0.5*Promedio
		
		promedio es el promedio ponderado entre tareas y 
			actividades
			
		s<12 se bota el ramo
-Para calcular el promedio del ramo se utilizo la siguente formula

		0.3*prom(tareas) + 0.3*prom(actividades + 
		0.3*examen + 0.1*prom(controles)
		
-Al momento de las estadisticas, un alumno retirado que se intente buscar no aparecera en la base de datos puesto que su curso fue retirado, tal como funciona en la realidad. sin embargo estos alumnos si estan guardados en la clase para calcular otras estadisticas