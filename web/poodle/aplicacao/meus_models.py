import requests
import requests_cache
from bs4 import BeautifulSoup

# Configurações iniciais
requests_cache.install_cache(expire_after=60)  # atualiza o cache a cada 60 segundos


class Indexador:
    # Construtor
    def __init__(self):
        self.url = ''  # url inicial
        self.keywords = []  # a busca pode ser uma palavra apenas ou uma frase.
        self.matchs = []  # lista de sites encontrados com pelo menos uma keyword

    # Funcao principal
    def search(self, keyword, url, deth=0):
        self.keywords = keyword.split()
        self.url = url if (url is not None) else 'https://www.uol.com.br'
        self.url = url if (url != '') else 'https://www.uol.com.br'

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
                html = response.text
                soup = BeautifulSoup(response.text, 'html.parser')

                frases = soup.find_all(text=True)

                for keyword in self.keywords:

                    keyword = keyword.lower()

                    for frase in frases:
                        palavras_da_frase = frase.lower().split()
                        for palavra in palavras_da_frase:
                            if keyword in palavra:  # se repete 4 vezes
                                self.salvar_site(site, keyword, html)

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
    def salvar_site(self, a_href, keyword, html):
        soup = BeautifulSoup(html, 'html.parser')
        frases = soup.find_all(text=True)
        title = a_href
        descricao = []  # transformei a descrição em uma lista apenas para ver se os resultados davam certo

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
                    descricao.append(' '.join(palavras_da_frase[max(0, index - 5):min(index + 6, len(palavras_da_frase))]))

        self.matchs.append(
            {'link': a_href,
             'titulo': title,
             'descricao': '... '.join(descricao)
             }
        )

        # só lembrando que, por causa desses "for" iguais no salvar_site e no visitar_sites, a resposta no fim sai
        # duplicada kkkjkj

    def get_matchs(self):
        resultado = []
        for match in self.matchs:
            if match not in resultado:
                resultado.append(match)
        return resultado
