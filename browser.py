# browser.py
# programa principal do browser simulator
# Grupo 05 - Enquanto Funcionar Ta Bom

import os
from colorama import init, Fore, Style
from historico import Historico
from banco_urls import BancoURLs
from favoritos import Favoritos
from config    import carregar_home, salvar_home

# inicializa o colorama (necessario no windows)
init(autoreset=True)

# comandos disponiveis
CMD_BACK      = "#back"
CMD_SAIR      = "#sair"
CMD_SHOWHIST  = "#showhist"
CMD_ADD       = "#add"
CMD_HELP      = "#help"
CMD_FAVORITOS = "#favoritos"
CMD_SETHOME   = "#sethome"

# atalhos de cor
OK    = Fore.GREEN
ERRO  = Fore.RED
AVISO = Fore.YELLOW
INFO  = Fore.CYAN
RESET = Style.RESET_ALL


def cabecalho(hist, home, visitas):
    print("\n" + "=" * 55)
    print(f"  {INFO}Historico:{RESET} {hist}")
    print(f"  {INFO}Home     :{RESET} [{home}]" if home else f"  {INFO}Home     :{RESET} [ ]")
    print(f"  {INFO}Visitas  :{RESET} {visitas} pagina(s) nesta sessao")
    print("=" * 55)
    print("  Digite uma url ou comando (#help para ajuda)")
    print("-" * 55)


def mostrar_conteudo(url, banco):
    caminho = banco.arquivo_da_url(url)
    print(f"\n  url: {OK}{url}{RESET}")

    if not caminho or not os.path.exists(caminho):
        print(f"  {AVISO}<sem conteudo cadastrado para esta pagina>{RESET}")
        return

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            for linha in f:
                print(f"  {linha}", end="")
        print()
    except OSError as e:
        print(f"  {ERRO}[ERRO] Nao foi possivel ler o arquivo: {e}{RESET}")


def mostrar_links(url, banco):
    links = banco.links_internos(url)
    if links:
        print(f"\n  {INFO}Links disponiveis:{RESET}")
        for link in links:
            print(f"    {link}")


def cmd_help():
    print(f"\n  {INFO}-- Comandos disponiveis --{RESET}")
    print("  #help              -> exibe esta ajuda")
    print("  #back              -> volta pra pagina anterior")
    print("  #showhist          -> mostra o historico completo")
    print("  #favoritos         -> gerencia seus favoritos")
    print("  #sethome           -> define a pagina atual como home padrao")
    print("  #add <url>         -> cadastra uma nova url")
    print("    ex: #add www.meusite.com")
    print("    ex: #add www.meusite.com/pagina paginas/arq.txt")
    print("  #sair              -> encerra o programa")
    print(f"  {INFO}--------------------------{RESET}")
    print("  /caminho -> navega pra subpagina da url atual")
    print("    ex: /tsi   /alunos   /professores")
    print(f"  {INFO}--------------------------{RESET}")


def cmd_back(hist, home):
    try:
        anterior = hist.voltar()
        print(f"\n  {OK}<< Voltando para: {anterior}{RESET}")
        return anterior
    except IndexError:
        print(f"\n  {AVISO}[!] Historico vazio.{RESET}")
        return home


def cmd_showhist(hist, home):
    print(f"\n  {INFO}-- Historico --{RESET}")
    paginas = hist.listar()
    if not paginas:
        print("  (nenhuma pagina visitada ainda)")
    else:
        for i, url in enumerate(paginas, 1):
            print(f"  {i}. {url}")
    print(f"  Atual: [{home}]" if home else "  Atual: [ ]")
    print(f"  {INFO}----------------{RESET}")


def cmd_add(entrada, banco):
    partes = entrada.split(maxsplit=2)
    if len(partes) < 2 or not partes[1].strip():
        print(f"\n  {AVISO}[!] Uso: #add <url>  ou  #add <url> <arquivo.txt>{RESET}")
        return

    nova_url = partes[1].strip()
    arquivo  = partes[2].strip() if len(partes) > 2 else ""

    try:
        ok = banco.adicionar(nova_url, arquivo)
        if ok:
            print(f"\n  {OK}[+] '{nova_url}' cadastrada!{RESET}")
            if arquivo:
                print(f"  {OK}[+] Arquivo: '{arquivo}'{RESET}")
        else:
            print(f"\n  {AVISO}[!] '{nova_url}' ja existe no banco.{RESET}")
    except ValueError as e:
        print(f"\n  {ERRO}[ERRO] {e}{RESET}")


