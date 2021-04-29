ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6

# PIEZAS = (
#     ((0, 0), (1, 0), (0, 1), (1, 1)), # Cubo
#     ((0, 0), (1, 0), (1, 1), (2, 1)), # Z (zig-zag)
#     ((0, 0), (0, 1), (1, 1), (1, 2)), # S (-Z)
#     ((0, 0), (0, 1), (0, 2), (0, 3)), # I (línea)
#     ((0, 0), (0, 1), (0, 2), (1, 2)), # L
#     ((0, 0), (1, 0), (2, 0), (2, 1)), # -L
#     ((0, 0), (1, 0), (2, 0), (1, 1)), # T
# )

# Constantes del objeto Juego
JUEGO_INDICE_PIEZA_ACTUAL = 0
JUEGO_INDICE_GRILLA = 1
JUEGO_INDICE_PUNTOS = 3

#Constantes de las celdas
CELDA_VACIA = 0
CELDA_SUPERFICIE = 1

PUNTOS_POR_LINEA = 10

import random

def generar_pieza(rotaciones, indice_pieza=None):
    """
    Genera una nueva pieza de entre las piezas del juego al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """
    if indice_pieza != None and 0 <= indice_pieza < len(rotaciones):
        return rotaciones[indice_pieza][0]
    else:
        return random.choice(rotaciones)[0]

def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
    nueva_pieza = []
    for indice in range(len(pieza)):
        nueva_pieza.append((pieza[indice][0] + dx, pieza[indice][1] + dy))
    return tuple(nueva_pieza)

def crear_grilla():
    """Va a crear la matriz ancho por alto con 0s,esto va a devolver la matriz y se la asigno a grilla en crear_juego"""
    matriz = []
    for i in range(ALTO_JUEGO):
        matriz.append([CELDA_VACIA]*ANCHO_JUEGO)
    return matriz

def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).
    """
    pieza_actual = trasladar_pieza(pieza_inicial, ANCHO_JUEGO // 2, 0)
    grilla = crear_grilla()
    nuevo_juego = [pieza_actual, grilla, False, 0]
    
    return nuevo_juego

def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    grilla = obtener_grilla(juego)
    alto = len(grilla)
    ancho = len(grilla[0])
    return (ancho, alto)

def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """

    pieza_centrada = juego[JUEGO_INDICE_PIEZA_ACTUAL]

    return pieza_centrada

def obtener_grilla(juego):
    """Recibe juego y devuelve la posicion de la grilla."""
    return juego[JUEGO_INDICE_GRILLA]

def obtener_puntos(juego):
    """Recibe juego y devuelve el puntaje actual."""
    return juego[JUEGO_INDICE_PUNTOS]

def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    ancho, alto = dimensiones(juego)
    return 0 <= x <= ancho - 1 and 0 <= y <= alto - 1 and celda_tiene_valor(juego, x, y, CELDA_SUPERFICIE)
 
def colisiona_con_superficie(juego, pieza):
    """
    Recibe el juego y la pieza, verifica si la pieza
    colisiono con la superficie.
    """
    for x,y in pieza:
        if hay_superficie(juego, x, y):
            return True
    return False

def esta_en_grilla(juego, pieza):
    """Recibe juego y pieza, verifica si las piezas estan
    dentro de la grilla."""
    ancho, alto = dimensiones(juego)
    for x, y in pieza:
        if not (0 <= x <= ancho - 1 and 0 <= y <= alto - 1):
            return False
    return True

def celda_tiene_valor(juego, x, y, valor):
    """Recibe juego, las coordenadas "x" e "y", y un valor,
    verifica que la celda tiene ese valor."""
    grilla = obtener_grilla(juego)
    return grilla[y][x] == valor

def asignar_celda(juego, x, y, valor):
    """Recibe juego, las coordenadas "x" e "y", y un valor,
    se le asigna el valor a esa celda."""
    grilla = obtener_grilla(juego)
    grilla[y][x] = valor

