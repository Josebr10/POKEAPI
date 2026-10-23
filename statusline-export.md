# Status line do Claude Code — exportação

Documento autocontido para reproduzir esta status line em outra máquina. Copie os três blocos de código para os caminhos indicados e reinicie o Claude Code.

## O que ela mostra

```
📊 ━━━━━━╌╌╌╌╌╌╌╌ 61K
🧠 Fable 5.1  ⚡ high  💰 $1.23
```

- **Linha 1**: barra de 14 células com o consumo de contexto e o total em K tokens. A cor vai de ciano → azul → azul-aço → laranja → vermelho; laranja só entra acima de 70% do teto (140K) e o vermelho satura no teto. Passou do teto, aparece um `+` no fim da barra.
- **Linha 2**: modelo em branco, esforço em violeta (mais vivo quanto maior o nível) e custo acumulado em USD.
- **Linha 3**: uma linha "vazia" (U+2800, braille em branco) que dá respiro entre a status line e os badges do rodapé, sobrevivendo ao trim do Claude Code.

## Pré-requisitos

- **Git Bash** (o comando roda via `bash`).
- **Python 3** no `PATH` como `python` (ou exporte `CLAUDE_PY` apontando para o executável). Substitui o `jq`, que o Smart App Control do Windows 11 bloqueia.

## Arquivos

### 1. `~/.claude/settings.json` — trecho a acrescentar

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/statusline-command.sh"
  }
}
```

### 2. `~/.claude/statusline-command.sh`

```bash
#!/usr/bin/env bash
# Claude Code statusLine: linha 1 = 📊 context tokens; linha 2 = 🧠 model  ⚡ effort
input=$(cat)

# Extracao dos 4 campos numa passagem so. Nao usamos `jq`: o Smart App Control
# do Windows 11 bloqueia o jq.exe do Chocolatey, e o script silenciava inteiro
# (todos os campos vazios => nenhuma linha impressa => status line some).
PY="${CLAUDE_PY:-python}"
{
    read -r model
    read -r used_tokens
    read -r effort
    read -r cost
} < <(printf '%s' "$input" | "$PY" "$HOME/.claude/lib/json-get.py" \
    'model.display_name' \
    'context_window.used_tokens|context_window.tokens_used|context_window.total_input_tokens|context_window.input_tokens' \
    'effort.level' \
    'cost.total_cost_usd')

esc=$'\033'

reset="${esc}[0m"
cap=140000     # teto do contexto: barra cheia e cor saturada
bar_w=14       # celulas da barra de progresso

# Paleta unica do contexto (ciano -> azul -> azul-aco -> laranja -> vermelho).
# Define r/g/b para um dado numero de tokens; barra e valor consomem daqui.
# Corte 70/30: tons calmos ocupam ate 70% do teto; laranja so entra ai e o
# vermelho satura no teto — o alerta fica no fim, nao no meio.
grad_rgb() {
    local t=$1 p len r0 g0 b0 r1 g1 b1
    if [ "$t" -gt "$cap" ]; then t=$cap; fi
    if [ "$t" -le 49000 ]; then
        p=$t; len=49000
        r0=34;  g0=211; b0=238
        r1=91;  g1=141; b1=239
    elif [ "$t" -le 98000 ]; then
        p=$(( t - 49000 )); len=49000
        r0=91;  g0=141; b0=239
        r1=176; g1=196; b1=222
    elif [ "$t" -le 119000 ]; then
        p=$(( t - 98000 )); len=21000
        r0=176; g0=196; b0=222
        r1=251; g1=146; b1=60
    else
        p=$(( t - 119000 )); len=21000
        r0=251; g0=146; b0=60
        r1=255; g1=85;  b1=85
    fi
    r=$(( r0 + (r1 - r0) * p / len ))
    g=$(( g0 + (g1 - g0) * p / len ))
    b=$(( b0 + (b1 - b0) * p / len ))
}

