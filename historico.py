"""
historico.py
------------
Módulo responsável por gerenciar o histórico de navegação do browser.

Grupo 05 - Enquanto Funcionar Tá Bom
Disciplina: Programação Orientada a Objetos
"""


class Historico:
    """
    Representa o histórico de navegação do browser.

    O histórico funciona como uma pilha (LIFO): a última URL visitada
    é a primeira a ser recuperada com o comando #back.

    Attributes:
        _paginas (list): lista interna que armazena as URLs visitadas.
    """

    def __init__(self):
        """Inicializa o histórico vazio."""
        self._paginas = []

    def adicionar(self, url: str) -> None:
        """
        Adiciona uma URL ao histórico de navegação.

        Args:
            url (str): URL a ser registrada no histórico.

        Raises:
            ValueError: Se a URL fornecida for vazia ou None.
        """
        if not url or not url.strip():
            raise ValueError("Não é possível adicionar uma URL vazia ao histórico.")
        self._paginas.append(url.strip())

    def voltar(self) -> str:
        """
        Remove e retorna a última URL do histórico (comando #back).

        Returns:
            str: A URL mais recente do histórico.

        Raises:
            IndexError: Se o histórico estiver vazio.
        """
        if self.esta_vazio():
            raise IndexError("Histórico vazio. Não há página anterior para retornar.")
        return self._paginas.pop()

    def ultima_pagina(self) -> str:
        """
        Retorna a última URL do histórico sem removê-la.

        Returns:
            str: A URL mais recente, ou string vazia se o histórico estiver vazio.
        """
        if self.esta_vazio():
            return ""
        return self._paginas[-1]

    def esta_vazio(self) -> bool:
        """
        Verifica se o histórico está vazio.

        Returns:
            bool: True se vazio, False caso contrário.
        """
        return len(self._paginas) == 0

    def listar(self) -> list:
        """
        Retorna uma cópia da lista de URLs do histórico.

        Returns:
            list: Lista com todas as URLs visitadas, da mais antiga à mais recente.
        """
        return list(self._paginas)

    def __str__(self) -> str:
        """Representação textual do histórico no formato exibido pelo browser."""
        if self.esta_vazio():
            return "[ ]"
        return " ".join(f"[{url}]" for url in self._paginas)
