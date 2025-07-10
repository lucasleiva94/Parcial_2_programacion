import pygame 
from Constantes import *
from Menu import *
from Juego import *
from Configuracion import *
from Rankings import *
from Terminado import *

pygame.init()
pygame.display.set_caption("PREGUNTADOS 114")
icono = pygame.image.load("icono.png")
pygame.display.set_icon(icono)

pantalla = pygame.display.set_mode(PANTALLA)
corriendo = True
datos_juego = {

    "puntuacion": 0,
    "vidas": 3,
    "nombre": "",
    "tiempo_restante": TIEMPO_JUEGO,
    "tiempo_extra": 0,
    "volumen_musica": 50,
    "indice": 0,
    "volumen_error": 100,
    "volumen_click": 100,
    "comodin_X2": False,
    "opciones_visibles": [True, True, True, True],
    "doble_chance_activado": False,
    "doble_chance_usado": False

              }
mezclar_lista(lista_preguntas)
lista_rankings = []
reloj = pygame.time.Clock()
ventana_actual = "menu"
Flag_abierto = True
bandera_juego = False
bandera_rankings = False

while corriendo:
    reloj.tick(FPS)
    cola_eventos = pygame.event.get()
    
    if ventana_actual == "menu":
        ventana_actual = mostrar_menu(pantalla,cola_eventos)
    elif ventana_actual == "salir":
        corriendo = False
    if ventana_actual == "rankings":


        if bandera_rankings == False :
            partidas = leer_json()
            bandera_rankings = True

        ventana_actual = mostrar_rankings(pantalla, cola_eventos, partidas)

    elif ventana_actual == "menu":
        bandera_rankings = False


    elif ventana_actual == "ajustes":
        ventana_actual = mostrar_ajustes(pantalla,cola_eventos,datos_juego)
    elif ventana_actual == "juego":
        if bandera_juego == False:
            pygame.mixer.init()
            pygame.mixer.music.load("musica.mp3")
            porcentaje_musica = datos_juego["volumen_musica"] / 100
            pygame.mixer.music.set_volume(porcentaje_musica)
            pygame.mixer.music.play(-1)
            bandera_juego = True
        ventana_actual = mostrar_juego(pantalla,cola_eventos,datos_juego,lista_preguntas)
    elif ventana_actual == "terminado":
        if bandera_juego == True:
            bandera_juego = False
            pygame.mixer.music.stop()
        ventana_actual = mostrar_fin_juego(pantalla,cola_eventos,datos_juego)
        
    

    CLICK_SONIDO.set_volume(datos_juego["volumen_click"] / 100)
    ERROR_SONIDO.set_volume(datos_juego["volumen_error"] / 100)
    
    
    pygame.display.flip()

pygame.quit()