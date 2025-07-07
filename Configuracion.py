import pygame
from Constantes import *
from Funciones import *

pygame.init()

boton_suma = crear_elemento_juego("mas.webp",60,60,420,200)
boton_resta = crear_elemento_juego("menos.webp",60,60,20,200)
boton_volver = crear_elemento_juego("textura_respuesta.jpg",100,40,10,10)
boton_mute = crear_elemento_juego("mute.png",60,60,335,510)
fondo_pantalla = pygame.transform.scale(pygame.image.load("fondo_configuracion.jpg"),PANTALLA)

boton_suma_efecto = crear_elemento_juego("mas.webp",60,60,420,400)
boton_resta_efecto = crear_elemento_juego("menos.webp",60,60,20,400)




def mostrar_ajustes(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    retorno = "ajustes"
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.KEYDOWN:
            #QUE VUELVA AL MENU CUANDO TOCO LA TECLA ESC
            pass

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_suma["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] <= 95:
                        datos_juego["volumen_musica"] += 5
                        CLICK_SONIDO.play()
                    else:
                        ERROR_SONIDO.play()
                elif boton_resta["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] > 0:
                        datos_juego["volumen_musica"] -= 5
                        CLICK_SONIDO.play()
                    else: 
                        ERROR_SONIDO.play()
                elif boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"
                elif boton_mute["rectangulo"].collidepoint(evento.pos):
                    datos_juego["volumen_musica"] = 0
                    datos_juego["volumen_click"] = 0
                    datos_juego["volumen_error"] = 0


                elif boton_suma_efecto["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_error"] <= 95 and datos_juego["volumen_click"] <= 95:
                        datos_juego["volumen_error"] += 5
                        datos_juego["volumen_click"] += 5
                        CLICK_SONIDO.play()


                elif boton_resta_efecto["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_error"] > 0 and datos_juego["volumen_click"] > 0:
                        datos_juego["volumen_error"] -= 5
                        datos_juego["volumen_click"] -= 5
                        CLICK_SONIDO.play()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    print(f"Click en: {evento.pos}")
                        


    
    pantalla.blit(fondo_pantalla,(0,0))
    mostrar_texto(pantalla,f"Ajuste volumen de musica",(80,100),FUENTE_PREGUNTA,COLOR_NEGRO)
    mostrar_texto(pantalla,f"Ajuste volumen de efectos",(80,340),FUENTE_PREGUNTA,COLOR_NEGRO)
    mostrar_texto(pantalla,f"Silenciar todo:",(80,530),FUENTE_PREGUNTA,COLOR_NEGRO)

    
    pantalla.blit(boton_suma["superficie"],boton_suma["rectangulo"])
    pantalla.blit(boton_resta["superficie"],boton_resta["rectangulo"])
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    pantalla.blit(boton_mute["superficie"],boton_mute["rectangulo"])

    pantalla.blit(boton_suma_efecto["superficie"],boton_suma_efecto["rectangulo"])
    pantalla.blit(boton_resta_efecto["superficie"],boton_resta_efecto["rectangulo"])

    
    mostrar_texto(pantalla,f"{datos_juego['volumen_musica']} %",(200,200),FUENTE_VOLUMEN,COLOR_NEGRO)
    mostrar_texto(boton_volver["superficie"],"VOLVER",(5,5),FUENTE_RESPUESTA,COLOR_BLANCO)


    mostrar_texto(pantalla,f"{datos_juego['volumen_error']} %",(200,400),FUENTE_VOLUMEN,COLOR_NEGRO)

    return retorno
    