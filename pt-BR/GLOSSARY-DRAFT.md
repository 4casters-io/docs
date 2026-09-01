# Glossário pt-BR — RASCUNHO (aguardando revisor nativo)

Rascunho de terminologia para a árvore `pt-BR/`. Uma tradução por conceito, aplicada em toda a árvore. Preferência pelo uso consolidado da Betfair Brasil e do mercado financeiro brasileiro (B3). **Este arquivo é um rascunho: o revisor nativo (Gate 2) deve validar cada linha antes de o idioma ser publicado sem banner.**

Convenções gerais desta árvore:

- Tratamento: **você** (nunca tu/usted). Gerúndio brasileiro (*estamos processando*).
- Vocabulário brasileiro: usuário, time, tela, cadastro, celular.
- **Números permanecem em formato en-US** (`3,000`, `1.5`, `1%`) — decisão do PM (2026-09-01).
- Ficam em inglês (sem tradução): `maker`, `taker`, `heartbeat`, `token`, `WebSocket`, `REST`, `moneyline`, `spread`, `total`, **odds** (uso consolidado no mercado brasileiro de apostas; tratado como substantivo feminino plural: *as odds*), **exchange**.
- `moneyline` / `spread` / `total` recebem uma glosa em português na primeira ocorrência de cada página: *moneyline (vencedor do jogo)*, *spread (handicap de pontos)*, *total (soma de pontos, over/under)*.
- `matched` / `unmatched` / `graded` etc. como **nomes de campo da API** ficam sempre em inglês (são chaves do payload). As traduções abaixo valem para o conceito em prosa.

| Inglês | pt-BR | Observações |
|---|---|---|
| matched (adj.) / matched bet | correspondida / aposta correspondida | Uso Betfair Brasil |
| unmatched | não correspondida | |
| match (verbo) | corresponder | "would match" = "corresponderia" |
| fill (substantivo) / partial fill | correspondência / correspondência parcial | Um evento de casamento de ordens |
| orderbook | livro de ofertas | Escolha única para a árvore (uso B3); não usar "livro de ordens" |
| order | ordem | |
| place an order | enviar uma ordem | Para apostas: "fazer uma aposta" |
| cancel an order | cancelar uma ordem | |
| resting order | ordem em espera (no livro) | |
| open order | ordem em aberto | |
| offer / resting offer | oferta / oferta em espera | |
| stake | valor apostado | |
| risk (lado do risco da aposta, campo `risk`) | risco | Distinto de liability |
| win (ganho potencial, campo `win`) | ganho | |
| settle / settled | liquidar / liquidada | |
| graded (settled) wager | aposta liquidada | O par graded/settled do inglês colapsa em "liquidada"; campo `graded` fica em inglês |
| liability | responsabilidade | Uso Betfair Brasil; perda máxima (pior cenário) |
| worst-case loss | perda no pior cenário | |
| american odds | odds americanas | |
| game | jogo | |
| league | liga | |
| user feed / price feed | feed do usuário / feed de preços | "feed" fica em inglês |
| in-play / live | ao vivo | |
| liquidity | liquidez | |
| commission | comissão | |
| taker fee | taxa de taker | |
| back (a participant) | apostar em / a favor de | |
| home / away | da casa / visitante | time da casa, time visitante |
| draw | empate | |
| futures / specials | futuros / especiais | mercados de futuros e especiais |
| replay (feed) | reprodução / reproduzir | Recuperação de mensagens perdidas |
| broadcast-all mode | modo de difusão total | |
| kill switch | botão de emergência | |
| rolling window | janela móvel | |
