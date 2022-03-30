####################################################################################
####################################···DrawSim···###################################
####################################################################################

Version: 2.0
Author: Nicolás Rodrigo Pérez
Date: 14/10/2021

#####################################################################################
####################################  DESCRIPCIÓN  ##################################
#####################################################################################

DrawSim es un simulador de dibujo que permite al usuario colocar puntos en un canvas, unirlos mediante
lineas generadas por distintos algoritmos, y agrupar estas lineas para crear formas a las que
poder aplicar transformaciones 2D.

La aplicacion se ha generado gracias a la libreria Tkinter de python, implementando una clase DrawSim,
la cual contiene los métodos necesarias para crear la interfaz de usuario, ademas de las necesarias para
dibujar puntos, crear lineas, y otras funcionalidades que se detallan en el apartado de uso.

Para poder mostrar las coordenadas de los elementos que situamos en el canvas, se ha de llevar a cabo
un preproceso sobre las coordenadas de este, con el fin de obtener las coordenadas cartesianas
que nosotros somos capaces de interpretar mas facilmente, pues en un canvas el origen esta Situado
tipicamente en la esquina superior izquierda.

Al ejecutar la aplicacion se distinguen cuatro elementos importantes:

·canvas: espacio donde el usuario puede dibujar. Ocupa el maximo espacio posible y muestra los ejes x e y.

·coordenadas de punto: muestra las coordenadas cartesianas de los puntos en el canvas. Situado
en la esquina superior derecha.

·coordenadas de linea: muestra las coordenadas cartesianas de los puntos que forman la última línea
en el canvas. Situado en la parte inferior.

·botonera: botones con los que el usuario maneja las funcionalidades de la aplicacion, detallado
en el apartado de uso. Situado debajo de las coordenadas de punto.

#####################################################################################
####################################  USO  ##########################################
#####################################################################################

Podemos ejecutar el simulador de varias maneras:

-Dentro de la carpeta DrawSim podemos copiar el logo de la aplicacion (acceso directo) en nuestro
 escritorio y ejecutar desde el mismo. (puede ser que solo funcione en windows)

-Dentro de la carpeta DrawSim podemos hacer doble click sobre el fichero launch.pyw lo que
 ejecutara el simulador. (puede ser que solo funcione en windows)

-Dentro de la carpeta DrawSim encontramos la carpeta src, dentro de la cual esta el archivo
 DrawSim.py, el cual ejecutaremos con nuestro ide de python favorito o linea de comandos.

El funcionamiento de la aplicacion se basa en la definicion de linea, la cual se compone de un
punto inicial y uno final, unidos por una sucesion de puntos, por lo que lo primero que haremos
sera dibujar dos puntos, ya sea con el puntero sobre el canvas, o con la funcion de dibujar un punto
dadas sus coordenadas, y procederemos a pulsar uno de los botones linea para unir estos puntos
con el algoritmo de linea deseado.

Para poder crear una forma en el canvas, se han de seleccionar las lineas que queremos que
la formen pulsando sobre ellas con click derecho, y a continuacion pulsaremos el boton "New shape",
que agrupará estas lineas en una única linea que consideraremos una "forma"(shape).

Para poder realizar transformaciones 2D, basta con seleccionar con click derecho de nuevo la forma
sobre la que queremos aplicarlas, teniendo que seleccionar de nuevo una forma cada vez que realicemos
una transformacion.

Se detalla a continuacion el funcionamiento de cada boton:

##############################···Botones generales···################################

-New dot: Coloca en el canvas un punto en las coordenadas cartesianas x e y indicadas en los cuadros de
 texto superiores, y muestra estas coordenadas en el elemento coordenadas de punto. Para situar el cursor
 en estos cuadros de texto basta con pulsar el tabulador, y volveremos a pulsarlo para cambiar de la
 coordenada x a la y y viceversa.

    · -> tambien se puede hacer click izquierdo sobre el canvas y colocar puntos de esta manera. (mas intuitivo)

-New shape: Crea una nueva forma agrupando las lineas que hemos seleccionado previamente con click derecho, y muestra
 las coordenadas de dicha forma en el elemento coordenadas de linea.

-Anim.: Se reproduce en el canvas la animacion que hayamos indicado en el cuadro de texto adyacente al boton.

-Delete dot: borra el ultimo punto colocado en el canvas, asi como sus coordenadas en el elemento
 coordenadas de punto.

-Delete line: borra la ultima linea dibujada en el canvas, asi como sus coordenadas en el elemento
 coodenadas de linea, mostrando en este las coordenadas de la linea previa a la eliminada, si existe.

-Delete Shape: borra la ultima forma creada en el canvas, asi como sus coordenadas en el elemento
 coodenadas de linea, mostrando en este las coordenadas de la linea o forma previa a la eliminada, si existe.

-Delete all: borra todos los elementos del canvas, asi como toda la informacion mostrada en los elementos
 coordenadas de punto y de linea.

-Size: el usuario introduce el numero de pixeles que tendra el lado del cuadrado(punto) que se coloca en
el canvas, y a continuacion pulsa el boton para fijar el nuevo tamaño. Por defecto es 3.

-Color: se presenta una ventana en la que el usuario puede elegir un nuevo color para los elementos
que coloca en el canvas.

-Save: guarda en un documento las coordenadas cartesianas de todas las lineas que se han dibujado en el canvas.

    · -> tambien se puede guardar con ctrl+s.

-Pattern: cambia el modo de dibujar las lineas (visualizacion). Por defeto (desactivado), para dibujar una linea,
 se pintan todos los pixeles que se obtienen con su algoritmo, lo que debido a las densidades de pixeles actuales,
 no permite distinguir el patron de cada algoritmo, y la linea se podria considerar en HD. Por el contrario si
 activamos el patron (pattern), dependiendo del Size que hayamos escogido, se escalara la linea Para poder mostrar
 el patron caracteristico de su algoritmo.

-Exit: cierra la aplicacion.

    · -> tambien se puede cerrar con ctrl+x.

########################···Botones de Algoritmos de linea···#########################

-> Requisito previo: tiene que haber al menos dos puntos en el canvas.

-line1: dibuja una linea entre los dos ultimos puntos con el algoritmo slope intercept original.

-line2: dibuja una linea entre los dos ultimos puntos con el algoritmo slope intercept modificado.

-line3: dibuja una linea entre los dos ultimos puntos con el algoritmo DDA.

-line4: dibuja una linea entre los dos ultimos puntos con el algoritmo de Bresenham modificado.

########################···Botones de Transformaciones 2D···##########################

-> Requisito previo: haber seleccionado una linea o forma con click derecho.

-Traslacion: realiza una traslacion del elemento seleccionado en x e y en las unidades indicadas.

-Escalado: realiza un escalado del elemento seleccionado en x e y en las unidades indicadas.

-Rotacion: realiza una rotacion del elemento seleccionado de los grados indicados, en sentido horario o antihorario.

-Cizalla: realiza una cizalla del elemento seleccionado en x e y en las unidades indicadas.

-Reflexion: realiza una reflexion del elemento seleccionado respecto del eje x, del eje y, o  de una recta de la que se indican m y b.
