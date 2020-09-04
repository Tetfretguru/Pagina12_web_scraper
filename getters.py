from bs4 import BeautifulSoup
from IPython.display import Image
import requests

class Article:
    def __init__(self, url):
        self.url = url
        self._copete = _get_copete(url)
        self._title = _get_title(url)
        self._date = _get_pub_date(url)
        self._volanta = _get_volanta(url)
        self._media_file = _get_media(url)
    
    def mk_map(self):
        page_dict = {
           'url': self.url,
           'copete':self._copete, 
           'title':self._title,
           'date':self._date,
           'volanta':self._volanta,
           'imagen':self._media_file
        }
        return page_dict
    
def __tester(url):
    nota = requests.get(url)
    s_nota = BeautifulSoup(nota.text, 'lxml')
    
    return s_nota

def _get_title(url):
    s_nota = __tester(url)
    # Extraer título
    titulo = s_nota.find('h1', attrs = {'class':'article-title'})
    if titulo:
        return titulo.text
    else:
        return None

def _get_pub_date(url):
    s_nota = __tester(url)
    # Extraer fecha
    fecha = s_nota.find('span', attrs = {'pubdate':'pubdate'}).get('datetime')
    if fecha:
        return fecha       
    else:
        return None

def _get_volanta(url):
    s_nota = __tester(url)
    # Extraer volanta
    volanta = s_nota.find('div', attrs = {'class':'article-summary'})
    if volanta:
        return volanta.text
    else:
        return None

def _get_copete(url):
    s_nota = __tester(url)
    # Extraer copete
    copete = s_nota.find('h2', attrs = {'class':'article-prefix'})
    if copete:
        return copete.text
    else:
        return None

def _get_media(url):
    s_nota = __tester(url)
    # Extraer archivos multimedia
    media = s_nota.find('div', attrs = {'class':'article-main-media'})
    imagenes = media.find_all('img')

    if len(imagenes) == 0:
        print('No hay imágenes')
    else:
        imagen = imagenes[-1] # Porque estan ordenadas de menor a mayor
        imagen_src = imagen.get('data-src')
        #print(f'Img URL: {imagen_src}')

    img_req = requests.get(imagen_src)
    if img_req.status_code == 200:
        img = Image(img_req.content)
        return imagen_src