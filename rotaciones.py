def cargar_rotaciones(ruta):
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

rotaciones = cargar_rotaciones("./piezas.txt.txt")
print(f"Hay {len(rotaciones)} piezas")

for rotacion in rotaciones:
    print(f"La rotacion actual tiene {len(rotacion)} posiciones")
    print(f"La rotacion actual es {rotacion}")