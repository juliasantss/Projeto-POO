"""
banco_urls.py
Módulo responsável por carregar e gerenciar as URLs do sistema.

Grupo: Enquanto Funcionar Tá Bom
Disciplina: Programação Orientada a Objetos
"""

import re


class BancoURLs:
    """
    Classe que gerencia as URLs cadastradas no sistema.

    As URLs são carregadas de um arquivo e também podem ser adicionadas
    durante a execução do programa.
    """

    # Regex para validar o formato das URLs
    _FORMATO_URL = re.compile(
        r'^(https?://)?'           # http:// ou https:// (opcional)
        r'(www\.)?'                # www. (opcional)
        r'[\w\-]+(\.[\w\-]+)+'     # domínio (ex: google.com)
        r'(/[\w\-./]*)?$'          # caminho opcional (ex: /teste)
    )

    def __init__(self, arquivo: str = "urls.txt"):
        """
        Inicializa o banco de URLs.

        Args:
            arquivo (str): arquivo onde as URLs estão armazenadas.
        """
        self._urls = set()
        self._arquivo = arquivo
        self._carregar_arquivo()

    def _carregar_arquivo(self) -> None:
        """
        Lê o arquivo e adiciona as URLs válidas ao sistema.
        Ignora linhas vazias e comentários.
        """
        try:
            with open(self._arquivo, "r", encoding="utf-8") as f:
                for linha in f:
                    url = linha.strip()
                    if url and not url.startswith("#"):
                        if self.validar_formato(url):
                            self._urls.add(url)
        except FileNotFoundError:
            print(f"[AVISO] Arquivo '{self._arquivo}' não encontrado. Banco iniciado vazio.")

    def validar_formato(self, url: str) -> bool:
        """
        Verifica se a URL está em um formato válido.
        """
        if not url or not url.strip():
            return False
        return bool(self._FORMATO_URL.match(url.strip()))

    def existe(self, url: str) -> bool:
        """
        Verifica se a URL já está cadastrada.
        """
        return url.strip() in self._urls

    def adicionar(self, url: str) -> bool:
        """
        Adiciona uma nova URL ao sistema.

        Returns:
            True se adicionou, False se já existia.

        Raises:
            ValueError se o formato for inválido.
        """
        url = url.strip()

        if not self.validar_formato(url):
            raise ValueError(f"Formato de URL inválido: '{url}'")

        if self.existe(url):
            return False

        self._urls.add(url)
        self._salvar_url_no_arquivo(url)
        return True

    def _salvar_url_no_arquivo(self, url: str) -> None:
        """
        Salva a nova URL no arquivo.
        """
        try:
            with open(self._arquivo, "a", encoding="utf-8") as f:
                f.write(url + "\n")
        except OSError as e:
            print(f"[AVISO] Não foi possível salvar no arquivo: {e}")

    def listar(self) -> list:
        """
        Retorna todas as URLs cadastradas.
        """
        return sorted(self._urls)

    def total(self) -> int:
        """
        Retorna a quantidade de URLs cadastradas.
        """
        return len(self._urls)
