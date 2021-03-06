import requests
from bs4 import BeautifulSoup
import re
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import pagina12_scraper as p12
import getters as g

def _nested_links(listed_links):
    logger.info('Showing nested links...')
    nest = []

    # Droping duplicated
    i = 0
    while i <= len(listed_links):
        link = listed_links[i]
        nest.append(link)
        i += 2

    return nest

def __create_page_dictonary(promo_article):
        # Crear objeto de Article
        la_nota = g.Article(url = promo_article)
        # Crear un page dictionary con nuestro objeto con el método mk_map()
        page_dictonary = la_nota.mk_map()
        return page_dictonary

def  __chosen_link(section_map):
    logger.info('Choose only one of them by typing its index.')
    choice = int(input('> '))
    
    for i in section_map:
        if i == choice:
            sub_section = str(section_map[i].values())
            sub_section = _cleaning_url(sub_section)
            print(f'{sub_section}')
            break
        elif choice > len(section_map):
            print('Not an option.')

    return sub_section

def _fetch_articles(sub_soup):
    articles = []
    listed_articles = (sub_soup.find('ul', attrs={'class':'article-list'})
                      .find_all('a')
                
                    )
    
    for article in listed_articles:
        url = article.get('href')
        articles.append(url)
    
    return articles

def _get_promo(sub_soup):
    promo_article =  (sub_soup.find('div', attrs={'class':'featured-article__container'})
                  .a.get('href')
                )

    return promo_article

def _cleaning_url(sub_section):
    
    beg = 14 # Static index of url starting after quotation mark
    end = len(sub_section) - 1
    while end <= len(sub_section):
        if sub_section[end] == "'":
            sub_section = sub_section[beg:end]
            break
        
        end = end - 1
        
    return sub_section
        
def sub_main(section_map):
    for link in section_map:
        print(f'{link}:{section_map[link]}')

    sub_section = __chosen_link(section_map)
    try:
        ss_section = requests.get(sub_section)
    except:
        print(p12.request_error)

    sub_soup = p12._parsing(url = ss_section)
    
    # See promoted article
    logging.info('See promoted article by entering the link below!')
    promo_article = _get_promo(sub_soup)
    
    
    print(f'Artículo promocional: {promo_article}' + '\n')
    
    page_dictonary = __create_page_dictonary(promo_article)
    logging.info('Use PANDAS to create your dataset after this pager below.')
    print('\n')
    print(page_dictonary)
    print('\n')
    try:
        listed_links = _fetch_articles(sub_soup)
    except Exception as fetch_error:
        print('ERROR while fetching. HINT - overwatch tagging get method.')
        pass

    # Nested links
    nest = input('Doy you want to see nested links? (s/n): ')
    if nest == 's':
        clean_nest = _nested_links(listed_links)
        for link in clean_nest:
            print(link)
    else:
        return 'Web scraper has expired session.'


    