import requests
import requests_cache
from bs4 import BeautifulSoup
import time

# Configurações iniciais
requests_cache.install_cache(expire_after=3600)  # Atualiza o cache a cada hora.


class Indexador:
    # Construtor
    def __init__(self):
        self.url = ''  # Url inicial.
        self.keywords = []  # A busca pode ser uma ou várias palavras.
        self.matchs = []  # Lista de sites encontrados com pelo menos uma keyword.

    # Funcao principal
    def search(self, keyword, url, depth=0):
        inicio = time.time()

        self.keywords = keyword.split()
        self.url = url if (url != '') else 'https://academico.ifpi.edu.br'  # Caso vazio, inicia a busca por esta url.

        camada_visitada = 0
        sites_sem_visita = [self.url]

        while camada_visitada <= depth:
            sites_sem_visita = self.visitar_sites(sites_sem_visita)  # Nesse momento, realiza uma busca recursiva.
            camada_visitada += 1

        fim = time.time()

        print('\n\n==========================================')
        print('Tempo de execução: {}'.format(fim - inicio))
        print('==========================================\n\n')

    # Visita cada site
    def visitar_sites(self, sites):
        links = []
        for site in sites:
            try:
                response = requests.get(site)
                if response.status_code == 200:

                    print('\n==========================================')
                    print('Visitando: ' + site)
                    print('==========================================')

                    html = response.content
                    soup = BeautifulSoup(html, 'html.parser')
                    frases = soup.get_text().replace('\n', ' ').split()

                    for keyword in self.keywords:
                        keyword = keyword.lower()
                        for palavra in frases:
                            if keyword in palavra.lower():
                                if self.adiciona_ponto(site):  # Keyword encontrada.
                                    continue
                                self.salvar_site(site, keyword, soup)

                    links = self.extrair_links(soup)
            except:
                continue

        return links

    def adiciona_ponto(self, url):
        if len(self.matchs) > 0:
            for site in self.matchs:
                if site['link'] == url:
                    site['pontos'] += 1
                    return True
        return False

    def extrair_links(self, soup):
        extracao_de_tag = soup.find_all('a')
        links_encontrados = []

        for link in extracao_de_tag:
            if 'href' in link.attrs:
                if 'http' in link['href']:
                    links_encontrados.append(link['href'])

        return links_encontrados

    def salvar_site(self, a_href, keyword, soup):
        frases = soup.find_all(text=True)
        descricao = []

        try:
            title = soup.title.string

            for frase in frases:
                palavras_da_frase = frase.split()
                for palavra in palavras_da_frase:
                    if keyword in palavra.lower():
                        index = palavras_da_frase.index(palavra)  # Salva a posicao da palavra na frase.

                        # Em seguida, monta uma frase com 5 palavras antes e depois da keyword:
                        descricao.append(
                            ' '.join(palavras_da_frase[max(0, index - 5):min(index + 6, len(palavras_da_frase))]))

            self.matchs.append(
                {'link': a_href,
                 'titulo': title,
                 'descricao': '... '.join(descricao),
                 'pontos': 1
                 }
            )
        except:
            pass

    # Método que retira as repetições de sites e ordena o resultado
    def get_matchs(self):
        resultado = []
        for match in self.matchs:
            if match not in resultado:
                resultado.append(match)
        resultado.sort(key=lambda x: x['pontos'], reverse=True)

        return resultado
