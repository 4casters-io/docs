# Glossário — Português Europeu (`pt`) — RASCUNHO

**Estado: rascunho para o revisor nativo (Gate 2).** Uma escolha por conceito, aplicada em toda a árvore `pt/`. Se o revisor alterar um termo, alterar esta tabela **e todas as ocorrências nas páginas, no mesmo commit** (ver `TRANSLATIONS.md`).

Convenções gerais desta árvore:

- Português **europeu**: `utilizador`, `equipa`, `ecrã`, `registo`, `telemóvel`, e a construção `estar a + infinitivo` («estamos a processar»). Tratamento formal, estilo técnico de PT-PT («o utilizador», «você» implícito).
- **Números em formato `en-US` em todas as línguas — decisão do PM (2026-09-01).** `3,000` fica `3,000`; `1.5` fica `1.5`; `1%` fica `1%`. Não localizar separadores.
- `WebSocket`, `REST`, `maker`, `taker`, `heartbeat`, `token` ficam em inglês.
- `moneyline`, `spread`, `total` ficam em inglês, com uma glosa curta em português na primeira utilização de cada página.
- `matched` e `unmatched` como **nomes de campos da API** ficam em inglês (regra 2 — são chaves do payload). Os termos portugueses abaixo são para o conceito em prosa.

| English | Português europeu | Nota |
|---|---|---|
| matched (verb / adj.) | corresponder / correspondida | Idioma Betfair.pt; «uma correspondência» para o substantivo |
| matched bets | apostas correspondidas | |
| unmatched | não correspondida | = em espera no livro |
| fill (a fill / to fill) | execução / executar | Quando o texto inglês distingue *fill* de *match* |
| orderbook | livro de ordens | Termo CMVM; não «livro de ofertas» |
| order | ordem | Feminino: «a ordem» |
| resting order | ordem em espera | Alternativa para o revisor: «ordem pendente» |
| place an order | colocar uma ordem | |
| cancel an order | cancelar uma ordem | |
| edit an order | editar uma ordem | |
| stake | montante | O lado arriscado da aposta em prosa genérica |
| risk (the `risk`/`bet` field side) | risco | **Não** confundir com *liability* |
| liability | responsabilidade | Idioma Betfair.pt: perda máxima possível num jogo |
| settle / settlement | liquidar / liquidação | |
| graded wager | aposta avaliada | «Avaliar» = atribuir resultado (won/lost/push) |
| american odds | odds americanas | Em Portugal «odds» é o empréstimo corrente; feminino («as odds») |
| game | jogo | |
| league | liga | |
| participant | participante | |
| market | mercado | |
| user feed / price feed | feed de utilizador / feed de preços | «feed» fica em inglês |
| in-play | ao vivo | «jogo ao vivo / em direto» |
| exchange | exchange | Empréstimo, com glosa «bolsa de apostas peer-to-peer» na primeira utilização |
| maker / taker | maker / taker | Ficam em inglês (partes e comissões) |
| moneyline | moneyline | Glosa: «aposta no vencedor do jogo» |
| spread | spread | Glosa: «handicap de pontos» |
| total | total | Glosa: «mais/menos pontos totais» |
| favorite / underdog | favorito / não favorito | |
| payout | pagamento | |
| odds tick | tick de odds | |
| push (result) | push | Fica em inglês — é um valor da API; glosa «reembolso» em prosa |
| heartbeat | heartbeat | Fica em inglês |
| token | token | Fica em inglês; masculino («o token») |
| login / log in | iniciar sessão | PT-PT; não «logar» |
| endpoint | endpoint | Empréstimo corrente |
| request / response | pedido / resposta | PT-PT: «pedido», não «solicitação» |
| header / body (HTTP) | cabeçalho / corpo | |
| payload | payload | Empréstimo corrente em documentação técnica |
| polling | polling | Empréstimo; «sem polling» |
| rate limit | limite de taxa | |
| batch (place/cancel) | em lote | |
