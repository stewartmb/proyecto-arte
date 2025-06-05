import pygame
import random
from pygame.math import Vector2, Vector3


EMOCIONES = {
    "alegria": {"color": (255, 255, 0), "masa": 1.0},
    "tristeza": {"color": (100, 150, 255), "masa": 1.2},
    "ira": {"color": (255, 50, 50), "masa": 1.5},
    "miedo": {"color": (150, 50, 255), "masa": 0.8},
    "desagrado": {"color": (150, 255, 50), "masa": 1.1}
}

class Circulo:
    def __init__(self, x, y, radio, masa, color, es_principal=False, velocidad_x=0, velocidad_y=0):
        self.posicion = Vector2(x, y)
        self.radio = radio
        self.color_original = color
        self.color_actual = color
        self.velocidad = Vector2(velocidad_x, velocidad_y)  # Cambiado a velocidad_x/y
        self.masa = masa
        self.es_principal = es_principal
        self.contaminacion = Vector3(0, 0, 0)
        self.amigos = {}
        self.id = random.randint(0, 1000000)


    def dibujar(self, superficie):
        pygame.draw.circle(superficie, self.color_actual, (int(self.posicion.x), int(self.posicion.y)), self.radio)
        if self.es_principal:
            pygame.draw.circle(superficie, (200, 200, 200), (int(self.posicion.x), int(self.posicion.y)), self.radio + 5, 2)

    def actualizar(self):
        if not self.es_principal:
            self.posicion += self.velocidad
        self.actualizar_color()

    def actualizar_color(self):
        if self.es_principal:
            # Suavizar la contaminación
            self.contaminacion *= 0.95
            # Mezclar con color original
            self.color_actual = (
                min(255, int(self.color_original[0] + self.contaminacion.x)),
                min(255, int(self.color_original[1] + self.contaminacion.y)),
                min(255, int(self.color_original[2] + self.contaminacion.z))
            )

    def contaminar(self, otro_circulo):
        if self.es_principal:
            distancia = self.posicion.distance_to(otro_circulo.posicion)
            if distancia < 200:
                factor = (1 - distancia/200) * 0.1
                self.contaminacion += Vector3(
                    (otro_circulo.color_original[0] - self.color_original[0]) * factor,
                    (otro_circulo.color_original[1] - self.color_original[1]) * factor,
                    (otro_circulo.color_original[2] - self.color_original[2]) * factor
                )
        # elif otro_circulo.es_principal:
        #     factor = self.masa * 0.05
        #     self.color_actual = (
        #         min(255, int(self.color_original[0] + (255 - self.color_original[0]) * factor)),
        #         min(255, int(self.color_original[1] + (255 - self.color_original[1]) * factor)),
        #         min(255, int(self.color_original[2] + (255 - self.color_original[2]) * factor))
        #     )

    @classmethod
    def generar_emocion_aleatoria(cls, x, y, radio, vx=0, vy=0):
        emocion = random.choice(list(cls.EMOCIONES.values()))
        circulo = cls(
            x, y, radio,
            emocion["masa"] * radio,
            emocion["color"]
        )
        circulo.velocidad = Vector2(vx, vy)
        return circulo