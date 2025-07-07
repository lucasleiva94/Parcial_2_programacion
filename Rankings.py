import pygame
from Constantes import *
from Funciones import *
import json

pygame.init()

boton_volver = crear_elemento_juego("textura_respuesta.jpg",100,40,10,10)
fondo_pantalla = pygame.transform.scale(pygame.image.load("fondo_festejo.jpg"),PANTALLA)


def mostrar_rankings(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event]) -> str:
    retorno = "rankings"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"
    
    pantalla.blit(fondo_pantalla,(0,0))
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])

    with open("partidas.json", "r", encoding="utf-8") as archivo:
        partidas = json.load(archivo)
        ordenar_por_puntaje(partidas)

    mostrar_texto(pantalla,f"TOP 10:",(80,200),FUENTE_VOLUMEN,COLOR_NEGRO)
    pos_y = 250
    for jugador in partidas[:10]:
        texto = f"{jugador['nombre']} : {jugador['puntaje']}" + " puntos"
        mostrar_texto(pantalla, texto, (80, pos_y), FUENTE_PREGUNTA, COLOR_NEGRO)
        pos_y += 35 


    mostrar_texto(boton_volver["superficie"],"VOLVER",(5,5),FUENTE_RESPUESTA,COLOR_BLANCO)
    
    return retorno
    