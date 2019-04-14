import requests
import requests_cache
from bs4 import BeautifulSoup

# Configurações iniciais
requests_cache.install_cache(expire_after=600)  # atualiza o cache a cada 10 minutos


class Indexador:
    # Construtor
    def __init__(self):
        self.url = ''  # url inicial
        self.keywords = []  # a busca pode ser uma palavra apenas ou uma frase.
        self.matchs = []  # lista de sites encontrados com pelo menos uma keyword

    # Funcao principal
    def search(self, keyword, url, deth=0):
        self.keywords = keyword.split()
        self.url = url if (url != '') else 'https://academico.ifpi.edu.br'

        camada_visitada = 0
        sites_sem_visita = [self.url]

        while camada_visitada <= deth:
            sites_sem_visita = self.visitar_sites(sites_sem_visita)
            camada_visitada += 1

    # Visita cada site
    def visitar_sites(self, sites):
        links = []
        for site in sites:
            try:
                response = requests.get(site)
            except:
                continue

            if response.status_code == 200:
                if self.adiciona_ponto(site):
                    continue

                html = response.content
                soup = BeautifulSoup(html, 'html.parser')
                frases = soup.find_all(text=True)

                for keyword in self.keywords:
                    keyword = keyword.lower()
                    for frase in frases:
                        palavras_da_frase = frase.split()
                        for palavra in palavras_da_frase:
                            if keyword in palavra.lower():
                                self.salvar_site(site, keyword, html)

                links = self.extrair_links(html)
        return links

    def adiciona_ponto(self, url):
        if len(self.matchs) != 0:
            for site in self.matchs:
                if site['link'] == url:
                    site['pontos'] += 1
                    return True
        return False

    def extrair_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        extracao_de_tag = soup.find_all('a')
        links_encontrados = []

        for link in extracao_de_tag:
            if 'href' in link.attrs:
                if 'http' in link['href']:
                    links_encontrados.append(link['href'])

        return links_encontrados

    def salvar_site(self, a_href, keyword, html):
        soup = BeautifulSoup(html, 'html.parser')
        frases = soup.find_all(text=True)
        title = a_href
        descricao = []

        try:
            title = soup.title.string
        except:
            pass

        for frase in frases:
            palavras_da_frase = frase.split()
            for palavra in palavras_da_frase:
                if keyword in palavra.lower():
                    index = palavras_da_frase.index(palavra)  # busca a posicao da palavra na frase

                    # faz append de 5 palavras antes e depois da keyword:
                    descricao.append(
                        ' '.join(palavras_da_frase[max(0, index - 5):min(index + 6, len(palavras_da_frase))]))

        self.matchs.append(
            {'link': a_href,
             'titulo': title,
             'descricao': '... '.join(descricao),
             'pontos': 1
             }
        )

    def get_matchs(self):
        resultado = []
        for match in self.matchs:
            if match not in resultado:
                resultado.append(match)
        resultado.sort(key=lambda x: x['pontos'], reverse=True)

        return resultado
