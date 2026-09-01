# Glossaire français — BROUILLON (en attente de relecture par un locuteur natif)

> **Statut : brouillon.** Cette table a été établie *avant* la traduction (voir TRANSLATIONS.md, « New languages ») et appliquée uniformément dans `fr/pages/` et `snippets/fr/types/`. Un relecteur natif doit la valider (Gate 2) avant toute mise en production ; tout changement de terme se fait dans cette table **et** dans toutes les pages, dans le même commit.

## Décisions générales

- **Registre : `vous`**, jamais `tu` — usage standard de la documentation technique française.
- **Chiffres, montants, cotes, pourcentages : format `en-US` partout** (décision PM 2026-09-01) — `3,000` reste `3,000`, `1%` reste `1%` (pas d'espace avant `%`), `1.5` garde le point décimal. Ne pas franciser les séparateurs.
- Guillemets : guillemets droits comme en anglais, pas de « » imposés.
- **Restent en anglais partout** : `WebSocket`, `REST`, `maker`, `taker`, `heartbeat`, `token`, `moneyline`, `spread`, `total` — les trois derniers avec une courte glose française à la première occurrence de chaque page (moneyline = vainqueur du match, spread = handicap de points, total = plus/moins de points).
- **`exchange`** reste en anglais (comme en espagnol) : « l'exchange », « exchange de paris peer-to-peer ».
- Les noms de champs, valeurs d'enum, endpoints et tout code inline restent **byte-identiques** à l'anglais (règle 2) — `matched`, `unmatched`, `liability`, `risk` en backticks sont des clés de payload, pas de la prose.

## Termes de l'exchange

| Anglais | Français retenu | Notes |
|---|---|---|
| matched (adj. / verbe) | matché(e) / matcher | Usage Betfair France (« paris matchés »). Écarté : « apparié ». |
| matched bets | paris matchés | |
| unmatched | non matché(e) | « ordres non matchés » = ordres encore au carnet |
| match / fill (nom, l'événement) | un matching / une exécution | « matching » pour l'événement de mise en correspondance |
| orderbook | carnet d'ordres | |
| order | ordre | masculin ; jamais « commande » |
| resting order | ordre en attente | ordre posté au carnet, pas encore matché |
| place an order | placer un ordre | |
| cancel an order | annuler un ordre | |
| edit an order | modifier un ordre | |
| stake | mise | |
| risk (côté mise d'un pari, champ `risk`) | risque | **Distinct de liability** — voir ci-dessous |
| liability | responsabilité | Terme Betfair FR. Perte maximale (pire cas) sur un match. **Ne pas confondre avec « risque »** : `risk` = la mise d'un pari, `liability` = l'exposition pire-cas agrégée. |
| settle / settlement / settled | régler / règlement / réglé(e) | |
| graded wager | wager réglé | `wager` (objet API distinct de *bet*) reste en anglais pour préserver la distinction wager/bet de l'API ; glosé « pari enregistré » à la première occurrence. À valider par le relecteur. |
| bet | pari | |
| wager (objet API) | wager | voir ci-dessus |
| odds / american odds | cotes / cotes américaines | |
| favorite / underdog | favori / outsider | |
| game | match | pluriel « matchs » ; « game » = rencontre sportive dans cette API |
| league | ligue | |
| participant | participant | |
| market | marché | |
| user feed / price feed | flux utilisateur / flux des prix | |
| in-play | en direct | glosé « (in-play) » si utile |
| pre-game | avant match | |
| maker / taker | maker / taker | anglais conservé (partie **et** frais) : « frais taker », « en tant que maker » |
| fee | frais | |
| payout | gain | le champ `payout` reste en code |
| balance | solde | |
| account | compte | |
| endpoint | endpoint | usage courant des docs dev françaises |
| payload | payload | idem |
| request / response | requête / réponse | |
| header / body | en-tête / corps | |
| push (résultat de pari) | push | glosé « remboursé » à la première occurrence |
| tick | tick | |
| stream / streaming | flux / streaming | « WebSocket de streaming » |
| grade (verbe, noter un pari) | régler | même famille que settle — l'API ne distingue pas les deux en prose |

## Points à trancher par le relecteur natif

1. **« matché »** (Betfair FR, anglicisme assumé) vs « apparié » — « matché » retenu partout ; confirmer.
2. **« responsabilité »** pour *liability* (terme Betfair FR) vs « exposition » (choix de l'espagnol) — « responsabilité » retenu ; confirmer.
3. **« wager réglé »** pour *graded wager* — confirmer que garder `wager` en anglais est acceptable, ou proposer un doublet français qui préserve la distinction wager/bet.
4. **« flux des prix »** vs « flux de prix » — « flux des prix » retenu.
5. « match » (game) vs « matché » (matched) — proximité assumée ; signaler toute phrase ambiguë.
