from math import sqrt
from pygame.math import Vector2

def aplicar_resorte(circulo1, circulo2, k=0.1, longitud_reposo=100):
    direccion = circulo2.posicion - circulo1.posicion
    distancia = direccion.length()

    if distancia == 0:
        return
    elongacion = distancia - longitud_reposo
    direccion_normalizada = direccion.normalize()
    fuerza = direccion_normalizada * (k * elongacion)
    circulo1.velocidad += fuerza

# def aplicar_gravedad(circulo1, circulo2, G=1):
#     direccion = circulo2.posicion - circulo1.posicion
#     distancia = direccion.length()

#     if distancia < 5:
#         return

#     fuerza_magnitud = G * circulo1.masa * circulo2.masa / (distancia**2)
#     circulo1.velocidad += direccion.normalize() * fuerza_magnitud / circulo1.masa
def aplicar_gravedad(circulo1, circulo2, G=0.5):
    if circulo1.es_principal and circulo2.es_principal:
        return
    
    direccion = circulo2.posicion - circulo1.posicion
    distancia = max(direccion.length(), 10)  # Evitar división por cero
    
    fuerza = direccion.normalize() * (G * circulo1.masa * circulo2.masa / (distancia**2))
    
    if not circulo1.es_principal:
        circulo1.velocidad += fuerza / circulo1.masa
    if not circulo2.es_principal:
        circulo2.velocidad -= fuerza / circulo2.masa
def aplicar_resorte_con_amortiguamiento(circulo1, circulo2, k=0.1, longitud_reposo=100, b=0.05, max_range=250):
    direccion = circulo2.posicion - circulo1.posicion
    distancia = direccion.length()

    if distancia > max_range or distancia == 0:
        return

    direccion_normalizada = direccion.normalize()
    fuerza_resorte = direccion_normalizada * (k * (distancia - longitud_reposo))
    
    velocidad_relativa = circulo2.velocidad - circulo1.velocidad
    fuerza_amortiguamiento = b * velocidad_relativa.dot(direccion_normalizada) * direccion_normalizada

    fuerza_total = fuerza_resorte + fuerza_amortiguamiento
    circulo1.velocidad += fuerza_total / circulo1.masa
    circulo2.velocidad -= fuerza_total / circulo2.masa

    # Eliminar la parte que usa 'amigos' ya que no es necesaria para la física
    if distancia < longitud_reposo * 1.2:
        # Solo mezcla de colores si están cerca
        peso = min(0.5, 0.1 * 0.1)  # Pequeño factor fijo para mezcla
        if not circulo1.es_principal and not circulo2.es_principal:
            for circ in [circulo1, circulo2]:
                amigo = circulo2 if circ == circulo1 else circulo1
                circ.color_actual = tuple(
                    int(circ.color_original[i] * (1-peso) + amigo.color_original[i] * peso)
                    for i in range(3)
                )
def aplicar_interaccion(circulo1, circulo2, umbral=50):
    distancia = (circulo2.posicion - circulo1.posicion).length()
    if distancia < umbral:
        circulo1.contaminar(circulo2)
        circulo2.contaminar(circulo1)