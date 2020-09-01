from IPython.display import Image

class Article:
    def __init__(self, url):
        self.url = url
        self._copete = _get_copete(url)
        self._title = _get_title(url)
        self._date = _get_pub_date(url)
        self._volanta = _get_volanta(url)

    def __tester(self, url):
        try:
            if url.status_code == 200:
                s_url = BeautifulSoup(url.text, 'lxml')
                return s_url
        except Exception as req_error:
            return req_error

    def _get_title(self, url):
        s_nota = __tester(url)
        # Extraer título
        titulo = s_nota.find('h1', attrs = {'class':'article-title'})
        return f'Título: {titulo.text}' + '\n'

    def get_pub_date(self, url):
        s_nota = __tester(url)
        # Extraer fecha
        fecha = s_nota.find('span', attrs = {'pubdate':'pubdate'}).get('datetime')
        return f'Fecha: {fecha}' + '\n')
       

    def _get_volanta(self, url):
        s_nota = __tester(url)
        # Extraer volanta
        volanta = s_nota.find('div', attrs = {'class':'article-summary'})
        return 'Volanta: ' + '\n' + volanta.text

    def _get_copete(self, url):
        s_nota = __tester(url)
        # Extraer copete
        copete = s_nota.find('h2', attrs = {'class':'article-prefix'})
        return f'Copete: {copete.text}' + '\n')
    
    def _get_media(self, url):
        s_nota = __tester(url)
        # Extraer archivos multimedia
        media = s_nota.find('div', attrs = {'class':'article-main-media'})
        imagenes = media.find_all('img')
        
        if len(imagenes) == 0:
            print('No hay imágenes')
        else:
            imagen = imagenes[-1] # Porque estan ordenadas de menor a mayor
            imagen_src = imagen.get('data-src')
            print(f' Img URL: {imagen_src}')

        img_req = requests.get(imagen_src)
        if img_req.status_code == 200:
            return Image(img_req.content)
