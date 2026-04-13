"""
banco_urls.py
-------------
Módulo responsável por carregar, validar e gerenciar o banco de URLs do browser.

Grupo 05 - Enquanto Funcionar Tá Bom
Disciplina: Programação Orientada a Objetos
"""

import re


class BancoURLs:
    """
    Gerencia o banco de URLs válidas conhecidas pelo browser.

    As URLs são carregadas de um arquivo texto na inicialização e podem
    ser adicionadas dinamicamente via comando #add durante a execução.

    Attributes:
        _urls (set): conjunto de URLs cadastradas (sem duplicatas).
        _arquivo (str): caminho do arquivo de persistência.
    """

    # Expressão regular para validar formato de URL
    _FORMATO_URL = re.compile(
        r'^(https?://)?'           # protocolo opcional (http:// ou https://)
        r'(www\.)?'                # www opcional
        r'[\w\-]+(\.[\w\-]+)+'    # domínio (ex: ifpb.edu.br)
        r'(/[\w\-./]*)?$'          # caminhos internos opcionais (ex: /tsi/alunos)
    )

    def __init__(self, arquivo: str = "urls.txt"):
        """
        Inicializa o banco carregando as URLs do arquivo.

        Args:
            arquivo (str): Caminho para o arquivo de URLs. Padrão: 'urls.txt'.
        """
        self._urls = set()
        self._arquivo = arquivo
        self._carregar_arquivo()

    def _carregar_arquivo(self) -> None:
        """
        Lê o arquivo de URLs e popula o banco interno.
        Linhas em branco e comentários (iniciados por #) são ignorados.

        Raises:
            FileNotFoundError: Se o arquivo não for encontrado (aviso, não encerra).
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
        Verifica se a URL segue um formato válido.

        Args:
            url (str): URL a ser validada.

        Returns:
            bool: True se o formato for válido, False caso contrário.
        """
        if not url or not url.strip():
            return False
        return bool(self._FORMATO_URL.match(url.strip()))

    def existe(self, url: str) -> bool:
        """
        Verifica se uma URL está cadastrada no banco.

        Args:
            url (str): URL a ser verificada.

        Returns:
            bool: True se a URL estiver cadastrada, False caso contrário.
        """
        return url.strip() in self._urls

    def adicionar(self, url: str) -> bool:
        """
        Cadastra uma nova URL no banco e salva no arquivo.

        Args:
            url (str): URL a ser cadastrada.

        Returns:
            bool: True se adicionada com sucesso, False se já existia ou formato inválido.

        Raises:
            ValueError: Se o formato da URL for inválido.
        """
        url = url.strip()

        if not self.validar_formato(url):
            raise ValueError(f"Formato de URL inválido: '{url}'")

        if self.existe(url):
            return False  # já cadastrada

        self._urls.add(url)
        self._salvar_url_no_arquivo(url)
        return True

    def _salvar_url_no_arquivo(self, url: str) -> None:
        """
        Appenda uma nova URL ao arquivo de persistência.

        Args:
            url (str): URL a ser salva.
        """
        try:
            with open(self._arquivo, "a", encoding="utf-8") as f:
                f.write(url + "\n")
        except OSError as e:
            print(f"[AVISO] Não foi possível salvar no arquivo: {e}")

    def listar(self) -> list:
        """
        Retorna a lista de todas as URLs cadastradas, ordenadas alfabeticamente.

        Returns:
            list: Lista de URLs cadastradas.
        """
        return sorted(self._urls)

    def total(self) -> int:
        """
        Retorna o número de URLs cadastradas.

        Returns:
            int: Quantidade de URLs no banco.
        """
        return len(self._urls)
