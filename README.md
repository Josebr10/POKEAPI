# POKEAPI

API de Pokémon desenvolvida em Flask para consultar informações de Pokémon e exibir detalhes como nome, peso, região, tipos e líderes de ginásio.

## Descrição

Este projeto consome a API pública da PokéAPI para buscar dados de Pokémon a partir de uma pesquisa na interface web. A aplicação monta uma página simples com as informações do Pokémon consultado e também identifica se ele pertence a algum time de líder de ginásio.

## Funcionalidades

- Busca de Pokémon por nome ou ID
- Exibição de imagem oficial
- Informações de peso, tipos e região de encontro
- Consulta à PokéAPI em tempo real
- Identificação de líderes de ginásio relacionados ao Pokémon
- Interface web em HTML/CSS

## Tecnologias

- Python
- Flask
- Requests
- HTML
- CSS

## Estrutura do projeto

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

## Pré-requisitos

- Python 3.9+
- pip

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/Josebr10/POKEAPI.git
cd POKEAPI
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Instale as dependências:

```bash
pip install flask requests
```

## Execução

No diretório raiz do projeto, execute:

```bash
python __init__.py
```

A aplicação será iniciada em:

```text
http://127.0.0.1:5000/
```

## Como usar

Na página inicial, pesquise um Pokémon, por exemplo:

```text
pikachu
```

A aplicação retorna dados como:

- nome
- ID
- peso
- imagem
- tipos
- região de encontro
- líderes de ginásio relacionados

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

## Autor

- Josebr10

## Observação

Como a aplicação utiliza a PokéAPI pública, a disponibilidade do serviço externo pode afetar o funcionamento em certos momentos.
