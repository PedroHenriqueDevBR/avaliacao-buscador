import requests
import requests_cache
from bs4 import BeautifulSoup


# Configurações iniciais
requests_cache.install_cache('visited_cache')


class Indexador:
    # Construtor
    def __init__(self):
        self.url = '' # url inicial
        self.deth = '' # limite de camadas para busca de informações, evita loop infinito
        self.keywords = [] # a busca pode ser uma palavra apenas ou uma frase.
        self.matchs = [] # lista de sites encontrados com pelo menos uma keyword

    # Funcao principal
    def seach(self, keyword, url = None, deth = 0):
        self.keywords = keyword.split()
        self.url = url if (url != None) else 'https://www.uol.com.br'
        self.deth = deth

        camada_visitada = 0
        sites_sem_visita = [self.url]

        while camada_visitada <= self.deth:
            sites_sem_visita = self.visitar_sites(sites_sem_visita)
            camada_visitada += 1

    # Visita cada site
    def visitar_sites(self, sites):
        for site in sites:
            try:
                response = requests.get(site)
            except:
                continue

            if response.status_code == 200:
                html = response.text

                for keyword in self.keywords:
                    if keyword in html:
                        self.salvar_site(site, html)

                links = self.extrair_links(html)

        return links

    # Extrai todos os links para uma nova busca
    def extrair_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        extracao_de_tag = soup.find_all('a')
        links_encontrados = []

        for link in extracao_de_tag:
            if 'href' in link.attrs:
                if 'http' in link['href']:
                    links_encontrados.append(link['href'])

        return links_encontrados

    # Salva um site caso haja um match
    def salvar_site(self, a_href, html):
        soup = BeautifulSoup(html, 'html.parser')
        title =  a_href
        metadados = soup.find_all('meta')
        descricao = 'Sem descricao'

        try:
            title = soup.title.string
        except:
            pass

        for meta in metadados:
            if 'name' in meta.attrs:
                if meta.attrs['name'] == 'description':
                    descricao = meta.attrs['content']

        self.matchs.append(
            {'link': a_href,
             'titulo': title,
             'descricao': descricao
             }
        )