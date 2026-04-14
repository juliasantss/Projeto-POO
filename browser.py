"""
browser.py
Programa principal do Browser Simulator.

Simula a navegação no terminal com histórico, banco de URLs
e comandos como #back, #add e #sair.

Grupo: Enquanto Funcionar Tá Bom
Disciplina: Programação Orientada a Objetos
"""

from historico import Historico
from banco_urls import BancoURLs


# Comandos especiais
CMD_BACK     = "#back"
CMD_SAIR     = "#sair"
CMD_SHOWHIST = "#showhist"
CMD_ADD      = "#add"


def exibir_cabecalho(historico: Historico, home: str) -> None:
    """
    Mostra o estado atual do browser (histórico e página atual).
    """
    print("\n" + "=" * 55)
    print(f"  Histórico de Visitas: {historico}")
    print(f"  Home: [{home}]" if home else "  Home: [ ]")
    print("=" * 55)
    print("  Digite uma url ou comando (#back, #sair...)")
    print("-" * 55)


def processar_add(entrada: str, banco: BancoURLs) -> None:
    """
    Adiciona uma nova URL usando o comando #add.
    """
    partes = entrada.split(maxsplit=1)

    if len(partes) < 2 or not partes[1].strip():
        print("\n  [ERRO] Uso correto: #add <url>")
        return

    nova_url = partes[1].strip()

    try:
        adicionada = banco.adicionar(nova_url)

        if adicionada:
            print(f"\n  [OK] URL '{nova_url}' cadastrada!")
        else:
            print(f"\n  [AVISO] URL já existe.")
    except ValueError as e:
        print(f"\n  [ERRO] {e}")


def processar_back(historico: Historico, home: str) -> str:
    """
    Volta para a página anterior (#back).
    """
    try:
        pagina_anterior = historico.voltar()
        print(f"\n  [BACK] Voltando para: {pagina_anterior}")
        return pagina_anterior
    except IndexError:
        print("\n  [AVISO] Histórico vazio.")
        return home


def processar_showhist(historico: Historico, home: str) -> None:
    """
    Mostra o histórico completo de navegação.
    """
    print("\n  ── Histórico ──")

    paginas = historico.listar()

    if not paginas:
        print("  (nenhuma página visitada)")
    else:
        for i, url in enumerate(paginas, start=1):
            print(f"  {i}. {url}")

    print(f"  Atual: [{home}]" if home else "  Atual: [ ]")
    print("  ───────────────")


def navegar(url: str, historico: Historico, home: str, banco: BancoURLs) -> str:
    """
    Faz a navegação para uma URL.

    Se existir no banco → sucesso (200)
    Se não existir → erro (404)
    """
    if banco.existe(url):

        if home:
            historico.adicionar(home)

        print(f"\n  [200 OK] Página encontrada!")
        return url

    else:
        print(f"\n  [404] Página não encontrada: '{url}'")
        return home


def executar_browser() -> None:
    """
    Loop principal do programa.
    Controla toda interação com o usuário.
    """
    print("\n" + "█" * 55)
    print("  🌐 BROWSER SIMULATOR")
    print("  Grupo: Enquanto Funcionar Tá Bom")
    print("█" * 55)

    banco = BancoURLs("urls.txt")
    historico = Historico()
    home = ""

    print(f"\n  [{banco.total()} URLs carregadas]")

    while True:
        exibir_cabecalho(historico, home)

        try:
            entrada = input("  url: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  [ENCERRADO] Browser fechado.")
            break

        if not entrada:
            continue

        entrada_lower = entrada.lower()

        # Comandos especiais
        if entrada_lower == CMD_SAIR:
            print("\n  [ENCERRADO] Até logo! 👋")
            break

        elif entrada_lower == CMD_BACK:
            home = processar_back(historico, home)

        elif entrada_lower == CMD_SHOWHIST:
            processar_showhist(historico, home)
            input("\n  [ENTER para continuar]")

        elif entrada_lower.startswith(CMD_ADD):
            processar_add(entrada, banco)
            input("\n  [ENTER para continuar]")

        # Navegação normal
        else:
            home = navegar(entrada, historico, home, banco)


# Ponto de entrada do programa
if __name__ == "__main__":
    executar_browser()
