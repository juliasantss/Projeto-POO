# favoritos.py
# guarda as paginas favoritas do usuario
# persiste num arquivo pra nao perder entre sessoes
# Grupo 05 - Enquanto Funcionar Ta Bom

class Favoritos:

    def __init__(self, arquivo="favoritos.txt"):
        self._lista   = []
        self._arquivo = arquivo
        self._carregar()

    def _carregar(self):
        # le os favoritos salvos de sessoes anteriores
        try:
            with open(self._arquivo, "r", encoding="utf-8") as f:
                for linha in f:
                    url = linha.strip()
                    if url and url not in self._lista:
                        self._lista.append(url)
        except FileNotFoundError:
            pass  # primeira vez rodando, arquivo nao existe ainda

    def _salvar(self):
        # reescreve o arquivo com a lista atual
        try:
            with open(self._arquivo, "w", encoding="utf-8") as f:
                for url in self._lista:
                    f.write(url + "\n")
        except OSError as e:
            print(f"  [!] Nao salvou favoritos: {e}")

    def adicionar(self, url):
        # adiciona a url nos favoritos se ainda nao estiver
        if not url or not url.strip():
            raise ValueError("URL vazia")
        if url in self._lista:
            return False  # ja ta nos favoritos
        self._lista.append(url)
        self._salvar()
        return True

    def remover(self, url):
        # remove a url dos favoritos
        if url not in self._lista:
            return False
        self._lista.remove(url)
        self._salvar()
        return True

    def listar(self):
        return list(self._lista)

    def vazio(self):
        return len(self._lista) == 0
