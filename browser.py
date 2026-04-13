"""
browser.py
----------
Programa principal do Browser Simulator - Checkpoint 1.

Simula a navegação em websites via linha de comando, com histórico
de navegação, banco de URLs e comandos especiais (#back, #sair, etc).

Grupo 05 - Enquanto Funcionar Tá Bom
Disciplina: Programação Orientada a Objetos
"""

from historico import Historico
from banco_urls import BancoURLs


# ─────────────────────────────────────────────
#  Constantes de comandos especiais
# ─────────────────────────────────────────────
CMD_BACK     = "#back"
CMD_SAIR     = "#sair"
CMD_SHOWHIST = "#showhist"
CMD_ADD      = "#add"


def exibir_cabecalho(historico: Historico, home: str) -> None:
    """
    Exibe o cabeçalho do browser com histórico e página atual.

    Args:
        historico (Historico): Objeto com o histórico de navegação.
        home (str): URL da página atualmente em exibição.
    """
    print("\n" + "=" * 55)
    print(f"  Histórico de Visitas: {historico}")
    print(f"  Home: [{home}]" if home else "  Home: [ ]")
    print("=" * 55)
    print("  Digite a url ou um comando especial (#back, #sair...)")
    print("-" * 55)


def processar_add(entrada: str, banco: BancoURLs) -> None:
    """
    Processa o comando #add para cadastrar uma nova URL.

    Args:
        entrada (str): Linha completa digitada pelo usuário (ex: '#add www.site.com').
        banco (BancoURLs): Banco de URLs onde a nova URL será cadastrada.
    """
    partes = entrada.split(maxsplit=1)
    if len(partes) < 2 or not partes[1].strip():
        print("\n  [ERRO] Uso correto: #add <url>")
        print("  Exemplo: #add www.meusite.com.br")
        return

    nova_url = partes[1].strip()
    try:
        adicionada = banco.adicionar(nova_url)
        if adicionada:
            print(f"\n  [OK] URL '{nova_url}' cadastrada com sucesso!")
        else:
            print(f"\n  [AVISO] A URL '{nova_url}' já está cadastrada.")
    except ValueError as e:
        print(f"\n  [ERRO] {e}")


def processar_back(historico: Historico, home: str) -> str:
    """
    Processa o comando #back, retornando à última página visitada.

    Args:
        historico (Historico): Objeto com o histórico de navegação.
        home (str): URL da página atual.

    Returns:
        str: A URL da página anterior (novo home), ou home atual se histórico vazio.
    """
    try:
        pagina_anterior = historico.voltar()
        print(f"\n  [BACK] Retornando para: {pagina_anterior}")
        return pagina_anterior
    except IndexError:
        print("\n  [AVISO] Não há página anterior no histórico.")
        return home


def processar_showhist(historico: Historico, home: str) -> None:
    """
    Exibe o histórico completo de navegação.

    Args:
        historico (Historico): Objeto com o histórico de navegação.
        home (str): URL da página atual.
    """
    print("\n  ── Histórico de Navegação ──")
    paginas = historico.listar()
    if not paginas:
        print("  (nenhuma página visitada anteriormente)")
    else:
        for i, url in enumerate(paginas, start=1):
            print(f"  {i}. {url}")
    print(f"  → Posição atual: [{home}]" if home else "  → Posição atual: [ ]")
    print("  ────────────────────────────")


def navegar(url: str, historico: Historico, home: str, banco: BancoURLs) -> str:
    """
    Processa uma requisição de navegação para uma URL.

    Se a URL existir no banco, registra a página atual no histórico
    e atualiza o home. Caso contrário, exibe erro 404.

    Args:
        url (str): URL digitada pelo usuário.
        historico (Historico): Objeto com o histórico de navegação.
        home (str): URL da página atual.
        banco (BancoURLs): Banco de URLs para verificação.

    Returns:
        str: O novo home após a navegação (ou o home atual se a URL for inválida).
    """
    if banco.existe(url):
        # Só registra no histórico se já havia uma página sendo visitada
        if home:
            historico.adicionar(home)
        print(f"\n  [200 OK] Página encontrada!")
        return url
    else:
        print(f"\n  [404] Página não encontrada: '{url}'")
        return home


def executar_browser() -> None:
    """
    Loop principal do browser. Gerencia toda a interação com o usuário.
    """
    print("\n" + "█" * 55)
    print("  🌐  BROWSER SIMULATOR  |  Grupo 05")
    print("  Enquanto Funcionar Tá Bom™")
    print("█" * 55)

    banco    = BancoURLs("urls.txt")
    historico = Historico()
    home     = ""  # página atual (vazia no início)

    print(f"\n  [{banco.total()} URLs carregadas do banco]")

    while True:
        exibir_cabecalho(historico, home)

        try:
            entrada = input("  url: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  [ENCERRADO] Browser fechado.")
            break

        if not entrada:
            continue

        # ── Comandos especiais ──────────────────────────
        entrada_lower = entrada.lower()

        if entrada_lower == CMD_SAIR:
            print("\n  [ENCERRADO] Até logo! 👋")
            break

        elif entrada_lower == CMD_BACK:
            home = processar_back(historico, home)

        elif entrada_lower == CMD_SHOWHIST:
            processar_showhist(historico, home)
            input("\n  [Pressione ENTER para continuar]")

        elif entrada_lower.startswith(CMD_ADD):
            processar_add(entrada, banco)
            input("\n  [Pressione ENTER para continuar]")

        # ── Navegação normal ────────────────────────────
        else:
            home = navegar(entrada, historico, home, banco)


# ─────────────────────────────────────────────
#  Ponto de entrada
# ─────────────────────────────────────────────
if __name__ == "__main__":
    executar_browser()
