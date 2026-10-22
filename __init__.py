from flask import Flask, request, render_template, jsonify, abort
import requests
import time


app = Flask(__name__)

LIDERES_GINASIO = {
    "Brock": ["geodude", "onix"],
    "Misty": ["staryu", "starmie"],
    "Lt. Surge": ["voltorb", "pikachu", "raichu"],
    "Erika": ["victreebel", "tangela", "vileplume"],
    "Koga": ["koffing", "muk", "weezing"],
    "Sabrina": ["kadabra", "mr-mime", "venomoth", "alakazam"],
    "Blaine": ["growlithe", "ponyta", "rapidash", "arcanine"],
    "Giovanni": ["rhyhorn", "dugtrio", "nidoqueen", "nidoking", "rhydon"],
}


@app.route("/")
def index():

    return (render_template("index.html"))

nomes_pokemon = []


@app.route("/sugestoes")
def sugestoes():

    global nomes_pokemon

    if not nomes_pokemon:
        resposta = requests.get("https://pokeapi.co/api/v2/pokemon?limit=2000")
        nomes_pokemon = [p["name"] for p in resposta.json()["results"]]

    texto = request.args.get("q", "").strip().lower()

    if not texto:
        return jsonify([])

    return jsonify([n for n in nomes_pokemon if n.startswith(texto)][:8])


GERACOES = [
    {"numero": 1, "regiao": "Kanto"},
    {"numero": 2, "regiao": "Johto"},
    {"numero": 3, "regiao": "Hoenn"},
    {"numero": 4, "regiao": "Sinnoh"},
    {"numero": 5, "regiao": "Unova"},
    {"numero": 6, "regiao": "Kalos"},
    {"numero": 7, "regiao": "Alola"},
    {"numero": 8, "regiao": "Galar"},
    {"numero": 9, "regiao": "Paldea"},
]

geracoes_cache = {}


def obter_geracao(numero):

    if numero not in geracoes_cache:
        resposta = requests.get(f"https://pokeapi.co/api/v2/generation/{numero}", timeout=10)
        resposta.raise_for_status()

        especies = resposta.json()["pokemon_species"]
        pokemons = [
            {"id": int(e["url"].rstrip("/").split("/")[-1]), "nome": e["name"]}
            for e in especies
        ]
        geracoes_cache[numero] = sorted(pokemons, key=lambda p: p["id"])

    return geracoes_cache[numero]


@app.route("/geracoes")
def geracoes():

    return render_template("geracoes.html", geracoes=GERACOES)


@app.route("/geracoes/<int:numero>")
def geracao(numero):

    atual = next((g for g in GERACOES if g["numero"] == numero), None)

    if atual is None:
        abort(404)

    try:
        pokemons = obter_geracao(numero)
    except requests.RequestException:
        return render_template("geracao.html", geracoes=GERACOES, atual=atual, pokemons=None), 502

    return render_template("geracao.html", geracoes=GERACOES, atual=atual, pokemons=pokemons)


@app.route("/recentes")
def recentes():

    return render_template("recentes.html")


@app.route("/favoritos")
def favoritos():

    return render_template("favoritos.html")


@app.route("/status")
def status():

    inicio = time.perf_counter()

    try:
        resposta = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1", timeout=5)
        online = resposta.status_code == 200
    except requests.RequestException:
        online = False

    ms = round((time.perf_counter() - inicio) * 1000)

    return jsonify({"online": online, "ms": ms})


@app.route("/buscar")
def buscar():

    pokemon = request.args.get("q")

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}".lower()

    try:
        resposta = requests.get(url, timeout=10)
    except requests.RequestException:
        return render_template("index.html", erro="indisponivel", termo=pokemon)

    if resposta.status_code == 404:
        return render_template("index.html", erro="nao_encontrado", termo=pokemon)

    dados = resposta.json()



    
    nome = dados["name"]
    id_pokemon = dados["id"]
    peso = dados["weight"] / 10
    url_encontros = dados["location_area_encounters"]

    resposta_encontros = requests.get(url_encontros)

    encontros = resposta_encontros.json()

    regiao = encontros[0]["location_area"]["name"] if encontros else "Desconhecido"
    imagem = dados["sprites"]["front_default"]
    tipos = [t["type"]["name"] for t in dados["types"]]
    som = dados.get("cries", {}).get("latest")
    lideres = [lider for lider, time in LIDERES_GINASIO.items() if nome in time]


    return render_template(
        "index.html",
        id=id_pokemon,
        nome=nome,
        peso=peso,
        regiao=regiao,
        imagem=imagem,
        som=som,
        tipos=tipos,
        lideres=lideres
    )
        
    

if __name__ == "__main__":
    app.run(debug=True)