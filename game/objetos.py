import pygame
import random
import math
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
        self.amigos = {}  # Restaurar este atributo
        self.velocidad = Vector2(velocidad_x, velocidad_y)
        self.masa = masa
        self.es_principal = es_principal
        self.influencias = {}  # Diccionario de emociones y sus pesos
        self.id = random.randint(0, 1000000)
        self.surface = pygame.Surface((radio*2, radio*2), pygame.SRCALPHA) if es_principal else None  

    def dibujar(self, superficie):
        if self.es_principal:
            if not self.surface or self.surface.get_size() != (self.radio*2, self.radio*2):
                self.surface = pygame.Surface((self.radio*2, self.radio*2), pygame.SRCALPHA)
            
            self._actualizar_pastel()
            superficie.blit(self.surface, (int(self.posicion.x - self.radio), int(self.posicion.y - self.radio)))
            pygame.draw.circle(superficie, (200, 200, 200), (int(self.posicion.x), int(self.posicion.y)), self.radio + 5, 2)
        else:
            pygame.draw.circle(superficie, self.color_actual, (int(self.posicion.x), int(self.posicion.y)), self.radio)
    
    def _actualizar_pastel(self):
        self.surface = pygame.Surface((self.radio*2, self.radio*2), pygame.SRCALPHA)
        
        # Si no hay influencias, mostrar color base
        if not self.influencias:
            pygame.draw.circle(self.surface, self.color_original, (self.radio, self.radio), self.radio)
            return

        # 1. Contar el peso total por emoción
        pesos_emociones = {}
        for emocion, peso in self.influencias.items():
            if peso > 0:
                pesos_emociones[emocion] = pesos_emociones.get(emocion, 0) + peso

        # 2. Calcular peso total de todas las emociones
        peso_total = sum(pesos_emociones.values())
        if peso_total <= 0:
            pygame.draw.circle(self.surface, self.color_original, (self.radio, self.radio), self.radio)
            return

        # 3. Dibujar gráfico de pastel proporcional
        angulo_actual = 0
        for emocion, peso in sorted(pesos_emociones.items(), key=lambda x: -x[1]):
            color = EMOCIONES[emocion]["color"]
            angulo_segmento = 360 * (peso / peso_total)

            # Solo dibujar segmentos significativos (> 1 grado)
            if angulo_segmento >= 1:
                puntos = [(self.radio, self.radio)]  # Centro
                
                # Puntos del arco (60 puntos por segmento para suavidad)
                for i in range(61):
                    angulo = angulo_actual + (i * angulo_segmento / 60)
                    rad = math.radians(angulo)
                    puntos.append((
                        self.radio + self.radio * math.cos(rad),
                        self.radio + self.radio * math.sin(rad)
                    ))

                pygame.draw.polygon(self.surface, color, puntos)
                angulo_actual += angulo_segmento

        # Dibujar borde blanco para mejor visualización
        pygame.draw.circle(self.surface, (255, 255, 255), (self.radio, self.radio), self.radio, 2)
    def actualizar(self):
        if not self.es_principal:
            self.posicion += self.velocidad
        self.actualizar_color()

    def actualizar_color(self):
        if self.es_principal:
            # Reducir gradualmente todas las influencias
            for emocion in list(self.influencias.keys()):
                self.influencias[emocion] *= 0.97  # Decaimiento lento
                
                # Eliminar influencias insignificantes
                if self.influencias[emocion] < 0.01:
                    del self.influencias[emocion]
    def contaminar(self, otro_circulo):
        if self.es_principal:
            distancia = self.posicion.distance_to(otro_circulo.posicion)
            max_distancia = 250  # Radio máximo de influencia
            
            if distancia < max_distancia:
                # Identificar la emoción del círculo
                emocion = next((k for k, v in EMOCIONES.items() 
                            if v["color"] == otro_circulo.color_original), None)
                
                if emocion:
                    # Calcular factor de influencia basado en:
                    # 1. Distancia (inversamente proporcional)
                    # 2. Masa del círculo emocional
                    # 3. Radio del círculo emocional
                    factor = (1 - distancia/max_distancia) * otro_circulo.masa * (otro_circulo.radio/30)
                    
                    # Acumular influencia
                    self.influencias[emocion] = self.influencias.get(emocion, 0) + factor
    @classmethod
    def generar_emocion_aleatoria(cls, x, y, radio, vx=0, vy=0):
        emocion_nombre, emocion = random.choice(list(EMOCIONES.items()))
        circulo = cls(
            x, y, radio,
            emocion["masa"] * radio,
            emocion["color"]
        )
        circulo.velocidad = Vector2(vx, vy)
        return circulo