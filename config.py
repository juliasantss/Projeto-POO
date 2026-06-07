# config.py
# salva configuracoes do browser (home page)
# Grupo 05 - Enquanto Funcionar Ta Bom

import os

ARQUIVO_CONFIG = "config.txt"

def carregar_home():
    # le a home page salva, retorna vazia se nao existir
    try:
        with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
            for linha in f:
                chave, _, valor = linha.strip().partition("=")
                if chave.strip() == "home":
                    return valor.strip()
    except FileNotFoundError:
        pass
    return ""

def salvar_home(url):
    # salva a home page no arquivo de config
    config = {"home": url}

    # le outras configs que ja existam pra nao perder
    try:
        with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
            for linha in f:
                chave, _, valor = linha.strip().partition("=")
                if chave.strip() != "home":
                    config[chave.strip()] = valor.strip()
    except FileNotFoundError:
        pass

    try:
        with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
            for chave, valor in config.items():
                f.write(f"{chave} = {valor}\n")
    except OSError as e:
        print(f"  [!] Nao salvou config: {e}")
