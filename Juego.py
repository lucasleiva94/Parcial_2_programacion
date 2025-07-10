import pygame 
from Constantes import *
from Funciones import *

pygame.init()

comodines_usados = {
"BOTON_BOMBA": False,
"BOTON_X2": False,
"BOTON_DOBLE_CHANCE": False,
"BOTON_PASAR": False

}
fondo_pantalla = pygame.transform.scale(pygame.image.load("fondo.jpg"),PANTALLA)
cuadro_pregunta = crear_elemento_juego("textura_pregunta.jpg",ANCHO_PREGUNTA,ALTO_PREGUNTA,80,80)
lista_respuestas = crear_lista_respuestas("textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON,125,245)
cuadro_comdin = crear_elemento_juego("textura_pregunta.jpg",ANCHO_BOTON,ALTO_BOTON,80,80)
lista_comodin = crear_lista_comodin("textura_respuesta.jpg",110,60,10,245)


evento_tiempo = pygame.USEREVENT 
pygame.time.set_timer(evento_tiempo,1000)    


def mostrar_juego(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict,lista_preguntas:list,) -> str:
    retorno = "juego"
    pregunta_actual = lista_preguntas[datos_juego["indice"]]
    
    if datos_juego["vidas"] == 0 or datos_juego["tiempo_restante"] == 0:
        print("GAME OVER")
        retorno = "terminado"
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == evento_tiempo:
            datos_juego["tiempo_restante"] -= 1
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                for i in range(len(lista_comodin)):
                    if lista_comodin[i]["rectangulo"].collidepoint(evento.pos):

                        if i == 1 and not comodines_usados["BOTON_BOMBA"]:
                            CLICK_SONIDO.play()                        
                            comodines_usados["BOTON_BOMBA"] = True

                            correcta = int(pregunta_actual["respuesta_correcta"]) - 1
                            opciones_incorrectas = [j for j in range(4) if j != correcta]

                            datos_juego["opciones_visibles"][opciones_incorrectas[0]] = False
                            datos_juego["opciones_visibles"][opciones_incorrectas[1]] = False




                        elif i == 0 and comodines_usados ["BOTON_X2"] == False :
                            CLICK_SONIDO.play()
                            datos_juego["comodin_X2"] = True


                            
                            comodines_usados ["BOTON_X2"] = True
                            
                        elif i == 3 and comodines_usados ["BOTON_PASAR"] == False :

                            mezclar_lista(lista_preguntas)
                            CLICK_SONIDO.play()
                            pregunta_actual = pasar_pregunta(lista_preguntas,datos_juego["indice"],cuadro_pregunta,lista_respuestas)
                            comodines_usados ["BOTON_PASAR"] = True

                        elif i == 2 and comodines_usados ["BOTON_DOBLE_CHANCE"] == False :
                            CLICK_SONIDO.play()
                            comodines_usados["BOTON_DOBLE_CHANCE"] = True
                            datos_juego["doble_chance_activado"] = True
                            datos_juego["doble_chance_usado"] = False


                        
                for i in range(len(lista_respuestas)):
                    if lista_respuestas[i]["rectangulo"].collidepoint(evento.pos):
                        respuesta = (i + 1)
                        if verificar_respuesta(datos_juego, pregunta_actual, respuesta):
                            CLICK_SONIDO.play()
                            if datos_juego.get("comodin_X2", False):
                                verificar_respuesta(datos_juego, pregunta_actual, respuesta)
                                datos_juego["comodin_X2"] = False
                
                            datos_juego["tiempo_extra"] += 1
                            datos_juego["doble_chance_activado"] = False
                
                            if datos_juego["tiempo_extra"] == 5:
                                datos_juego["tiempo_restante"] += 30
                                datos_juego["tiempo_extra"] = 0
                
                            datos_juego["indice"] += 1
                            if datos_juego["indice"] >= len(lista_preguntas):
                                datos_juego["indice"] = 0
                                mezclar_lista(lista_preguntas)
                
                            pregunta_actual = pasar_pregunta(lista_preguntas, datos_juego["indice"], cuadro_pregunta, lista_respuestas)
                            datos_juego["opciones_visibles"] = [True, True, True, True]
                
                        else:
                            ERROR_SONIDO.play()
                            datos_juego["tiempo_extra"] = 0
                

                            if datos_juego["doble_chance_activado"] == True and datos_juego["doble_chance_usado"] == False:
                                datos_juego["opciones_visibles"][respuesta - 1] = False
                                datos_juego["doble_chance_usado"] = True
                
                            else:
                                datos_juego["vidas"] -= 1
                                datos_juego["puntuacion"] -= PUNTUACION_ERROR

                
                                datos_juego["indice"] += 1
                                if datos_juego["indice"] >= len(lista_preguntas):
                                    datos_juego["indice"] = 0
                                    mezclar_lista(lista_preguntas)
                
                                pregunta_actual = pasar_pregunta(lista_preguntas, datos_juego["indice"], cuadro_pregunta, lista_respuestas)
                                datos_juego["opciones_visibles"] = [True, True, True, True]


                                        
    
    pantalla.blit(fondo_pantalla,(0,0))
    pantalla.blit(cuadro_pregunta["superficie"],cuadro_pregunta["rectangulo"])
    mostrar_texto(cuadro_pregunta["superficie"], pregunta_actual["pregunta"], (15, 15), FUENTE_PREGUNTA, COLOR_NEGRO)

    

    if not comodines_usados["BOTON_X2"]:
        pantalla.blit(lista_comodin[0]["superficie"], lista_comodin[0]["rectangulo"])
        mostrar_texto(lista_comodin[0]["superficie"], "X2", (5, 5), FUENTE_TEXTO, COLOR_BLANCO)

    if not comodines_usados["BOTON_BOMBA"]:
        pantalla.blit(lista_comodin[1]["superficie"], lista_comodin[1]["rectangulo"])
        mostrar_texto(lista_comodin[1]["superficie"], "BOMBA", (5, 5), FUENTE_TEXTO, COLOR_BLANCO)

    if not comodines_usados["BOTON_DOBLE_CHANCE"]:
        pantalla.blit(lista_comodin[2]["superficie"], lista_comodin[2]["rectangulo"])
        mostrar_texto(lista_comodin[2]["superficie"], "DOBLE CHANCE", (-2, -1), FUENTE_TEXTO, COLOR_BLANCO)

    if not comodines_usados["BOTON_PASAR"]:
        pantalla.blit(lista_comodin[3]["superficie"], lista_comodin[3]["rectangulo"])
        mostrar_texto(lista_comodin[3]["superficie"], "PASAR", (5, 5), FUENTE_TEXTO, COLOR_BLANCO)






    for i in range(len(lista_respuestas)):
        if datos_juego["opciones_visibles"][i] == True:
            pantalla.blit(lista_respuestas[i]["superficie"], lista_respuestas[i]["rectangulo"])
            mostrar_texto(lista_respuestas[i]["superficie"], pregunta_actual[f"respuesta_{i + 1}"], (15, 15), FUENTE_RESPUESTA, COLOR_BLANCO)




    mostrar_texto(pantalla,f"VIDAS: {datos_juego['vidas']}",(10,10),FUENTE_TEXTO,COLOR_NEGRO)
    mostrar_texto(pantalla,f"PUNTUACION: {datos_juego['puntuacion']}",(10,40),FUENTE_TEXTO,COLOR_NEGRO)
    mostrar_texto(pantalla,f"TIEMPO: {datos_juego['tiempo_restante']} seg",(275,10),FUENTE_TEXTO,COLOR_NEGRO)


    
    
    return retorno