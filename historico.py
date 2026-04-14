"""
historico.py
Módulo responsável por controlar o histórico de navegação.

Grupo: Enquanto Funcionar Tá Bom
Disciplina: Programação Orientada a Objetos
"""


class Historico:
    """
    Classe que representa o histórico do navegador.

    Funciona como uma pilha (LIFO):
    a última página acessada é a primeira a sair no #back.
    """

    def __init__(self):
        """Cria um histórico vazio."""
        self._paginas = []

    def adicionar(self, url: str) -> None:
        """
        Adiciona uma URL ao histórico.

        Raises:
            ValueError se a URL for vazia.
        """
        if not url or not url.strip():
            raise ValueError("Não é possível adicionar uma URL vazia.")
        self._paginas.append(url.strip())

    def voltar(self) -> str:
        """
        Remove e retorna a última página visitada (#back).

        Raises:
            IndexError se o histórico estiver vazio.
        """
        if self.esta_vazio():
            raise IndexError("Histórico vazio.")
        return self._paginas.pop()

    def ultima_pagina(self) -> str:
        """
        Retorna a última página sem remover.
        """
        if self.esta_vazio():
            return ""
        return self._paginas[-1]

    def esta_vazio(self) -> bool:
        """
        Verifica se o histórico está vazio.
        """
        return len(self._paginas) == 0

    def listar(self) -> list:
        """
        Retorna todas as páginas visitadas.
        """
        return list(self._paginas)

    def __str__(self) -> str:
        """
        Mostra o histórico no formato exibido no terminal.
        """
        if self.esta_vazio():
            return "[ ]"
        return " ".join(f"[{url}]" for url in self._paginas)
