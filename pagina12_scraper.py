import requests
from bs4 import BeautifulSoup
import re
import logging
logging.basicConfig(level=logging.INFO)
import pag12_submain as p12s

logger = logging.getLogger(__name__)

def _build_map(sections_url, sections_text):
    section_map = {}
    n = 0

    while n < len(sections_url) and n < len(sections_text):
        for url in sections_url:
            for text in sections_text:
                section_map[n] = {text:url}
                n += 1

    
    return section_map
    

def _extract_text(soup_sections):
    logger.info('Extracting text from tags...')
    sections_text = [section.a.get_text('href') for section in soup_sections]

    return sections_text

def _extract_links(soup_sections):
    logger.info('Extracting links from "href"...')
    sections_url = [section.a.get('href') for section in soup_sections]
    
    return sections_url

def _scraping_tags(soup):
    logger.info('Scraping the list tags for sections...')
    soup_sections = (soup.find('ul', attrs={'class':'sections'})
        .find_all('li')
    )

    return soup_sections

def _parsing(url):
    logger.info('Parsing website...')
    soup =  BeautifulSoup(url.text, 'lxml')
    
    
    return soup

def main(pagina12):
    logger.info('Scraping "Página 12" news page...')
    soup = _parsing(url = pagina12)
    soup_sections = _scraping_tags(soup)
    sections_url = _extract_links(soup_sections)
    sections_text = _extract_text(soup_sections)
    section_map = _build_map(sections_url, sections_text)
    logger.info(f'Have been found {len(section_map)} redirecting links.')

    q = 'Do you want to continue scraping any of them? (1:yes / 0: no)'
    res = input(q)
    if res == '1':
        return p12s.sub_main(section_map)
    else:
        return 'Session expired.'





if __name__ == '__main__':
    url = 'https://www.pagina12.com.ar/'
    pagina12 = requests.get(url)

    main(pagina12)