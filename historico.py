# historico.py
# controla o historico de navegacao do browser
# usa uma pilha pra guardar as paginas visitadas
# Grupo 05 - Enquanto Funcionar Ta Bom

class Historico:
    # pilha de paginas visitadas
    # funciona como LIFO: ultima que entrou, primeira a sair no #back

    def __init__(self):
        self._paginas = []

    def adicionar(self, url):
        # nao deixa adicionar url vazia
        if not url or not url.strip():
            raise ValueError("URL vazia nao pode entrar no historico")
        self._paginas.append(url.strip())

    def voltar(self):
        # tira e retorna a ultima pagina (comando #back)
        if self.esta_vazio():
            raise IndexError("Nao tem pagina anterior no historico")
        return self._paginas.pop()

    def ultima_pagina(self):
        # ve o topo sem remover
        if self.esta_vazio():
            return ""
        return self._paginas[-1]

    def esta_vazio(self):
        return len(self._paginas) == 0

    def listar(self):
        # retorna copia pra nao mexer na lista original
        return list(self._paginas)

    def __str__(self):
        if self.esta_vazio():
            return "[ ]"
        return " ".join(f"[{p}]" for p in self._paginas)
