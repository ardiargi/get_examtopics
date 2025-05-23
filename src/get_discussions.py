from playwright.sync_api import sync_playwright
import re
import logging

import sys
sys.path.append('./proxy')  # Donde 'subcarpeta' es la carpeta donde está tu proxy.py

import proxy.ProxyRotator as proxyrot

def get_discussions(url, cert,logger):

    questions = []
    num_page = 1
    with sync_playwright() as p:
     
        #proxy = proxyrot.get_good()
        #browser = p.chromium.launch(proxy={"server": proxy},headless=True)
        browser = p.chromium.launch(headless=True)
        
        page = browser.new_page()
           
        while True:
            logger.debug(f"Procesando {url}{num_page}")
            try:
                response = page.goto(f"{url}{num_page}")
            except Exception as e:
                logger.error(f"Página {url}{num_page} no encontrada. Deteniendo...")
                break       
            logger.debug(f"Procesando {url}{num_page}. Response: {response.status}")
                
            # Verificar si la respuesta es 404 o no exitosa
            if response.status != 200:
                logger.error(f"Página {url}{num_page} no encontrada (status: {response.status}). Deteniendo...")
                break
                    
            page.wait_for_selector("a.discussion-link", timeout=5000)

            links = page.locator("a.discussion-link")
            count = links.count()
            for i in range(count):
                link_text = links.nth(i).text_content()
                if cert in link_text:
                    href = links.nth(i).get_attribute("href")
                    #print(f"the url is: {url}")
                    #print(f"https://www.examtopics.com{href}")
                  
                    questions.append("https://www.examtopics.com"+href)
                
            num_page += 1

        browser.close()        
        return questions        
    
    browser.close()        
    return questions
