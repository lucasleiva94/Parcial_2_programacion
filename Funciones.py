import random
from Constantes import *
import pygame
import csv
import os
import json
from datetime import datetime

def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')):

    """
    Dibuja texto multilínea sobre una superficie, ajustando automáticamente las líneas si exceden el ancho.

    Args:
        surface (pygame.Surface): Superficie sobre la que se va a renderizar el texto.
        text (str): Texto a mostrar. 
        pos (tuple): Posición (x, y) inicial del texto.
        font (pygame.font.Font): Fuente a utilizar.
        color (pygame.Color, optional): Color del texto. Por defecto es negro.
    """

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

def crear_elemento_juego(textura:str, ancho:int, alto:int, pos_x:int, pos_y:int) -> dict:
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

def crear_lista_respuestas(textura:str,ancho:int,alto:int,pos_x:int,pos_y:int) -> list:
    """
    Crea una lista de 4 botones para respuestas, dispuestos verticalmente.

    Args:
        textura (str): Ruta a la textura de los botones.
        ancho (int): Ancho de cada botón.
        alto (int): Alto de cada botón.
        pos_x (int): Coordenada X inicial.
        pos_y (int): Coordenada Y inicial.

    Returns:
        list: Lista de diccionarios, cada uno con un botón.
    """
    lista_respuestas = []

    for i in range(4):
        respuesta = crear_elemento_juego(textura,ancho,alto,pos_x,pos_y)
        lista_respuestas.append(respuesta)
        pos_y += 80    
        
    return lista_respuestas

def crear_botones_menu() -> list:
    """
    Crea 4 botones que simulan un menú, posicionados verticalmente.

    Returns:
        list: Lista con los botones creados (diccionarios).
    """
    lista_botones = []
    pos_x = 125
    pos_y = 115

    for i in range(4):
        boton = crear_elemento_juego("textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON,pos_x,pos_y)
        pos_y += 80
        lista_botones.append(boton)
    
    return lista_botones

def limpiar_superficie(elemento_juego:dict, textura:str, ancho:int, alto:int) -> None:
    """
    Reasigna la textura de un elemento del juego.

    Args:
        elemento_juego (dict): Elemento a actualizar.
        textura (str): Ruta a la nueva textura.
        ancho (int): Ancho de la textura.
        alto (int): Alto de la textura.
    """
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura),(ancho,alto))

def verificar_respuesta(datos_juego:dict, pregunta_actual:dict, respuesta:int) -> bool:
    """
    Verifica si la respuesta seleccionada es correcta y actualiza puntaje y vidas.

    Args:
        datos_juego (dict): Estadísticas del juego (vidas, puntuación, etc.).
        pregunta_actual (dict): Pregunta actual con la respuesta correcta.
        respuesta (int): Número de respuesta elegida.

    Returns:
        bool: True si la respuesta es correcta, False si es incorrecta.
    """
    
    if int(pregunta_actual["respuesta_correcta"]) == respuesta:
        datos_juego["puntuacion"] += PUNTUACION_ACIERTO   
        retorno = True         
    else:
        retorno = False
    return retorno

def reiniciar_estadisticas(datos_juego:dict) -> None:
    """
    Reinicia las estadísticas del jugador al comenzar una nueva partida.

    Args:
        datos_juego (dict): Diccionario donde se guardan las estadísticas.
    """
    datos_juego["vidas"] = CANTIDAD_VIDAS
    datos_juego["puntuacion"] = 0
    datos_juego["nombre"] = ""
    datos_juego["tiempo_restante"] = TIEMPO_JUEGO

def pasar_pregunta(lista_preguntas:list, indice:int, cuadro_pregunta:dict, lista_respuestas:list,) -> dict:
    """
    Limpia las texturas y devuelve la siguiente pregunta.

    Args:
        lista_preguntas (list): Lista de preguntas.
        indice (int): Índice de la pregunta actual.
        cuadro_pregunta (dict): Superficie donde se muestra la pregunta.
        lista_respuestas (list): Lista de botones de respuestas.

    Returns:
        dict: Pregunta correspondiente al índice actual.
    """
    pregunta_actual = lista_preguntas[indice]
    limpiar_superficie(cuadro_pregunta,"textura_pregunta.jpg",ANCHO_PREGUNTA,ALTO_PREGUNTA)
    for i in range(len(lista_respuestas)):
        limpiar_superficie(lista_respuestas[i],"textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON)
    
    
    return pregunta_actual

def mezclar_lista(lista_preguntas:list) -> None:
    """
    Mezcla aleatoriamente la lista de preguntas.

    Args:
        lista_preguntas (list): Lista a mezclar.
    """
    random.shuffle(lista_preguntas)

def cargar_preguntas(nombre_archivo:str) -> dict:
    """
    Carga preguntas desde un archivo CSV y las devuelve como una lista de diccionarios.

    Args:
        nombre_archivo (str): Ruta al archivo CSV.

    Returns:
        list: Lista de preguntas, cada una representada como un diccionario.
    """
    lista_preguntas = []
    with open(nombre_archivo, mode='r', encoding='utf-8-sig') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            lista_preguntas.append(dict(fila))
            
    return lista_preguntas



def guardar_partida(nombre:str, puntaje:int, ruta_json="partidas.json"):
    """
    Guarda el nombre, puntaje y fecha de una partida en un archivo JSON.

    Args:
        nombre (str): Nombre del jugador.
        puntaje (int): Puntaje final.
        ruta_json (str, optional): Ruta del archivo JSON donde se guarda la información.
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


def ordenar_por_puntaje(lista:list) -> None:
    """
    Ordena una lista de diccionarios por la clave 'puntaje' de mayor a menor.

    Args:
        lista (list): Lista de diccionarios con la clave 'puntaje'.
    """
    n = len(lista)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if lista[j]["puntaje"] < lista[j + 1]["puntaje"]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

def crear_botones_comodin_menu() -> list:
    """
    Crea botones para seleccionar los comodines en el menú, posicionados verticalmente.

    Returns:
        list: Lista de botones creados (diccionarios).
    """
    lista_botones_comodin = []
    pos_x = 10
    pos_y = 250

    for i in range(4):
        boton = crear_elemento_juego("textura_respuesta.jpg",100,50,pos_x,pos_y)
        pos_y += 70
        lista_botones_comodin.append(boton)
    
    return lista_botones_comodin

def crear_lista_comodin(textura:str, ancho:int, alto:int, pos_x:int, pos_y:int) -> list:
    """
    Crea una lista de botones de comodines.

    Args:
        textura (str): Ruta a la textura de cada botón.
        ancho (int): Ancho de cada botón.
        alto (int): Alto de cada botón.
        pos_x (int): Coordenada X inicial.
        pos_y (int): Coordenada Y inicial.

    Returns:
        list: Lista de botones comodín.
    """
    lista_comodin = []

    for i in range(4):
        respuesta = crear_elemento_juego(textura,ancho,alto,pos_x,pos_y)
        lista_comodin.append(respuesta)
        pos_y += 80    
        
    return lista_comodin

lista_preguntas = cargar_preguntas("preguntas.csv")

def leer_json() -> dict:
    """
    Lee un archivo json y las ordena por puntaje de mayor a menor

    """
    with open("partidas.json", "r", encoding="utf-8") as archivo:
        partidas = json.load(archivo)
        ordenar_por_puntaje(partidas)

    return partidas