line1=""
if [ -n "$used_tokens" ]; then
    tokens_int=$(printf '%.0f' "$used_tokens")
    k=$(( tokens_int / 1000 ))

    grad_rgb "$tokens_int"
    color="${esc}[1;38;2;${r};${g};${b}m"

    t_bar=$tokens_int
    if [ "$t_bar" -gt "$cap" ]; then t_bar=$cap; fi
    filled=$(( t_bar * bar_w / cap ))

    # barra inteira na cor do nivel atual — nao registra por onde passou
    bar="${esc}[38;2;${r};${g};${b}m"
    i=0
    while [ "$i" -lt "$bar_w" ]; do
        if [ "$i" -lt "$filled" ]; then
            bar="${bar}━"
        else
            bar="${bar}${esc}[38;2;68;68;68m╌"
        fi
        i=$(( i + 1 ))
    done
    # passou do teto: "+" na cor da barra — ainda ha contexto, mas nao convem seguir
    if [ "$tokens_int" -gt "$cap" ]; then
        bar="${bar}${esc}[38;2;${r};${g};${b}m+"
    fi
    bar="${bar}${reset}"

    line1="📊 ${bar} ${color}${k}K${reset}"
fi

white="${esc}[38;2;255;255;255m"
line2=""
[ -n "$model" ] && line2="🧠 ${white}${model}${esc}[0m"

# paleta do esforco: quanto maior, mais vivo o violeta
if [ -n "$effort" ]; then
    case "$effort" in
        low)    er=148; eg=163; eb=184 ;;
        medium) er=165; eg=180; eb=252 ;;
        high)   er=167; eg=139; eb=250 ;;
        xhigh)  er=192; eg=132; eb=252 ;;
        max)    er=217; eg=70;  eb=239 ;;
        *)      er=148; eg=163; eb=184 ;;
    esac
    line2="${line2:+$line2  }⚡ ${esc}[38;2;${er};${eg};${eb}m${effort}${esc}[0m"
fi

if [ -n "$cost" ]; then
    cost_fmt=$(printf '%.2f' "$cost")
    line2="${line2:+$line2  }💰 ${white}\$${cost_fmt}${esc}[0m"
fi

# linha final "vazia": respiro entre a statusline e os badges do footer.
# U+2800 (braille em branco) porque nao e whitespace — sobrevive ao trim de
# linha em branco do Claude Code — mas renderiza invisivel.
blank=$'⠀'
if [ -n "$line1" ] && [ -n "$line2" ]; then
    printf '%s\n%s\n%s' "$line1" "$line2" "$blank"
elif [ -n "$line1$line2" ]; then
    printf '%s\n%s' "${line1}${line2}" "$blank"
fi
```

### 3. `~/.claude/lib/json-get.py`

Só o modo de caminhos (`json-get.py <caminho> ...`) é usado pela status line; os modos `--find` e `--encode` atendem outros hooks e podem ficar, pois não custam nada.

```python
#!/usr/bin/env python3
"""Leitor de JSON para os scripts de shell do Claude Code — substitui o `jq`.

O `jq.exe` do Chocolatey e bloqueado pelo Smart App Control do Windows 11
(mensagem "Device Guard"), o que apagava a status line e silenciava o hook do
Telegram. Este helper usa so a stdlib do Python, que o SAC aceita.

Tres modos, todos lendo JSON de stdin (ou de arquivos, onde indicado):

  json-get.py <caminho> [<caminho> ...]
      Imprime UMA LINHA por caminho, na ordem dos argumentos. Caminho e
      travessia por ponto (`model.display_name`), com indice inteiro para lista
      (`allowFrom.0`) e alternativas separadas por `|` — vale o primeiro que
      resolver para valor nao-nulo. Valor lista/dict imprime o COMPRIMENTO
      (cobre o `| length` do jq). Ausente/nulo => linha vazia.

  json-get.py --find <campo>=<valor> <caminho>[,<caminho>...] <arquivo> [...]
      Varre os arquivos, cada um um objeto JSON, e imprime <caminho> do
      PRIMEIRO cujo <campo> case com <valor>. Arquivo ilegivel ou invalido e
      pulado. Varios caminhos separados por virgula imprimem UMA LINHA cada,
      na ordem dada, todos do mesmo arquivo — uma so varredura resolve o
      registro inteiro (ex.: `name,pid,kind`). Nenhum arquivo casa => uma
      linha vazia por caminho.

  json-get.py --encode <chave>=<valor> [<chave>=<valor> ...]
      Imprime um objeto JSON com os pares dados. O valor `-` significa "le o
      texto de stdin" — o texto vai por stdin, nao por argumento, porque o Git
      Bash converte argumentos de .exe nativo para a codepage ANSI do Windows e
      corromperia os acentos.

Nunca falha por dado ruim: JSON invalido, stdin vazio ou caminho inexistente
saem como linha vazia, com codigo de saida 0. Quem chama nao precisa de
`2>/dev/null` nem de `|| true` para o caso normal de ausencia.
"""