def cmd_favoritos(home, favs):
    print(f"\n  {INFO}-- Favoritos --{RESET}")
    lista = favs.listar()
    if favs.vazio():
        print("  (nenhum favorito salvo)")
    else:
        for i, url in enumerate(lista, 1):
            print(f"  {i}. {url}")
    print(f"  {INFO}----------------{RESET}")

    if not home:
        return

    if home in lista:
        print(f"  Pagina atual ja esta nos favoritos.")
        print(f"  Digite 'r' para remover ou ENTER para voltar: ", end="")
        acao = input().strip().lower()
        if acao == "r":
            favs.remover(home)
            print(f"  {AVISO}[-] '{home}' removido dos favoritos.{RESET}")
    else:
        print(f"  Digite 'a' para adicionar '{home}' ou ENTER para voltar: ", end="")
        acao = input().strip().lower()
        if acao == "a":
            favs.adicionar(home)
            print(f"  {OK}[+] '{home}' adicionado aos favoritos!{RESET}")


def cmd_sethome(home):
    if not home:
        print(f"\n  {AVISO}[!] Nenhuma pagina aberta para definir como home.{RESET}")
        return
    salvar_home(home)
    print(f"\n  {OK}[+] '{home}' definida como pagina inicial!{RESET}")
    print(f"  Na proxima vez que abrir o browser, vai comecar aqui.")


def navegar(entrada, hist, home, banco):
    if entrada.startswith("/"):
        if not home:
            print(f"\n  {AVISO}[!] Nenhuma pagina aberta. Digite uma URL primeiro.{RESET}")
            return home, False

        url_completa = banco.resolver_caminho(home, entrada)

        if banco.existe(url_completa):
            hist.adicionar(home)
            print(f"\n  {OK}[200 OK] Pagina encontrada!{RESET}")
            mostrar_conteudo(url_completa, banco)
            mostrar_links(url_completa, banco)
            return url_completa, True
        else:
            print(f"\n  {ERRO}[404] Pagina interna '{entrada}' nao encontrada.{RESET}")
            return home, False

    if banco.existe(entrada):
        if home:
            hist.adicionar(home)
        print(f"\n  {OK}[200 OK] Pagina encontrada!{RESET}")
        mostrar_conteudo(entrada, banco)
        mostrar_links(entrada, banco)
        return entrada, True
    else:
        print(f"\n  {ERRO}[404] '{entrada}' nao encontrada.{RESET}")
        return home, False


def iniciar():
    print("\n" + "#" * 55)
    print(f"  {OK}BROWSER SIMULATOR{RESET}")
    print("  Grupo 05 - Enquanto Funcionar Ta Bom")
    print("  #help para ver os comandos")
    print("#" * 55)

    banco   = BancoURLs("urls.txt")
    hist    = Historico()
    favs    = Favoritos("favoritos.txt")
    visitas = 0

    # carrega a home page salva da sessao anterior
    home = carregar_home()
    if home:
        print(f"\n  {INFO}[>>] Carregando home page: {home}{RESET}")
        if banco.existe(home):
            mostrar_conteudo(home, banco)
            mostrar_links(home, banco)
            visitas += 1
        else:
            print(f"  {AVISO}[!] Home page salva nao existe mais no banco.{RESET}")
            home = ""

    print(f"\n  [{banco.total()} URLs carregadas]\n")

    while True:
        cabecalho(hist, home, visitas)

        try:
            entrada = input("  url: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Encerrando...")
            break

        if not entrada:
            continue

        cmd = entrada.lower()

        if cmd == CMD_SAIR:
            print(f"\n  {OK}Ate mais! o/{RESET}")
            break

        elif cmd == CMD_HELP:
            cmd_help()
            input("\n  [ENTER para continuar]")

        elif cmd == CMD_BACK:
            home = cmd_back(hist, home)

        elif cmd == CMD_SHOWHIST:
            cmd_showhist(hist, home)
            input("\n  [ENTER para continuar]")

        elif cmd == CMD_FAVORITOS:
            cmd_favoritos(home, favs)
            input("\n  [ENTER para continuar]")

        elif cmd == CMD_SETHOME:
            cmd_sethome(home)
            input("\n  [ENTER para continuar]")

        elif cmd.startswith(CMD_ADD):
            cmd_add(entrada, banco)
            input("\n  [ENTER para continuar]")

        else:
            home, navegou = navegar(entrada, hist, home, banco)
            if navegou:
                visitas += 1


if __name__ == "__main__":
    iniciar()
