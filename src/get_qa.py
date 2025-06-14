from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import re
import os
import logging
import sys
sys.path.append('./proxy')  # Donde 'subcarpeta' es la carpeta donde está tu proxy.py

import proxy.ProxyRotator as proxyrot

def replaces(text):
    # Función para limpiar el texto, eliminando saltos de línea y espacios duplicados
    if text:
        text = re.sub(r'\s+', ' ', text).strip()
    return text

'''
    recibida la url de la discussionm parseará el contenido. Si recibe error 1004 o General server error, puede que estes ya baneado
    
    todo:
    review the return values in case of not getting the expeted content.
'''
def get_qa(url,logger):
    with sync_playwright() as p:
        #proxy = proxyrot.get_good()
        #browser = p.chromium.launch(proxy={"server": proxy},headless=True)
        browser = p.chromium.launch(headless=True)
        
        page = browser.new_page()
        logger.debug(f"Procesando url: {url}")
        
        try:
            # Navegar a la URL
            page.goto(url, timeout=15000)
            
            # Intentar revelar la solución si el botón existe
            try:
                page.click(".reveal-solution", timeout=5000)
            except PlaywrightTimeoutError:
                logger.error(f"Procesando url: {url} No se encontró botón de 'reveal solution' o no cargó a tiempo.")
                return None

            # Esperar a que el contenido principal cargue
            page.wait_for_selector(".question-body", timeout=10000)
            
            # Eliminar estilos que afectan la opacidad
            # Eliminar cualquier propiedad 'opacity' en los atributos 'style'
            
            # Obtener el HTML del elemento con la clase .question-body después de limpiar
            
            header_html = page.inner_html(".discussion-list-header")
            question_html = page.inner_html(".question-body")
            
            # Depuración: Verificar si se obtiene contenido HTML
            if not question_html:
                #un ejeplo puede ser que nos este devolviendo la tipica pagina de error 1004z   
                logger.warning(f"Procesando url: {url} o se pudo obtener el HTML del elemento .question-body.")
                browser.close()
                return None
            
            # Si la respuesta contiene lo esperado, 
            # Crear el hiperenlace con la URL 
            link_html = f'<a href="{url}" target="_blank">{url}</a><br>\n'
            # Eliminar los botones específicos usando sus clases
            question_html = re.sub(r'<a href="#" class="btn btn-primary reveal-solution d-none">.*?</a>', '', question_html)
            question_html = re.sub(r'<a href="#" class="btn btn-primary hide-solution">.*?</a>', '', question_html)
          
            # Combinar el hiperenlace con el HTML recuperado
            full_html = header_html + question_html  + link_html 
            
            #Eliminamos la opacidad que por defecto introduce examtopics
            full_html = re.sub(r'opacity\s*:\s*[^;]+;', '', full_html)
            
            browser.close()
            return full_html
                
        except Exception as e:
            logger.error(f"Error procesando la URL: {url} Exepcion {e}")
            browser.close()
            return None

