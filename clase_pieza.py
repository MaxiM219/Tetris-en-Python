class Pieza:
    def __init__(self, rotaciones):
        self.rotaciones = rotaciones
        self.rotacion_actual = 0

    def rotar(self):
        self.rotacion_actual = (self.rotacion_actual + 1) % len(self.rotaciones)

    def rotacion_actual(self):
        return self.rotaciones[self.rotacion_actual]
