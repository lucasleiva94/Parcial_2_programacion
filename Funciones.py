import random
from Constantes import *
import pygame
import csv
import os
import json
from datetime import datetime

def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def crear_elemento_juego(textura:str,ancho:int,alto:int,pos_x:int,pos_y:int) -> dict:
    """Se encarga de crear un elemento en el juego guardando su superficie (textura) y su rectangulo (comportamiento) 

    Args:
        textura (str): Tiene que ser una ruta ya sea relativa o absoluta
        ancho (int): En pixeles el ancho de ese elemento
        alto (int): En pixeles el alto de ese elemento
        pos_x (int): Donde se va a ubicar en el eje x
        pos_y (int): Donde se va a ubicar en el eje y

    Returns:
        dict: El diccionario con el elemento creado
    """
    elemento_juego = {}
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura),(ancho,alto))
    elemento_juego["rectangulo"] = pygame.Rect(pos_x,pos_y,ancho,alto)
    
    return elemento_juego

def crear_lista_respuestas(textura:str,ancho:int,alto:int,pos_x:int,pos_y:int):
    lista_respuestas = []

    for i in range(4):
        respuesta = crear_elemento_juego(textura,ancho,alto,pos_x,pos_y)
        lista_respuestas.append(respuesta)
        pos_y += 80    
        
    return lista_respuestas

def crear_botones_menu() -> list:
    lista_botones = []
    pos_x = 125
    pos_y = 115

    for i in range(4):
        boton = crear_elemento_juego("textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON,pos_x,pos_y)
        pos_y += 80
        lista_botones.append(boton)
    
    return lista_botones

def limpiar_superficie(elemento_juego:dict,textura:str,ancho:int,alto:int):
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura),(ancho,alto))

def verificar_respuesta(datos_juego:dict,pregunta_actual:dict,respuesta:int) -> bool:
    
    if int(pregunta_actual["respuesta_correcta"]) == respuesta:
        datos_juego["puntuacion"] += PUNTUACION_ACIERTO   
        retorno = True         
    else:
        datos_juego["puntuacion"] -= PUNTUACION_ERROR
        datos_juego["vidas"] -= 1
        retorno = False
    return retorno

def reiniciar_estadisticas(datos_juego:dict):
    datos_juego["vidas"] = CANTIDAD_VIDAS
    datos_juego["puntuacion"] = 0
    datos_juego["nombre"] = ""
    datos_juego["tiempo_restante"] = TIEMPO_JUEGO

def pasar_pregunta(lista_preguntas:list,indice:int,cuadro_pregunta:dict,lista_respuestas:list) -> dict:
    pregunta_actual = lista_preguntas[indice]
    limpiar_superficie(cuadro_pregunta,"textura_pregunta.jpg",ANCHO_PREGUNTA,ALTO_PREGUNTA)
    for i in range(len(lista_respuestas)):
        limpiar_superficie(lista_respuestas[i],"textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON)
    
    return pregunta_actual

def mezclar_lista(lista_preguntas:list) -> None:
    random.shuffle(lista_preguntas)

def cargar_preguntas(nombre_archivo):
    lista_preguntas = []
    with open(nombre_archivo, mode='r', encoding='utf-8-sig') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            lista_preguntas.append(dict(fila))  # Cada fila es un diccionario
            
    return lista_preguntas



def guardar_partida(nombre, puntaje, ruta_json="partidas.json"):
    """
    Guarda los datos de una partida en un archivo .json
    args: 
    nombre(str):recibe el nombre del jugador
    puntaje(int):puntaje obtenido
    ruta_json(str): ruta al archivo .json donde vamos a guardar la partida.
    """
    partidas = []
    if os.path.exists(ruta_json):
        with open(ruta_json, "r", encoding="utf-8-sig") as archivo:
            contenido = archivo.read().strip()
            if contenido != "":
                partidas = json.loads(contenido)

    nueva_partida = {
        "nombre": nombre,
        "puntaje": puntaje,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    partidas.append(nueva_partida)

    with open(ruta_json, "w", encoding="utf-8") as archivo:
        json.dump(partidas, archivo, indent=4, ensure_ascii=False)


def ordenar_por_puntaje(lista: list) -> None:
    n = len(lista)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if lista[j]["puntaje"] < lista[j + 1]["puntaje"]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

