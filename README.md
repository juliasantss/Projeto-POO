# 🌐 Browser Simulator

Simulador de navegação web via linha de comando desenvolvido em Python.

**Grupo 05 - Enquanto Funcionar Tá Bom**  
Júlia Beatriz · Nilson Vinícius · Wellington Antonio  
Disciplina: Programação Orientada a Objetos - IFPB · 2026.1

---

## 📋 Sobre o projeto

O Browser Simulator simula o funcionamento básico de um navegador web no terminal. O usuário digita URLs, navega por páginas internas, mantém um histórico de visitas e usa comandos especiais como `#back` e `#favoritos`.

O projeto foi desenvolvido em dois checkpoints:

- **CP1** - estrutura base: histórico de navegação, banco de URLs e comandos principais
- **CP2** - páginas internas: árvore de URLs, exibição de conteúdo de arquivos e novos comandos

---

## 🗂️ Estrutura de arquivos

```
Projeto-POO/
├── browser.py        # programa principal - loop de interação
├── banco_urls.py     # banco de URLs com estrutura de árvore (CP2)
├── historico.py      # pilha de navegação (LIFO)
├── favoritos.py      # gerenciamento de páginas favoritas
├── config.py         # configurações do browser (home page padrão)
├── urls.txt          # banco inicial de URLs com arquivos associados
├── paginas/          # arquivos de conteúdo de cada URL
│   ├── ifpb.txt
│   ├── ifpb_tsi.txt
│   ├── ifpb_tsi_alunos.txt
│   ├── ifpb_tsi_professores.txt
│   ├── ifpb_rc.txt
│   ├── ifpb_rc_coordenacao.txt
│   └── ifpb_rc_matriz.txt
├── favoritos.txt     # gerado automaticamente ao usar #favoritos
├── config.txt        # gerado automaticamente ao usar #sethome
└── .gitignore
```

---

## ⚙️ Requisitos

- Python 3.8 ou superior
- Biblioteca `colorama` (para cores no terminal)

```bash
pip install colorama
```

---

## ▶️ Como rodar

```bash
python browser.py
```

O terminal deve ser aberto na pasta raiz do projeto (onde está o `browser.py`).

---

## 🖥️ Comandos disponíveis

| Comando | Descrição |
|---|---|
| `#help` | Lista todos os comandos disponíveis |
| `#back` | Volta para a última página visitada |
| `#showhist` | Exibe o histórico completo de navegação |
| `#favoritos` | Gerencia as páginas favoritas |
| `#sethome` | Define a página atual como home padrão |
| `#add <url>` | Cadastra uma nova URL no banco |
| `#add <url> <arquivo>` | Cadastra URL com arquivo de conteúdo associado |
| `#sair` | Encerra o programa |
| `/caminho` | Navega para uma subpágina da URL atual |

### Exemplos de navegação

```
url: www.ifpb.edu.br          → acessa a URL raiz
url: /tsi                      → navega para www.ifpb.edu.br/tsi
url: /alunos                   → navega para www.ifpb.edu.br/tsi/alunos
url: #add www.meusite.com.br   → cadastra nova URL
url: #add www.site.com/sobre paginas/sobre.txt   → cadastra com arquivo
```

---

## 🗄️ Formato do urls.txt

Cada linha representa uma URL e, opcionalmente, o arquivo de conteúdo associado:

```
# comentários são ignorados
www.ifpb.edu.br paginas/ifpb.txt
www.ifpb.edu.br/tsi paginas/ifpb_tsi.txt
www.ifpb.edu.br/tsi/alunos paginas/ifpb_tsi_alunos.txt
www.google.com.br paginas/google.txt
```

---

## 🏗️ Estrutura de dados

### Historico (historico.py)
Pilha **LIFO** implementada com lista Python. Cada página visitada é empilhada com `append()` e desempilhada com `pop()` no `#back`.

```
Navega:  ifpb → google → youtube
Pilha:   [ifpb, google]   home: youtube

#back:   [ifpb]           home: google
#back:   []               home: ifpb
```

### BancoURLs (banco_urls.py)
Dicionário aninhado que representa a hierarquia de URLs como uma árvore. Cada nó contém o arquivo de conteúdo e os filhos (subpáginas).

```python
{
  "www.ifpb.edu.br": {
    "arquivo": "paginas/ifpb.txt",
    "filhos": {
      "tsi": {
        "arquivo": "paginas/ifpb_tsi.txt",
        "filhos": {
          "alunos": { "arquivo": "paginas/ifpb_tsi_alunos.txt", "filhos": {} },
          "professores": { "arquivo": "...", "filhos": {} }
        }
      },
      "rc": { ... }
    }
  }
}
```

---

## ⭐ Diferenciais do grupo

Além dos requisitos obrigatórios, o grupo implementou:

**Cores no terminal** - usando `colorama`:
- 🟢 Verde → sucesso (`[200 OK]`, mensagens positivas)
- 🔴 Vermelho → erro (`[404]`, erros de formato)
- 🟡 Amarelo → avisos (histórico vazio, duplicatas)
- 🔵 Ciano → informações (histórico, links disponíveis)

**Contador de visitas** - exibido no cabeçalho a cada iteração, contabiliza apenas navegações bem-sucedidas.

**`#favoritos`** - adiciona ou remove a página atual dos favoritos. Lista persiste em `favoritos.txt` entre sessões.

**`#sethome`** - define a página atual como home padrão. Na próxima abertura do browser, o programa já começa nessa página. Configuração salva em `config.txt`.

---

## 🧪 Testes

Para testar as classes sem o loop interativo:

```python
from historico import Historico
from banco_urls import BancoURLs

# testa historico
h = Historico()
h.adicionar("www.ifpb.edu.br")
h.adicionar("www.google.com.br")
print(h)           # [www.ifpb.edu.br] [www.google.com.br]
print(h.voltar())  # www.google.com.br
print(h)           # [www.ifpb.edu.br]

# testa banco
b = BancoURLs("urls.txt")
print(b.existe("www.ifpb.edu.br"))          # True
print(b.links_internos("www.ifpb.edu.br"))  # ['/tsi', '/rc']
print(b.arquivo_da_url("www.ifpb.edu.br"))  # paginas/ifpb.txt
```

---

## 📌 Conceitos de POO aplicados

| Conceito | Onde aparece |
|---|---|
| **Encapsulamento** | Atributos privados `_paginas`, `_urls`, `_arvore`, `_lista` |
| **Modularização** | 5 arquivos com responsabilidades separadas |
| **Tratamento de exceções** | `ValueError`, `IndexError`, `FileNotFoundError` em todos os módulos |
| **Método especial** | `__str__` na classe `Historico` |
| **Atributo de classe** | `_FORMATO_URL` em `BancoURLs` |
| **Estruturas de dados** | Pilha (`Historico`), árvore/dicionário aninhado (`BancoURLs`), conjunto (`set`) |

---

## 👥 Divisão do grupo

| Membro | Responsabilidade |
|---|---|
| Julia Beatriz | `browser.py` - loop principal, navegação, diferenciais visuais |
| Nilson Vinícius | `banco_urls.py`, `favoritos.py` - banco de dados e favoritos |
| Wellington Antonio | `historico.py`, `config.py` - pilha de navegação e configurações |