def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    
    pieza, grilla, terminado, puntos = juego
    pieza_movida = trasladar_pieza(pieza, direccion, 0)

    if (not esta_en_grilla(juego, pieza_movida)) or (colisiona_con_superficie(juego, pieza_movida)):
        # El movimiento no es valido. Devuelve el juego original.
        return juego
            
    
    # Todas las posiciones son validas. Retorna nuevo estado de juego.
    juego_nuevo = [pieza_movida, grilla, terminado, puntos]
    
    return juego_nuevo

def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    
    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).
    
    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida 
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar 
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """
    grilla = obtener_grilla(juego)
    puntaje = obtener_puntos(juego)
    pieza = pieza_actual(juego)
    pieza_abajo = trasladar_pieza(pieza, 0, 1)
    hay_colision = colisiona_con_superficie(juego, pieza_abajo)
    esta_adentro = esta_en_grilla(juego, pieza_abajo)

    if not hay_colision and esta_adentro:
        # La pieza "sigue viva" (no colisiono con superficie ni se fue de la grilla).
        # Devolvemos el nuevo juego con la pieza en la nueva ubicación.
        
        juego_nuevo = [pieza_abajo, grilla, False, puntaje]
        cambiar_pieza = False
        return (juego_nuevo, cambiar_pieza)
    else:
        # La pieza termino su "ciclo". Hay que incorporarla a la superficie consolidada.
        consolidar_pieza(juego, pieza)

        # Eliminamos las lineas que se hayan completado y sumamos los puntos
        lineas_eliminadas = eliminar_lineas(juego)
        puntaje = puntaje + PUNTOS_POR_LINEA * len(lineas_eliminadas)
        reacomodar_superficie(juego, lineas_eliminadas)

        # Cambiamos la pieza actual por siguiente_pieza (si se puede).
        siguiente_pieza_centrada = trasladar_pieza(siguiente_pieza, ANCHO_JUEGO // 2, 0)
        hay_colision_sig_pieza = colisiona_con_superficie(juego, siguiente_pieza_centrada)
        esta_adentro_sig_pieza = esta_en_grilla(juego, siguiente_pieza_centrada)

        if not hay_colision_sig_pieza and esta_adentro_sig_pieza:
            # La pieza actual no colisiono con la superficie en lo alto de todo, por lo tanto, se cambia la pieza.
            cambiar_pieza = True
            juego_nuevo = [siguiente_pieza_centrada, grilla, False, puntaje]
            return (juego_nuevo, cambiar_pieza)
        else:
            # La pieza colisiona con la superficie en lo alto de todo y como resultado termina el juego.
            juego_nuevo = [pieza, grilla, True, puntaje]
            cambiar_pieza = False
            return (juego_nuevo, cambiar_pieza)
    
def consolidar_pieza(juego, pieza):
    """
    Recibe juego y pieza, cuando la pieza toca la superficie,
    este se consolida.
    """
    if esta_en_grilla(juego, pieza):
        for x, y in pieza:
            asignar_celda(juego, x, y, CELDA_SUPERFICIE)

def eliminar_lineas(juego):
    """ 
    Recorre la grilla y reemplaza las lineas completas (todos 1s) con 0s.
    """
    lineas_eliminadas = []
    grilla = obtener_grilla(juego)
    ancho, alto = dimensiones(juego)
    for numeroDeFila in range(alto):
        if es_fila_completa(juego, numeroDeFila):
            # La fila tiene todos 1s. La eliminamos (reemplazamos todos los valores con 0).
            rellenar_fila_con_vacio(juego, numeroDeFila)
            lineas_eliminadas.append(numeroDeFila)
    return lineas_eliminadas

def es_fila_completa(juego, numeroDeFila):
    """
    Recibe juego y el numero de filas, devuelve True si hay una fila completa, y False si
    la fila esta incompleta.
    """
    ancho, alto = dimensiones(juego)
    for x in range(ancho):
        if not hay_superficie(juego, x, numeroDeFila):
            return False
    return True

def rellenar_fila_con_vacio(juego, numeroDeFila):
    """Recibe juego y el numero de filas, se le asigna la celda vacia (0),
    si esa fila esta completa.
    """
    ancho, alto = dimensiones(juego)
    for x in range(ancho):
        asignar_celda(juego, x, numeroDeFila, CELDA_VACIA)

def reacomodar_superficie(juego, lineas_eliminadas):
    """Recibe juego y las lineas eliminadas,  busca las lineas eliminadas de forma inversa,
    luego borra esas lineas y por cada linea eliminada se inserta una linea de 0 en lo alto del tablero"""
    grilla = obtener_grilla(juego)
    ancho, alto = dimensiones(juego)

    lineas_descendientes = sorted(lineas_eliminadas, reverse = True)
    for linea in lineas_descendientes:
        #Borra la fila que tiene las lineas completas
        del grilla[linea]
    for i in range(len(lineas_descendientes)):
        grilla.insert(0,[0]*ancho)
    
def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """
    pieza_actual,grilla,juego_terminado,puntuacion = juego
    return juego_terminado

