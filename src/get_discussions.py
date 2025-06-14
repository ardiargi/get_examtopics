from playwright.sync_api import sync_playwright
from concurrent.futures import ProcessPoolExecutor, as_completed
import logging
import sys

def scrape_page(url, cert, page_num, timeout_seconds=5):
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            print (f"{url}{page_num}")
            
            response = page.goto(f"{url}{page_num}")

            if response.status != 200:
                return []

            page.wait_for_selector("a.discussion-link", timeout=5000)
            links = page.locator("a.discussion-link")
            count = links.count()
            for i in range(count):
                link_text = links.nth(i).text_content()
                if cert in link_text:
                    href = links.nth(i).get_attribute("href")
                    results.append("https://www.examtopics.com" + href)

            browser.close()
    except Exception as e:
        return []
    return results

def get_discussions_parallel(url, cert, logger, max_pages=500, workers=4):
    all_questions = []

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(scrape_page, url, cert, i) for i in range(1, max_pages + 1)]
        for future in as_completed(futures):
            try:
                result = future.result()
                all_questions.extend(result)
            except Exception as exc:
                logger.error(f"Error durante la ejecución paralela: {exc}")
    
    return all_questions
