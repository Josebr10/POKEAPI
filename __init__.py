from flask import Flask, request, render_template
import requests


app = Flask(__name__)


@app.route("/")
def index():

    return (render_template("index.html"))

@app.route("/buscar")
def buscar():

    pokemon = request.args.get("q")

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}".lower()

    resposta = requests.get(url)
    
    dados =resposta.json()



    
    nome = dados["name"]
    id_pokemon = dados["id"]
    peso = dados["weight"] / 10
    url_encontros = dados["location_area_encounters"]

    resposta_encontros = requests.get(url_encontros)

    encontros = resposta_encontros.json()

    regiao = encontros[0]["location_area"]["name"] if encontros else "Desconhecido"
    imagem = dados["sprites"]["front_default"]
    tipos = [t["type"]["name"] for t in dados["types"]]


    return render_template(
        "index.html",
        id=id_pokemon,
        nome=nome,
        peso=peso,
        regiao=regiao,
        imagem=imagem,
        tipos=tipos
    )
        
    

if __name__ == "__main__":
    app.run(debug=True)