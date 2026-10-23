# 🐾 POKEAPI

<div align="center">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png" alt="Pikachu" width="140" />
</div>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img alt="Flask" src="https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img alt="PokéAPI" src="https://img.shields.io/badge/Pok%C3%A9API-Data-FFCB05?style=for-the-badge&logo=githubactions&logoColor=black" />
</div>

Uma aplicação web em Python usando Flask para consultar Pokémon via a PokéAPI e exibir informações em uma interface simples e amigável.

## ✨ Funcionalidades

- Busca de Pokémon por nome ou ID
- Exibição de imagem oficial do Pokémon
- Informações como peso, tipos e região de encontro
- Consulta em tempo real à PokéAPI
- Identificação de líderes de ginásio relacionados ao Pokémon
- Layout simples em HTML/CSS

## 🧩 Tecnologias

- Python
- Flask
- Requests
- HTML
- CSS

## 📁 Estrutura do projeto

```text
POKEAPI/
├── __init__.py
├── APIpokemon
├── LICENSE
├── README.md
├── routes/
│   └── pokemon.py
├── static/
├── templates/
├── .gitignore
└── __pycache__/
```

## 🚀 Pré-requisitos

Antes de rodar o projeto, certifique-se de ter instalado:

- Python 3.9 ou superior
- pip

## 🛠️ Instalação

1. Clone o repositório:

```bash
git clone https://github.com/Josebr10/POKEAPI.git
cd POKEAPI
```

2. Crie um ambiente virtual:

```bash
python -m venv venv
```

3. Ative o ambiente virtual:

```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

4. Instale as dependências:

```bash
pip install flask requests
```

## ▶️ Como executar

No diretório raiz do projeto, execute:

```bash
python __init__.py
```

Depois, abra no navegador:

```text
http://127.0.0.1:5000/
```

## 🔎 Exemplo de uso

Na página inicial, pesquise um Pokémon como:

```text
pikachu
```

Você verá informações como:

- nome
- ID
- peso
- tipos
- imagem
- região de encontro
- líderes de ginásio relacionados

## 🧠 Como funciona

A aplicação envia uma requisição para a PokéAPI com o nome ou ID do Pokémon informado. Em seguida, processa os dados retornados e os apresenta na página web usando Flask e templates HTML.

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

- Josebr10

## ⚠️ Observação

Como o projeto depende da PokéAPI pública, a disponibilidade do serviço externo pode influenciar o funcionamento da aplicação em alguns momentos.

---

<p align="center">
  <i>Feito com ❤️ para explorar o mundo Pokémon.</i>
</p>
