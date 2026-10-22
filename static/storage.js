// Funções compartilhadas entre as páginas (histórico e favoritos no localStorage)
const SPRITE_URL = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/';
const CHAVE_HISTORICO = 'historicoPokemon';
const CHAVE_FAVORITOS = 'favoritosPokemon';

// Itens guardados: { nome, id }. Itens antigos (só o nome) são convertidos.
function lerLista(chave) {
    try {
        const salvo = JSON.parse(localStorage.getItem(chave));
        if (!Array.isArray(salvo)) return [];
        return salvo.map(item => typeof item === 'string' ? { nome: item, id: null } : item);
    } catch (e) {
        return [];
    }
}

function salvarLista(chave, lista) {
    try {
        localStorage.setItem(chave, JSON.stringify(lista));
    } catch (e) {}
}

// Miniatura clicável (sprite + nome) que leva à busca do Pokémon
function criarMini(pokemon) {
    const link = document.createElement('a');
    link.className = 'poke-mini';
    link.href = '/buscar?q=' + encodeURIComponent(pokemon.nome);

    if (pokemon.id) {
        const img = document.createElement('img');
        img.src = SPRITE_URL + pokemon.id + '.png';
        img.alt = pokemon.nome;
        img.loading = 'lazy';
        link.appendChild(img);

        const numero = document.createElement('span');
        numero.className = 'poke-mini-numero';
        numero.textContent = '#' + pokemon.id;
        link.appendChild(numero);
    } else {
        const bola = document.createElement('span');
        bola.className = 'pokebola-mini';
        bola.setAttribute('aria-hidden', 'true');
        link.appendChild(bola);
    }

    const nome = document.createElement('span');
    nome.textContent = pokemon.nome;
    link.appendChild(nome);

    return link;
}
