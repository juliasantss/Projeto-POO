# banco_urls.py
# gerencia as urls cadastradas e suas paginas internas
# usa um dicionario aninhado pra representar a hierarquia de paginas
#
# estrutura interna (arvore):
# {
#   "www.ifpb.edu.br": {
#     "arquivo": "paginas/ifpb.txt",
#     "filhos": {
#       "tsi": {
#         "arquivo": "paginas/ifpb_tsi.txt",
#         "filhos": { "alunos": {...}, "professores": {...} }
#       }
#     }
#   }
# }
#
# Grupo 05 - Enquanto Funcionar Ta Bom

import re
import os

class BancoURLs:

    # regex pra validar formato de url
    # aceita: google.com | www.google.com | http://google.com | http://site.com/pagina
    _FORMATO_URL = re.compile(
        r'^(https?://)?'
        r'(www\.)?'
        r'[\w\-]+(\.[\w\-]+)+'
        r'(/[\w\-./]*)?$'
    )

    def __init__(self, arquivo="urls.txt"):
        self._arvore  = {}   # dicionario aninhado com todas as urls
        self._arquivo = arquivo
        self._carregar()

    # --- metodos internos ---

    def _novo_no(self, arquivo=""):
        # cria um no vazio pra arvore
        return {"arquivo": arquivo, "filhos": {}}

    def _chave(self, url):
        # remove http/https pra padronizar a chave na arvore
        # mas MANTEM o www pra nao perder o formato original
        url = url.strip()
        url = re.sub(r'^https?://', '', url)
        return url

    def _carregar(self):
        # le o arquivo e monta a arvore de urls
        # formato de cada linha: www.site.com paginas/arquivo.txt
        try:
            with open(self._arquivo, "r", encoding="utf-8") as f:
                for linha in f:
                    linha = linha.strip()
                    if not linha or linha.startswith("#"):
                        continue
                    partes  = linha.split()
                    url     = partes[0]
                    arquivo = partes[1] if len(partes) > 1 else ""
                    if self.validar_formato(url):
                        self._inserir(url, arquivo)
        except FileNotFoundError:
            print(f"[AVISO] '{self._arquivo}' nao encontrado. Banco vazio.")

    def _inserir(self, url, arquivo=""):
        # coloca a url na arvore mantendo a hierarquia
        chave    = self._chave(url)
        partes   = chave.split("/")
        dominio  = partes[0]      # ex: www.ifpb.edu.br
        caminhos = partes[1:]     # ex: ['tsi', 'alunos']

        if dominio not in self._arvore:
            self._arvore[dominio] = self._novo_no()

        no = self._arvore[dominio]

        for parte in caminhos:
            if not parte:
                continue
            if parte not in no["filhos"]:
                no["filhos"][parte] = self._novo_no()
            no = no["filhos"][parte]

        if arquivo:
            no["arquivo"] = arquivo

    def _buscar_no(self, url):
        # retorna o no da arvore da url ou None se nao existir
        chave    = self._chave(url)
        partes   = chave.split("/")
        dominio  = partes[0]
        caminhos = partes[1:]

        if dominio not in self._arvore:
            return None

        no = self._arvore[dominio]

        for parte in caminhos:
            if not parte:
                continue
            if parte not in no["filhos"]:
                return None
            no = no["filhos"][parte]

        return no

    def _salvar(self, url, arquivo=""):
        # appenda a nova url no arquivo pra persistir
        try:
            with open(self._arquivo, "a", encoding="utf-8") as f:
                linha = url if not arquivo else f"{url} {arquivo}"
                f.write(linha + "\n")
        except OSError as e:
            print(f"[AVISO] Nao foi possivel salvar: {e}")

    # --- api publica ---

    def validar_formato(self, url):
        if not url or not url.strip():
            return False
        return bool(self._FORMATO_URL.match(url.strip()))

    def existe(self, url):
        return self._buscar_no(url) is not None

    def arquivo_da_url(self, url):
        no = self._buscar_no(url)
        if no is None:
            return ""
        return no.get("arquivo", "")

    def links_internos(self, url):
        # retorna as subpaginas disponiveis da url atual
        no = self._buscar_no(url)
        if no is None:
            return []
        return ["/" + filho for filho in no["filhos"].keys()]

    def resolver_caminho(self, home, caminho):
        # transforma /tsi em www.ifpb.edu.br/tsi
        # tenta como subpagina do home atual primeiro
        # se nao encontrar, tenta da raiz do dominio
        chave_home = self._chave(home)
        caminho    = caminho.lstrip("/")

        # tenta: home_atual + /caminho
        tentativa = f"{chave_home}/{caminho}"
        if self._buscar_no(tentativa) is not None:
            # reconstroi com o prefixo original (www ou sem www)
            return self._prefixo_original(home) + tentativa[len(self._chave(home).split('/')[0]):]

        # tenta: dominio_raiz + /caminho
        dominio = chave_home.split("/")[0]
        return self._prefixo_original(home) + f"/{caminho}" if "/" not in chave_home else dominio + f"/{caminho}"

    def _prefixo_original(self, url):
        # devolve o prefixo do dominio como foi digitado originalmente
        # ex: "www.ifpb.edu.br/tsi" -> "www.ifpb.edu.br"
        chave = self._chave(url)
        return chave.split("/")[0]

    def adicionar(self, url, arquivo=""):
        url = url.strip()
        if not self.validar_formato(url):
            raise ValueError(f"'{url}' nao tem formato de URL valido")
        if self.existe(url):
            return False
        self._inserir(url, arquivo)
        self._salvar(url, arquivo)
        return True

    def listar(self):
        urls = []
        for dominio, no in self._arvore.items():
            self._coletar(dominio, no, urls)
        return sorted(urls)

    def _coletar(self, prefixo, no, resultado):
        resultado.append(prefixo)
        for filho, no_filho in no["filhos"].items():
            self._coletar(f"{prefixo}/{filho}", no_filho, resultado)

    def total(self):
        return len(self.listar())
