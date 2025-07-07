import pygame
from Constantes import *
from Funciones import *

pygame.init()

fuente = pygame.font.SysFont("Arial Narrow",40)
cuadro = crear_elemento_juego("textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON,125,245)
fondo_pantalla = pygame.transform.scale(pygame.image.load("fin_juego.jpg"),PANTALLA)

def mostrar_fin_juego(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    retorno = "terminado"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"

        elif evento.type == pygame.KEYDOWN:
            bloc_mayus = pygame.key.get_mods() and pygame.KMOD_CAPS
            letra_presionada = pygame.key.name(evento.key)

            if letra_presionada == "return" or letra_presionada == "kp_enter":
                if len(datos_juego["nombre"].strip()) >= 3:
                    guardar_partida(datos_juego["nombre"], datos_juego["puntuacion"])
                    retorno = "salir"
                else:
                    print("debe teer nas de 3 caracteres")
                    pygame.display.update()



            elif letra_presionada == "backspace" and len(datos_juego["nombre"]) > 0:
                datos_juego["nombre"] = datos_juego["nombre"][:-1]
                limpiar_superficie(cuadro, "textura_respuesta.jpg", 250, 50)

            elif letra_presionada == "space":
                datos_juego["nombre"] += " "

            elif len(letra_presionada) == 1:
                if letra_presionada.isalpha() or letra_presionada.isdigit():
                    if bloc_mayus != 0:
                        datos_juego["nombre"] += letra_presionada.upper()
                    else:
                        datos_juego["nombre"] += letra_presionada

        
        
    pantalla.blit(fondo_pantalla,(0,0))
    pantalla.blit(cuadro["superficie"],cuadro["rectangulo"])
    mostrar_texto(cuadro["superficie"],datos_juego["nombre"],(10,0),fuente,COLOR_BLANCO)
    mostrar_texto(pantalla,f"Usted obtuvo: {datos_juego['puntuacion']} puntos",(80,80),fuente,COLOR_NEGRO)
    mostrar_texto(pantalla,f"Ingrese su nombre para participar del ranking, el nombre debe ser mayor a 3 caracteres",(80,125),fuente,COLOR_NEGRO)
    
    return retorno