def rotar(juego, rotaciones):
    """ 
    De la misma forma que mover, rotar debería rotar la pieza actual; para esto recibe el juego y un 
    parámetro adicional con la información sobre las rotaciones.
    """
    pieza = pieza_actual(juego)
    pieza_ordenada = sorted(pieza)
    offset = pieza_ordenada[0]
    pieza_ordenada_en_origen = []
    for posicion in pieza_ordenada:
        pieza_ordenada_en_origen.append((posicion[0] - offset[0], posicion[1] - offset[1]))
    pieza_ordenada_en_origen_como_tupla = tuple(pieza_ordenada_en_origen)

    for rotacion in rotaciones:
        if pieza_ordenada_en_origen_como_tupla in rotacion:

            indice_rotacion_actual = rotacion.index(pieza_ordenada_en_origen_como_tupla)
            indice_siguiente_rotacion = (indice_rotacion_actual + 1) % len(rotacion)
            siguiente_rotacion_en_origen = rotacion[indice_siguiente_rotacion]
            siguiente_rotacion = []
            for posicion in siguiente_rotacion_en_origen:
                siguiente_rotacion.append((posicion[0] + offset[0], posicion[1] + offset[1]))
            juego[JUEGO_INDICE_PIEZA_ACTUAL] = siguiente_rotacion

    return juego

def guardar_partida(juego, ruta):
    """Guarda el juego en el estado actual en un archivo """
    with open(ruta,"w") as archivo:
        # Primero guardamos los puntos
        puntos = obtener_puntos(juego)
        archivo.write(str(puntos) + "\n")

        # Segundo se guarda la pieza actual
        pieza_actual = juego[JUEGO_INDICE_PIEZA_ACTUAL]
        pieza_actual_serializada = ""

        for x,y in pieza_actual:
            pieza_actual_serializada += f"{x},{y};"
        pieza_actual_serializada = pieza_actual_serializada.rstrip(";")

        archivo.write(pieza_actual_serializada + "\n")

        # Ultimo, se guarda toda la grilla
        grilla = obtener_grilla(juego)

        for fila in grilla:
            fila_serializada = ""

            for celda in fila:
                fila_serializada += f"{celda},"
            fila_serializada = fila_serializada.rstrip(",")
            
            archivo.write(fila_serializada + "\n")

def cargar_partida(ruta):
    """Carga una partida guardada desde un archivo. 
    Devuelve un estado del juego, de forma similar a crear_juego, pero en este caso el estado no es inicial, 
    sino que es el mismo estado que se guardó """
    with open(ruta) as partida:
        # La primera linea es el puntaje
        puntos = int(partida.readline().rstrip('\n'))
        
        # La segunda linea es la pieza actual
        pieza_actual_serializada = partida.readline().rstrip('\n')
        pieza_actual = []
        for posicion in pieza_actual_serializada.split(";"):
            x, y = posicion.split(",")
            pieza_actual.append((int(x), int(y)))
        
        # Por ultimo, leelos la grilla
        grilla = []
        for linea in partida:
            fila_actual = []
            for celda in linea.split(","):
                fila_actual.append(int(celda))
            grilla.append(fila_actual)
            print(fila_actual)

    return [pieza_actual, grilla, False, puntos]