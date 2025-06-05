import pygame
import sys
import random
from game.objetos import Circulo, EMOCIONES  # Asegúrate de importar EMOCIONES desde objetos
from game.crearCirculo import crear_circulo_emocion
from game.funciones import aplicar_gravedad, aplicar_resorte_con_amortiguamiento

# Inicialización
pygame.init()
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Sistema de Emociones Interactivo")

# Círculo central
circulo_central = Circulo(ANCHO//2, ALTO//2, 30, 1000, (255, 255, 255), es_principal=True)
circulos = [circulo_central]

# Configuración
fuente = pygame.font.SysFont('Arial', 16)
reloj = pygame.time.Clock()

# Diccionario de emociones mapeadas a teclas
teclas_emociones = {
    pygame.K_1: "alegria",
    pygame.K_2: "tristeza",
    pygame.K_3: "ira",
    pygame.K_4: "miedo",
    pygame.K_5: "desagrado"
}

# Círculos sin gravedad (flotantes)
circulos_flotantes = set()

while True:
    for evento in pygame.event.get():
        
        if evento.type == pygame.KEYDOWN:
            print(evento.key)  # Imprimir la tecla presionada
            # Crear emociones con teclas 1-5
            if evento.key in teclas_emociones:
                emocion_nombre = teclas_emociones[evento.key]
                emocion = EMOCIONES[emocion_nombre]
                nuevo = crear_circulo_emocion(ANCHO, ALTO, emocion)
                circulos.append(nuevo)
                print(f"Emoción {emocion_nombre} creada")
            
            # Tecla F para hacer flotar un círculo aleatorio
            elif evento.key == pygame.K_f:
                if len(circulos) > 1:  # Excluye al protagonista
                    flotante = random.choice([c for c in circulos if not c.es_principal])
                    circulos_flotantes.add(flotante.id)
                    print(f"Círculo {flotante.id} ahora es flotante")
            
            # Tecla D para debug
            elif evento.key == pygame.K_d:
                debug_mode = not debug_mode
            
            elif evento.key == 27:
                print("Apagando el juego...")
                pygame.quit()
                sys.exit()


    ventana.fill((0, 0, 0))

    # Física e interacciones
    for i in range(1, len(circulos)):
        # Solo aplicar fuerzas si no es flotante
        if circulos[i].id not in circulos_flotantes:
            for j in range(i+1, len(circulos)):
                if circulos[j].id not in circulos_flotantes:
                    aplicar_gravedad(circulos[i], circulos[j], G=2)
                    aplicar_resorte_con_amortiguamiento(
                        circulos[i], circulos[j],
                        k=0.005,
                        longitud_reposo=150,
                        b=0.02,
                        max_range=300
                    )
            
            # Atracción al centro (solo para no flotantes)
            distancia = circulo_central.posicion.distance_to(circulos[i].posicion)
            if distancia > 0:
                fuerza_centro = (circulo_central.posicion - circulos[i].posicion).normalize() * (distancia * 0.0005)
                circulos[i].velocidad += fuerza_centro
        
        # Contaminación emocional (siempre aplica)
        if circulo_central.posicion.distance_to(circulos[i].posicion) < 250:
            circulo_central.contaminar(circulos[i])

    # Actualizar y dibujar
    for circ in circulos:
        circ.actualizar()
        circ.dibujar(ventana)
        
        # Marcar círculos flotantes con un borde rojo
        if circ.id in circulos_flotantes:
            pygame.draw.circle(ventana, (255, 0, 0), (int(circ.posicion.x), int(circ.posicion.y)), circ.radio + 3, 2)
            if circ.posicion.x < 0 or circ.posicion.x > ANCHO or circ.posicion.y < 0 or circ.posicion.y > ALTO:
                # Si un círculo flotante sale de la pantalla, lo eliminamos
                circulos_flotantes.remove(circ.id)
                # y lo eliminamos de la lista de círculos
                circulos = [c for c in circulos if c.id != circ.id]

    # Info en pantalla
    info_texto = [
        "Controles:",
        "1-5: Crear emociones",
        "F: Hacer flotar aleatorio",
        f"Círculos: {len(circulos)}",
        f"Flotantes: {len(circulos_flotantes)}"
    ]
    
    for i, texto in enumerate(info_texto):
        render = fuente.render(texto, True, (255, 255, 255))
        ventana.blit(render, (10, 10 + i*20))

    pygame.display.flip()
    reloj.tick(60)