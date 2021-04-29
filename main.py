import gamelib
import tetris

#Constantes de la ventana y del tamaño de la grilla
ANCHO_VENTANA, ALTO_VENTANA = 400, 400
GRILLA_ANCHO_PIXEL,GRILLA_ALTO_PIXEL = ANCHO_VENTANA // 2, ALTO_VENTANA

#Constantes de la siguiente pieza en la parte derecha de la pantalla
VENTANA_SIG_PIEZA_X, VENTANA_SIG_PIEZA_Y = (ANCHO_VENTANA // 2) + (ANCHO_VENTANA // 5), ALTO_VENTANA // 2

#Tamaño del tetris
ANCHO_CELDA, ALTO_CELDA = GRILLA_ANCHO_PIXEL // tetris.ANCHO_JUEGO, GRILLA_ALTO_PIXEL // tetris.ALTO_JUEGO

ESPERA_DESCENDER = 8

#Constante del ranking de puntuaciones
TOP_PUNTUACIONES = 10

#Constante de las acciones de las teclas
ACCION_ROTAR = "ROTAR"
ACCION_IZQ = "IZQUIERDA"
ACCION_DER = "DERECHA"
ACCION_DESCENDER = "DESCENDER"
ACCION_GUARDAR = "GUARDAR"
ACCION_CARGAR = "CARGAR"
ACCION_SALIR = "SALIR"

def dibujar_grilla():
    """Dibuja la grilla del tetris."""
    gamelib.draw_rectangle(0,0,GRILLA_ANCHO_PIXEL,GRILLA_ALTO_PIXEL,outline = "white",fill = "black")

    for x in range(0, GRILLA_ANCHO_PIXEL, ANCHO_CELDA):
        gamelib.draw_line(x,0,x,GRILLA_ALTO_PIXEL)
    for y in range(0, GRILLA_ALTO_PIXEL, ALTO_CELDA):
        gamelib.draw_line(0,y,GRILLA_ANCHO_PIXEL,y)

def dibujar_superficie_consolidada(juego):
    """Dibuja la superficie consolidada de cada pieza que colisione
    con esta."""
    ancho, alto = tetris.dimensiones(juego)

    for x in range(ancho):
        for y in range(alto):
            if tetris.celda_tiene_valor(juego, x, y, tetris.CELDA_SUPERFICIE):
                pixel_x, pixel_y = (x * ANCHO_CELDA, y * ALTO_CELDA)
                gamelib.draw_rectangle(pixel_x, pixel_y, pixel_x + ANCHO_CELDA, pixel_y + ALTO_CELDA,fill = "white")

def dibujar_puntuaciones(juego):
    """Dibuja la puntuacion, para ganar los puntos, se tienen
    que eliminar cada linea."""
    puntos = tetris.obtener_puntos(juego)
    gamelib.draw_text(f"Puntos:{puntos}", VENTANA_SIG_PIEZA_X + 10, VENTANA_SIG_PIEZA_Y - 100,fill = "red")

def dibujar_pieza(juego):
    """Dibuja la pieza que esta dentro de la grilla"""
    # Pieza es una tupla de tuplas con las posiciones de la pieza
    for x, y in tetris.pieza_actual(juego):
        pixel_x, pixel_y = (x * ANCHO_CELDA, y * ALTO_CELDA)
        gamelib.draw_rectangle(pixel_x, pixel_y, pixel_x + ANCHO_CELDA, pixel_y + ALTO_CELDA,fill = "red")

def dibujar_siguiente(pieza):
    """Dibuja la siguiente pieza en la parte derecha de la pantalla"""
    gamelib.draw_text("Sig. Pieza",VENTANA_SIG_PIEZA_X + 10, VENTANA_SIG_PIEZA_Y - 40,fill = "white")
    for x, y in pieza:
        pixel_x, pixel_y = (VENTANA_SIG_PIEZA_X + x * ANCHO_CELDA, (VENTANA_SIG_PIEZA_Y + 10) + y * ALTO_CELDA)
        gamelib.draw_rectangle(pixel_x, pixel_y, pixel_x + ANCHO_CELDA, pixel_y + ALTO_CELDA,fill = "red")

def cargar_config_teclas(ruta):
    """cargar_config_teclas, guarda cada tecla en un
    diccionario con la tecla como clave y su valor la accion"""
    dicc_teclas = {}
    with open(ruta,"r") as archivo:
        for linea in archivo:
            if (linea.strip() == ""):
                continue
            tecla, accion = linea.strip().split("=")
            tecla_sin_espacios = tecla.strip()
            if tecla_sin_espacios not in dicc_teclas:
                dicc_teclas[tecla_sin_espacios] = accion.strip()
    print(dicc_teclas)
    return dicc_teclas

def realizar_accion_tecla(juego, config, tecla, siguiente_pieza, piezas):
    """realizar_accion_teclas: verifica que la tecla este 
    en el diccionario si no esta, no hace nada pero si esta
    realiza su respectiva accion."""
    if not tecla in config:
        return (juego, False, False)
    accion = config[tecla]
    if accion == ACCION_IZQ:
        return (tetris.mover(juego, tetris.IZQUIERDA), False, False)
    elif accion == ACCION_DER:
        return (tetris.mover(juego,tetris.DERECHA), False, False)
    elif accion == ACCION_DESCENDER:
        nuevo_juego, cambiar_pieza = tetris.avanzar(juego, siguiente_pieza)
        return (nuevo_juego, cambiar_pieza, False)
    elif accion == ACCION_ROTAR:
        return (tetris.rotar(juego, piezas), False, False)
    elif accion == ACCION_GUARDAR:
        tetris.guardar_partida(juego, "./partida.txt")
        return (juego, False, False)
    elif accion == ACCION_CARGAR:
        return (tetris.cargar_partida("./partida.txt"), False, False)
    elif accion == ACCION_SALIR:
        return (juego, False, True)
    else:
        return (juego, False, False)

def cargar_rotaciones(ruta):
    """Carga cada una de las piezas, la pieza inicial y
    sus rotaciones"""
    # Lista de tuplas
    piezas = []

    with open(ruta,"r") as archivo:
        for linea in archivo:
            # Si la linea es vacia, no hacemos nada
            if (linea.strip() == ""):
                continue

            rotaciones, nombre = linea.strip().split("#") # rotaciones = "0,0;1,0;1,1;2,0 0,0;1,-1;1,0;1,1 0,0;1,-1;1,0;2,0 0,0;0,1;0,2;1,1 "

            # Obtenemos una lista con cada rotacion de la pieza actual
            lista_rotaciones = rotaciones.strip().split() # lista_rotaciones = ["0,0;1,0;1,1;2,0", "0,0;1,-1;1,0;1,1", ...]

            # Convertimos cada rotacion en una tupla de posiciones (tuplas)
            pieza_actual = []

            for posiciones_rotacion in lista_rotaciones:
                rotacion_actual = []
                posiciones = posiciones_rotacion.split(";")
                
                for posicion in posiciones:
                    x, y = posicion.split(",")
                    tupla_posicion = (int(x), int(y))
                    rotacion_actual.append(tupla_posicion)

                pieza_actual.append(tuple(rotacion_actual))
            
            piezas.append(tuple(pieza_actual))

    return tuple(piezas)

def cargar_puntuaciones(ruta):
    """Carga las puntuaciones del archivo. Las puntuaciones guarda
    tupla con puntos y nombres (puntos, nombres) y lo devuelve de menor a mayor"""
    puntuaciones = []

    with open(ruta,"r") as archivo:
        for linea in archivo:
            nombre, puntos = linea.rstrip().split(";")
            puntuaciones.append((int(puntos), nombre))
    
    return sorted(puntuaciones)

def guardar_puntuaciones(ruta, puntuaciones):
    """Guarda las puntuaciones en el archivo de forma nombre;puntuacion"""
    with open(ruta,"w") as archivo:
        for puntuacion, nombre in puntuaciones:
            archivo.write(f"{nombre};{puntuacion}\n")

def es_mejor_puntuacion(mejores_puntuaciones, puntuacion):
    if len(mejores_puntuaciones) < TOP_PUNTUACIONES:
        return True
    return puntuacion > mejores_puntuaciones[0][0]

def main():
    # Inicializar el estado del juego
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)
    teclas = cargar_config_teclas("./teclas.txt")
    piezas = cargar_rotaciones("./piezas.txt")
    mejores_puntuaciones = cargar_puntuaciones("./puntuaciones.txt")
    juego = tetris.crear_juego(tetris.generar_pieza(piezas))
    siguiente_pieza = tetris.generar_pieza(piezas)
    timer_bajar = ESPERA_DESCENDER
    juego_terminado = False
    
    while gamelib.loop(fps=30):
        if juego_terminado:
            break

        gamelib.draw_begin()
        # Dibujar la pantalla
        dibujar_grilla()
        dibujar_pieza(juego)
        dibujar_superficie_consolidada(juego)
        dibujar_puntuaciones(juego)
        dibujar_siguiente(siguiente_pieza)
        gamelib.draw_end()

        for event in gamelib.get_events():
            if not event:
                break
            if event.type == gamelib.EventType.KeyPress:
                tecla = event.key
                
              # Actualizar el juego, según la tecla presionada
                juego, cambiar_pieza, terminado = realizar_accion_tecla(juego, teclas, tecla, siguiente_pieza, piezas)
                juego_terminado = terminado

                if cambiar_pieza:
                    siguiente_pieza = tetris.generar_pieza(piezas)

        timer_bajar -= 1
        if timer_bajar == 0:
            timer_bajar = ESPERA_DESCENDER
            # Descender la pieza automáticamente
            juego, cambiar_pieza = tetris.avanzar(juego, siguiente_pieza)
            juego_terminado = tetris.terminado(juego)
            
            if cambiar_pieza:
                siguiente_pieza = tetris.generar_pieza(piezas)

    # Termino el juego
    puntuacion = tetris.obtener_puntos(juego)
    if es_mejor_puntuacion(mejores_puntuaciones, puntuacion):
        nombre = gamelib.input(f"Ha ingresado al top {TOP_PUNTUACIONES}. Ingrese su nombre:")

        if nombre:
            mejores_puntuaciones.append((puntuacion, nombre))
            print(mejores_puntuaciones)
            guardar_puntuaciones("./puntuaciones.txt", sorted(mejores_puntuaciones, reverse=True)[:TOP_PUNTUACIONES])

gamelib.init(main)