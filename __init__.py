from flask import Flask, request, render_template
import requests


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

@app.route("/buscar")
def buscar():

    pokemon = request.args.get("q")

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}".lower()

    resposta = requests.get(url)
    
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
    lideres = [lider for lider, time in LIDERES_GINASIO.items() if nome in time]


    return render_template(
        "index.html",
        id=id_pokemon,
        nome=nome,
        peso=peso,
        regiao=regiao,
        imagem=imagem,
        tipos=tipos,
        lideres=lideres
    )
        
    

if __name__ == "__main__":
    app.run(debug=True)