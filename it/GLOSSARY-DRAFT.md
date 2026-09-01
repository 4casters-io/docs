# Glossario italiano — BOZZA

**Stato: bozza per il revisore madrelingua.** Questi termini sono stati scelti seguendo, dove possibile, l'uso di Betfair Italia (il vocabolario di exchange betting più consolidato in italiano). Un termine per concetto, applicato in modo uniforme a tutto l'albero `it/`. Se il revisore cambia un termine qui, va cambiato in ogni pagina nello stesso commit (vedi `TRANSLATIONS.md`).

Il lettore è sempre il **tu** (seconda persona singolare), come da convenzione della documentazione per sviluppatori in italiano.

| English | Italiano | Note |
|---|---|---|
| exchange | exchange | Invariato (uso Betfair Italia: "Betfair Exchange"). |
| matched (verb / noun) | abbinare / abbinamento | Uso Betfair Italia. |
| matched bets | scommesse abbinate | |
| unmatched | non abbinato / -a | "ordini non abbinati". Come nome di campo API (`matched`, `unmatched`) resta in inglese (regola 2). |
| fill (a fill / to fill) | abbinamento / abbinare | Stesso concetto di *matched*: un termine per concetto. "Partial fill" = "abbinamento parziale". |
| orderbook | libro degli ordini | |
| order | ordine | |
| resting order | ordine in attesa | Ordine non abbinato che resta nel libro. |
| place an order | piazzare un ordine | Uso Betfair Italia ("piazza scommessa"). |
| cancel an order | annullare un ordine | Uso Betfair Italia ("annulla" per le scommesse non abbinate). |
| edit an order | modificare un ordine | |
| stake | puntata | |
| risk (the stake side, the `risk`/`bet` field) | rischio | Distinto da *liability*: `rischio` è l'importo puntato su una singola scommessa. |
| liability | responsabilità | Uso Betfair Italia. Perdita massima possibile; **non** intercambiabile con `rischio`. |
| settle / settlement | liquidare / liquidazione | |
| graded wager | giocata refertata | "Referto" è il termine italiano per l'esito ufficiale. **Da confermare col revisore.** |
| wager (vs bet) | giocata | La distinzione giocata/scommessa rispecchia la coppia wager/bet dell'API. **Da confermare col revisore.** |
| bet | scommessa | |
| american odds | quote americane | |
| odds | quote (sing. quota) | |
| game | evento | Copre anche i mercati futures, dove "partita" non funzionerebbe. |
| league | lega | Codici lega (`NBA`, ecc.). |
| participant | partecipante | |
| user feed / price feed | feed utente / feed prezzi | |
| in-play | live | Uso Betfair Italia. |
| maker / taker | maker / taker | Invariati (decisione tree-wide). |
| heartbeat | heartbeat | Invariato. |
| token | token | Invariato. |
| WebSocket / REST | WebSocket / REST | Invariati ovunque. |
| moneyline | moneyline | Invariato, con glossa alla prima occorrenza per pagina: *quota sul vincente* ("testa a testa"). |
| spread | spread | Invariato, con glossa alla prima occorrenza per pagina: *handicap di punti*. |
| total | total | Invariato, con glossa alla prima occorrenza per pagina: *totale punti, over/under*. |
| payout | vincita | L'importo vinto (win amount). |
| favorite / underdog | favorito / sfavorito | |
| draw | pareggio | Come valore API (`"draw"`) resta in inglese. |
| batch | batch | Invariato ("in batch", "un batch di ordini"). |
| endpoint | endpoint | Invariato. |
| feed | feed | Invariato. |
| stream | stream | Invariato. |
| polling | polling | Invariato. |
| snapshot | snapshot | Invariato. |
| tick | tick | Invariato. |
| handshake | handshake | Invariato. |
| payload | payload | Invariato. |
| header (HTTP) | header | Invariato ("l'header `Authorization`"). |

## Numeri

**I numeri restano in formato `en-US` in tutte le lingue — decisione PM (2026-09-01).** `3,000` resta `3,000`, `1.5` resta `1.5`, `1%` resta `1%`. Non localizzare mai i separatori (mai `1.234,56`).

## Punti aperti per il revisore

1. **giocata / scommessa** per wager / bet — regge la distinzione dell'API? In alternativa: "scommessa refertata" per *graded wager* e "scommessa" ovunque.
2. **evento** per *game* — alternativa: "partita" (ma non copre i futures).
3. **lega** per *league* — alternativa: "campionato".
4. **responsabilità** per *liability* — è il termine Betfair Italia; alternativa più finanziaria: "esposizione" (lo spagnolo usa `exposición`).
