import argparse
import sys
sys.path.append('./src')  # Donde 'subcarpeta' es la carpeta donde está tu proxy.py

import re
from src.get_qa import *
from src.get_discussions import *
import logging

def main():

    #logging.basicConfig(filename='app.log', level=logging.DEBUG)
    logging.basicConfig( level=logging.DEBUG)
    logger = logging.getLogger()

    url = "https://www.examtopics.com/discussions/microsoft/"
    cert = "DP-700"
    
    logger.info(f"Iniciando recuperacion de pregutnas de {cert} desde {url}")
  
    discussion_list = get_discussions( url, cert, logger)
    ##ordeno para recuperar por id, que entiendo será de mas reciente a mas antiguo
    print(discussion_list)
    discussion_list.sort(reverse=True)
    print(discussion_list)
    
    logger.info(f"Recuperadas {len(discussion_list)} discusiones")
    
    #salvamos las preguntas a archivo
    with open("C:\code\get_examtopics\out\LISTA_preguntas.html", "w", encoding="utf-8") as file:
        file.write(str(discussion_list))
        file.close    
    
    
    file = open(r"C:\code\get_examtopics\out\preguntas.html", "w", encoding="utf-8")
    # importamos los estilos
    imports = "<link rel=""stylesheet"" href=""./css/styles.css"">"
    file.write(imports)
    file.write(f"<h1>{url}<br>{cert}</h1>")


    separador = "div class=""line""></div>"
    
    respuestas = []
    error_count = 0
    for pregunta in discussion_list:
        r = get_qa(pregunta, logger)    
        '''
         todo: en esa funcion incorporar algo par detectar si tengo varios errores consecutivos, o si ya estoy recibiendo una web 
        
            General Server Error Error Code: 1004

        si recibes esto es porque quiza esten viendo mucho trafico desde tu ip
        '''
        if r is not None:
            respuestas.append(r)
            file.write(r)
            file.write(separador)
            #seteamos error a 0 
            error_count=0
        else:
            error_count+=1
            
        #si llegamos a 10 errores seguidos,paramos por que estamos baneados
        if error_count>=10:
            logger.error(f"Paramos ya que hemos llegado al numero maximo de errores")
            break
    
    file.close
    logger.info(f"Recuperadas {len(respuestas)} respuestas")     
    logger.info("Fin")
    
    
    ##url = "https://www.examtopics.com/discussions/snowflake/view/69302-exam-snowpro-core-topic-1-question-70-discussion/"
    


if __name__ == "__main__":
    main()
   



