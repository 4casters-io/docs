# Woordenlijst Nederlands (`nl`) — CONCEPT

**Status: concept, nog niet door een moedertaalspreker beoordeeld (Gate 2 open).**
Eén term per concept, in de hele boom consequent toegepast. API-veldnamen (`matched`,
`unmatched`, `bet`, `risk`, `win`, …) blijven altijd Engels — dat zijn keys in de payload
(regel 2). De Nederlandse termen hieronder gelden voor het concept in lopende tekst.

De lezer wordt aangesproken met **je**, nooit *u* (conventie voor Nederlandse developerdocs).

Nederlandse wed- en tradingtaal leent zwaar uit het Engels; waar een Nederlandse
munting gekunsteld zou zijn, is de Engelse term bewust aangehouden. Die keuzes staan
expliciet in de tabel en zijn punten voor de reviewer.

| Engels | Nederlands | Toelichting / beslissing |
|---|---|---|
| matched (verb/adj.) | gematcht / matchen | "gematcht" (niet "gekoppeld" of "gecrost"); werkwoord "matchen" |
| matched bets | gematchte weddenschappen | |
| unmatched | niet-gematcht | als concept; het veld `unmatched` blijft Engels |
| fill (noun) | fill | Engels gehouden; "een gedeeltelijke fill". "uitvoering" zou kunnen maar botst met order-flow-jargon |
| orderbook | orderboek | |
| order | order (de) | |
| resting order | openstaande order | niet "rustende order" |
| place an order | een order plaatsen | |
| cancel an order | een order annuleren | niet "intrekken" |
| edit an order | een order bewerken | |
| stake | inzet | |
| settle / settlement | afwikkelen / afwikkeling | niet "verrekenen" |
| graded (wager) | afgewikkeld | `wager` als API-object blijft Engels: "afgewikkelde wagers" |
| liability | liability (Engels) | **Beslissing:** Engels gehouden. "Aansprakelijkheid" is juridisch register, "risico" botst met *risk* (het `risk`-veld). Bij eerste gebruik per pagina geglost als "je maximale verlies". Reviewer: akkoord? |
| risk (inzetkant van een weddenschap) | risico | het `risk`-veld zelf blijft Engels |
| win (winstkant) | winst / winbedrag | |
| american odds | Amerikaanse odds | "odds" is gangbaar Nederlands wedjargon; nooit "noteringen" |
| game | wedstrijd | niet "spel"; het veld `gameID` blijft Engels |
| league | competitie | |
| participant | deelnemer | |
| user feed / price feed | user feed / price feed | Engels gehouden (eigennamen van de feeds) |
| in-play | live (in-play) | "live" in lopende tekst; "in-play" bij eerste gebruik ernaast |
| exchange | exchange | Engels gehouden, net als in het Spaans aanbevolen; "(wed)beurs" alleen als gloss |
| betting exchange | betting exchange | gloss bij eerste gebruik: "peer-to-peer wedbeurs" |
| maker / taker | maker / taker | verplicht Engels (regel) |
| heartbeat, token, WebSocket, REST | onvertaald | verplicht Engels (regel) |
| moneyline | moneyline | verplicht Engels; gloss eerste gebruik per pagina: "(inzet op de winnaar)" |
| spread | spread | verplicht Engels; gloss: "(handicap)" |
| total | total | verplicht Engels; gloss: "(over/onder het totaal aantal punten)" |
| draw | gelijkspel | |
| favorite / underdog | favoriet / underdog | |
| payout | uitbetaling | |
| commission | commissie | |
| taker fee | taker-fee | |
| endpoint | endpoint | |
| request / response | verzoek / antwoord | koppen "Request"/"Response" → "Verzoek {#request}" / "Antwoord {#response}" |
| replay(ing missed messages) | opnieuw afspelen / replay | zelfstandig naamwoord "replay" blijft Engels |
| subscribe / subscription | abonneren / abonnement | de commando's `subscribe` enz. blijven Engels (code) |
| changelog-koppen | Toegevoegd / Gewijzigd / Opgelost / Verouderd / Verwijderd | Added / Changed / Fixed / Deprecated / Removed |

## Getallen

**en-US-formaat in elke taal — PM-beslissing (2026-09-01).** `3,000` blijft `3,000`,
`1.5` blijft `1.5`, `1%` blijft `1%`. Nooit `1.234,56`.

## Open punten voor de reviewer

1. `liability` Engels houden vs. toch een Nederlandse term — zie tabelrij.
2. "gematcht" vs. "gematched" spelling — hier consequent *gematcht* (vernederlandste
   werkwoordspelling: matchen → gematcht).
3. "orderboek" vs. Engels "orderbook" — hier vertaald, omdat "orderboek" gevestigd
   beursjargon is (AEX/brokers).
4. Changelog-kop "Opgelost" vs. "Gecorrigeerd" voor *Fixed*.
