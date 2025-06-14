import argparse
import sys
import time

sys.path.append('./src')  # Donde 'subcarpeta' es la carpeta donde está tu proxy.py

import re
from src.get_qa import *
from src.get_discussions import *
import logging

from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

lock = threading.Lock()

def process_question(index, pregunta, logger):
    global error_count
    r = get_qa(pregunta, logger)
    with lock:
        if r is not None and "General Server Error Error Code: 1004" not in r:
            error_count = 0
        else:
            error_count += 1
        return index, r, error_count
    

def main():

    #logging.basicConfig(filename='app.log', level=logging.DEBUG)
    logging.basicConfig( level=logging.INFO)
    logger = logging.getLogger()
    

    url = "https://www.examtopics.com/discussions/microsoft/"
    cert = "DP-700"
    
    
    
    logger.info(f"Iniciando recuperacion de pregutnas de {cert} desde {url}")
    
    if True: ## asi desactivo leer las discusiones
        start_discussion_time = time.time()
        discussion_list = get_discussions_parallel( url, cert, logger, max_pages=1000, workers=4)
        ##ordeno para recuperar por id, que entiendo será de mas reciente a mas antiguo
        print("\n".join(str(e) for e in discussion_list))
        discussion_list.sort(reverse=True)
        print("\n".join(str(e) for e in discussion_list))

        
        logger.info(f"Recuperadas {len(discussion_list)} discusiones")
        
        #salvamos las preguntas a archivo
        with open("out\LISTA_preguntas.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(str(e) for e in discussion_list))
            file.close    
        
        end_discussion_time = time.time()
        logger.info(f"Tiempo del Paso 1: {end_discussion_time - start_discussion_time:.2f} segundos")
    

    
    start_queston_time = time.time()
    
    file_Salida = f"out/Preguntas_{cert}.html"
    with ThreadPoolExecutor(max_workers=5) as executor, open(file_Salida, "w", encoding="utf-8") as file, open(r"out\LISTA_preguntas.txt", "r", encoding="utf-8") as file_qa:
        discussion_list = [line.strip() for line in file_qa if line.strip()]    
        imports = "<link rel=""stylesheet"" href=""./css/styles.css"">"
        file.write(imports)
        file.write(f"<h1>{url}<br>{cert}</h1>")

        separador = "<div class=""line""></div>"
                
        lock = threading.Lock()
        MAX_CONSEC_ERRORS = 10
        
        ##aqui
        respuestas = []
    
        future_to_index = {executor.submit(process_question, i, pregunta, logger): i for i, pregunta in enumerate(discussion_list)}

        for future in as_completed(future_to_index):
            index, r, current_error_count = future.result()

            if r is not None and "General Server Error Error Code: 1004" not in r:
                respuestas.append(r)
                file.write(f"<br><h2> Pregunta {index+1} de {len(discussion_list)} <h2><br>")
                file.write(r)
                file.write(separador)

            if current_error_count >= MAX_CONSEC_ERRORS:
                logger.error(f"Paramos ya que hemos llegado al numero maximo de errores consecutivos")
                break
    ##fin
    file.close
    logger.info(f"Recuperadas {len(respuestas)} respuestas")
    end_queston_time = time.time()
    logger.info(f"Tiempo del Paso 2: {end_queston_time - start_queston_time:.2f} segundos")     
    logger.info("Fin")
    
    
    ##url = "https://www.examtopics.com/discussions/snowflake/view/69302-exam-snowpro-core-topic-1-question-70-discussion/"
    


if __name__ == "__main__":
    main()
   



