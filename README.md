# MD-Machine

Projeto **Knowledge Engine** da disciplina de Lógica e Matemática Discreta.

## Ideia central

Montar uma base de conhecimento em Prolog (lógica de primeira ordem) a partir do **ranking mundial de jogadores de xadrez da FIDE** e responder perguntas sobre ela usando fatos, regras e consultas. (A Base utilizada é de Novembro de 2026)

## Base de dados

- **Fonte:** lista de ratings da FIDE, https://ratings.fide.com/download_lists.phtml (arquivo `players_list_xml`, versão com ratings clássico, rápido e blitz).
- **Recorte:** os **500 jogadores com maior rating clássico** que possuem todos os campos preenchidos (nome, federação, sexo, ano de nascimento, título e os três ratings).
- **Campos utilizados (8):**

| Campo | Exemplo |
|---|---|---|
| Nome  | `magnus_carlsen` |
| Federacao  | `nor` |
| Sexo  | `m` |
| AnoNascimento | `1990` |
| Titulo | `gm` |
| RatingClassico | `2830` |
| RatingRapido | `2820` |
| RatingBlitz | `2880` |

## Conversão dos dados

O script `gerar_base.py` lê o XML da FIDE e gera o arquivo `base.pl`:

Lê o XML da FIDE, retira jogadores com algum camp vazio, normaliza os textos para PROLOG, padroniza nomes para nome_sobrenome e ordena por rating clássico, obtendo os 500 melhores.

## Base de conhecimento

```prolog
jogador(Nome, Federacao, Sexo, AnoNascimento, Titulo, RatingClassico, RatingRapido, RatingBlitz).
```

Exemplo:

```prolog
jogador(pentala_harikrishna, ind, m, 1986, gm, 2659, 2595, 2620).
```
## Regras

### Quantos jogadores tem uma federação?
```prolog
total_jogadores(F, Total) :-
    findall(1, jogador(_, F, _, _, _, _, _, _), L),
    sum_list(L, Total).
```
Query: `total_jogadores(ind, Q).`

### Qual a soma dos ratings clássicos de uma federação?
```prolog
total_rating(F, Total) :-
    findall(C, jogador(_, F, _, _, _, C, _, _), L),
    sum_list(L, Total).
```
Query: `total_rating(ind, S).`

### Qual a média de rating clássico de uma federação?
```prolog
media_rating(F, M) :-
    findall(C, jogador(_, F, _, _, _, C, _, _), L1),
    sum_list(L1, S),
    findall(1, jogador(_, F, _, _, _, _, _, _), L2),
    sum_list(L2, Q),
    Q > 0,
    M is S / Q.
```
Query: `media_rating(ind, M).`

### Quais jogadores rendem mais de 50 pontos a mais no blitz do que no clássico (são melhores em Blitz)?
```prolog
especialista_blitz(N, D) :-
    jogador(N, _, _, _, _, C, _, B),
    D is B - C,
    D > 50.
```
Query: `especialista_blitz(N, D).`

### Quais jogadores rendem mais de 50 pontos a mais no rápido do que no clássico (São melhores no rápido)?
```prolog
especialista_rapido(N, D) :-
    jogador(N, _, _, _, _, C, R, _),
    D is R - C,
    D > 50.
```
Query: `especialista_rapido(N, D).`

### Quantos jovens possuem pontuações altas (nascidos depois de 2000 e rating clássico acima de 2600) tem uma federação?
```prolog
total_jovens_fortes(F, Total) :-
    findall(1, (jogador(_, F, _, A, _, C, _, _), A > 2000, C > 2600), L),
    sum_list(L, Total).
```
Query: `total_jovens_fortes(ind, Q).`

### Quantos grandes mestres tem uma federação?
```prolog
total_gm(F, Total) :-
    findall(1, jogador(_, F, _, _, gm, _, _, _), L),
    sum_list(L, Total).
```
Query: `total_gm(ind, Q).`

## Como rodar

### 1. Gerar a base
1. Baixe a lista da FIDE e extraia o XML.
2. Ajuste o caminho `ARQ_XML` no início de `gerar_base.py`.
3. Execute:
```bash
python gerar_base.py
```
Isso cria o `base.pl`.

### 2. Consultar no SWISH (https://swish.swi-prolog.org/)
1. Crie um notebook
2. Crie uma célula **Program** e cole nela o conteúdo de `perguntas.pl` e de `base.pl`. (na mesma célula)
3. **Clique dentro da célula Program** antes de rodar cada query. O SWISH roda a query só na célula selecionada.
4. Digite as queries na área **Query**.

## Observações

- Nas queries, a federação é passada como constante (`ind`, `usa`, `nor`...).
- O código da federação segue o padrão FIDE em minúsculas (`bra`, `ind`, `usa`...). Conforme a  `base.pl`.

## Funcionamento Lógico
Transforma cada linha da base em uma proposição verdadeira.
E as regras permitem filtrar ou selecionar informações a partir dos dados.


