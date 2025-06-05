import random
from game.objetos import Circulo, EMOCIONES

def crear_circulo_emocion(ancho_ventana, alto_ventana, emocion, radio=30):
    lado = random.randint(0, 3)
    velocidad_min, velocidad_max = 1, 3

    if lado == 0:  # Izquierda
        x, y = -radio, random.randint(0, alto_ventana)
        vx, vy = random.uniform(velocidad_min, velocidad_max), random.uniform(-velocidad_max, velocidad_max)
    elif lado == 1:  # Derecha
        x, y = ancho_ventana + radio, random.randint(0, alto_ventana)
        vx, vy = -random.uniform(velocidad_min, velocidad_max), random.uniform(-velocidad_max, velocidad_max)
    elif lado == 2:  # Arriba
        x, y = random.randint(0, ancho_ventana), -radio
        vx, vy = random.uniform(-velocidad_max, velocidad_max), random.uniform(velocidad_min, velocidad_max)
    else:  # Abajo
        x, y = random.randint(0, ancho_ventana), alto_ventana + radio
        vx, vy = random.uniform(-velocidad_max, velocidad_max), -random.uniform(velocidad_min, velocidad_max)

    return Circulo(
        x=x, 
        y=y, 
        radio=radio, 
        masa=emocion["masa"] * radio, 
        color=emocion["color"],
        velocidad_x=vx,  # Cambiado a velocidad_x
        velocidad_y=vy   # Cambiado a velocidad_y
    )