import json
import sys


def _ler_json(fonte):
    """Decodifica JSON, devolvendo None em qualquer falha."""
    try:
        return json.loads(fonte)
    except (ValueError, TypeError):
        return None


def resolver(dados, caminho):
    """Percorre `caminho` (ponto-separado) em `dados`. None se nao existir."""
    atual = dados
    for parte in caminho.split("."):
        if isinstance(atual, dict):
            atual = atual.get(parte)
        elif isinstance(atual, list):
            try:
                indice = int(parte)
            except ValueError:
                return None
            atual = atual[indice] if -len(atual) <= indice < len(atual) else None
        else:
            return None
        if atual is None:
            return None
    return atual


def resolver_alternativas(dados, expressao):
    """`a.b|c.d` — primeiro caminho que der valor nao-nulo."""
    for caminho in expressao.split("|"):
        valor = resolver(dados, caminho)
        if valor is not None:
            return valor
    return None


def formatar(valor):
    """Renderiza escalar como texto; lista/dict viram o comprimento."""
    if valor is None:
        return ""
    if isinstance(valor, bool):
        return "true" if valor else "false"
    if isinstance(valor, (list, dict)):
        return str(len(valor))
    return str(valor)


def modo_caminhos(expressoes):
    dados = _ler_json(sys.stdin.read())
    for expressao in expressoes:
        valor = None if dados is None else resolver_alternativas(dados, expressao)
        print(formatar(valor))


def modo_find(criterio, caminhos, arquivos):
    campo, _, esperado = criterio.partition("=")
    # Varios caminhos numa varredura so: quem chama de um hook paga o custo de
    # subir o Python uma vez, nao uma vez por campo do mesmo registro.
    caminhos = caminhos.split(",")
    for nome in arquivos:
        try:
            with open(nome, encoding="utf-8", errors="replace") as arquivo:
                dados = _ler_json(arquivo.read())
        except OSError:
            continue
        if dados is None:
            continue
        if formatar(resolver(dados, campo)) == esperado:
            for caminho in caminhos:
                print(formatar(resolver(dados, caminho)))
            return
    for _ in caminhos:
        print("")


def modo_encode(pares):
    texto = None
    objeto = {}
    for par in pares:
        chave, _, valor = par.partition("=")
        if valor == "-":
            if texto is None:
                texto = sys.stdin.read()
            valor = texto
        objeto[chave] = valor
    sys.stdout.write(json.dumps(objeto, ensure_ascii=False))


def main(argv):
    # UTF-8 explicito nas duas pontas: o console do Windows entrega cp1252 por
    # padrao e comeria os acentos das mensagens do Telegram.
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")

    if not argv:
        return 0
    if argv[0] == "--encode":
        modo_encode(argv[1:])
    elif argv[0] == "--find":
        if len(argv) < 4:
            return 0
        modo_find(argv[1], argv[2], argv[3:])
    else:
        modo_caminhos(argv)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

## Instalação

1. Crie `~/.claude/lib/` e salve o `json-get.py` lá.
2. Salve o `statusline-command.sh` em `~/.claude/` (salve em UTF-8 sem BOM e com fim de linha LF; o `.editorconfig` ou o editor cuidam disso).
3. Acrescente o bloco `statusLine` ao `~/.claude/settings.json` (se o arquivo já tiver outras chaves, só inclua a chave `statusLine` no objeto raiz).
4. Reinicie o Claude Code.

## Teste rápido sem abrir o Claude Code

```bash
printf '%s' '{"model":{"display_name":"Fable 5.1"},"context_window":{"used_tokens":61000},"effort":{"level":"high"},"cost":{"total_cost_usd":1.234}}' | bash ~/.claude/statusline-command.sh
```

Saída esperada: as duas linhas coloridas do exemplo no início mais a linha invisível. Se nada aparecer, o helper Python não rodou: confira `python --version` no Git Bash ou defina `CLAUDE_PY`.

## Ajustes comuns

| O que mudar | Onde |
|---|---|
| Teto do contexto (barra cheia) | `cap=140000` |
| Largura da barra | `bar_w=14` |
| Cores por faixa de tokens | função `grad_rgb` |
| Cores do esforço | `case "$effort"` |
| Remover o custo | apague o bloco `if [ -n "$cost" ]` |
