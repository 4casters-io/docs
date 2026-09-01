# Translating these docs

This site ships in several languages. English is the source; every other language is a mirror of it.

Mintlify renders the language switcher from two things: a folder per language, and a `navigation.languages` entry in `docs.json`. There is no i18n library and no build step.

```
pages/                    English — the only hand-edited source
es/pages/                 mirror of pages/
zh-Hans/pages/            mirror of pages/
zh-Hant/pages/            generated from zh-Hans/ by script
snippets/types/           English snippets
snippets/{locale}/types/  mirrored snippets
```

## Rules

These keep the site building and the code samples runnable. They are not style preferences.

1. **English under `pages/` is the only hand-edited source.** Translations regenerate from it. Never fix a typo in a translation and leave English wrong — fix English, then regenerate.

2. **Code fences and inline code stay byte-identical to English.** Code, JSON, field names, endpoint paths, enum values. A translated field name is a broken integration. This is the rule that matters most.

3. **`openapi:` frontmatter lines stay verbatim.** In frontmatter only `title:` and `description:` values translate.

4. **MDX tags and attributes are markup.** Translate text children and human-facing labels — `<Tab title="…">`, `<Accordion title="…">`, and the CodeGroup fence label (the text after the language in ```` ```json Request ````). Never translate a component name or a prop name.

5. **Internal links target the same-language page** when it exists, else the English path.

6. **Give translated headings an explicit anchor.** Mintlify derives anchors from heading text, so translating a heading silently breaks every deep link to it. Write `## Respuesta {#response}` using the English anchor.

7. **Never write under `sources/`.** It is snapshotted from the services by the docs reconciler and overwritten on every API change.

8. **Out of scope: the generated API Reference tab.** Its text comes from the OpenAPI document the reconciler snapshots; a bot overwrites it on every API change, so translating it would be undone.

### One exception to rule 2

Inline code that names a **translated heading on the same page**, rather than an API identifier.

`changelog.mdx` says "changes are grouped under `Added`, `Changed`, …" and those `### Added` headings are themselves translated. Leaving the inline code in English would point at headings that don't exist on the page.

The exception list is `INLINE_EXEMPT` in `scripts/check-structure.py`, keyed on the English source path. Adding to it needs the same justification: the backticked text names something on the page that is itself translated, and is not an API identifier.

## Adding a language

1. Draft `{locale}/pages/**.mdx` from `pages/**.mdx` under the rules above.
2. Mirror `snippets/{locale}/types/*.mdx` and repoint the refs to `<Snippet file="{locale}/types/…" />`.
3. Add explicit `{#anchor}` IDs to translated headings.
4. Add the `navigation.languages` block to `docs.json`.
5. Add the locale to `LOCALES` in **both** `scripts/check-structure.py` and `scripts/check-links.py` — they are separate lists.
6. Write the glossary section for the language, below, **before** drafting. Not after.
7. Pass both gates.

### Gate 1 — mechanical

```bash
python scripts/check-structure.py   # fences, MDX components, openapi:, inline code
python scripts/check-links.py       # internal links and heading anchors
mint dev                            # renders — the one check that isn't automated
```

Both exit non-zero on failure. Zero failures is the bar.

`check-structure.py` also reports **informational** findings for translated CodeGroup fence labels. Those are rule 4 being followed, not problems. Only the failure count matters.

### Gate 2 — a native speaker reads it

A fluent reader confirms the prose reads naturally and the glossary terms are right.

**Do not ship a language on Gate 1 alone.** These docs describe a money API where `matched`, `unmatched`, `liability`, `stake` and `settle` have exact meanings. A structurally perfect translation that uses the wrong word for "unmatched" produces a developer who builds the wrong thing.

## When English changes

The translations are now stale, and nothing tells you which ones. Diff the English page against the commit the translation was made from, and re-translate the changed sections.

If a code sample changed, the translation is **broken**, not just stale — rule 2 means the fence content must match, and Gate 1 will fail until it does.

## Glossary

Shared with the frontend (PRO-275) so the app and the docs never render the same term two different ways. Changing a term means changing this table **and every occurrence in the pages, in the same commit**.

### All languages

`maker`, `taker`, `heartbeat`, `token`, `WebSocket`, `REST` stay untranslated.

`moneyline`, `spread`, `total` stay in English, with a short gloss in the target language on first use per page.

### Spanish (`es`)

**The Spanish pages are native-speaker work and are not to be edited from this table.** This table is *derived from them* — it records what the translation already says, so the frontend can match it. If a term here disagrees with `es/pages/`, the pages are right and this table is wrong.

Address the user as `tú`, never `usted`. Neutral between Spain and Latin America.

| English | Spanish |
|---|---|
| matched (verb / noun) | cruzar / un cruce |
| matched bets | apuestas cruzadas |
| orderbook | libro de órdenes |
| order | orden |
| resting order | orden en espera |
| stake | importe |
| settle | liquidar |
| liability | riesgo |
| american odds | cuotas americanas |
| game | evento |
| league | liga |
| user feed / price feed | feed de usuario / feed de precios |
| in-play | en vivo |

`matched` and `unmatched` as **API field names** stay in English everywhere — they are keys in the payload (rule 2). The Spanish words above are for the concept in prose.

**One open question for the Spanish reviewer:** "liability" is rendered as `riesgo` in 16 places and `exposición` in 6. Both read fine; the frontend needs one of them so the app and the docs agree. Ask before changing anything — it may be a deliberate distinction.

### Simplified Chinese (`zh-Hans`)

| English | Simplified |
|---|---|
| orderbook | 订单簿 |
| order | 订单 |
| place an order | 下单 |
| cancel an order | *unsettled — see below* |
| matched / unmatched | 已成交 / 未成交 |
| in-play | 滚球 |
| account | 账户 |
| real-time | 实时 |

**Unsettled: "cancel an order."** The current pages use `取消` (the ordinary word for cancel). `撤单` is the exchange term — what Chinese brokerages use for pulling a resting order — and is more domain-idiomatic. Needs a Chinese speaker to decide, then applied everywhere in one commit, in the docs and the frontend together.

### Traditional Chinese (`zh-Hant`)

Not translated by hand. Generated from `zh-Hans/` by:

```bash
python scripts/gen-zh-hant.py
```

The script runs OpenCC `s2twp` (Taiwan profile) over prose only — code fences and inline code are stashed and restored so rule 2 holds — then applies the Taiwan terms `s2twp` gets wrong:

| `s2twp` gives | Taiwan uses |
|---|---|
| 實時 | 即時 |
| 賬戶 | 帳戶 |
| 賬號 | 帳號 |
| 登錄 | 登入 |
| 注銷 | 登出 |

Regenerate after every change to `zh-Hans/`, and re-check that list afterwards — it is easy to reintroduce.

`s2twp` applies Taiwan vocabulary. If Hong Kong and Singapore readers matter as much as Taiwan, switch to the plain `s2t` profile in `scripts/gen-zh-hant.py`.

### Portuguese — `pt` and `pt-BR`

Two separate translations, not a script conversion. There is no OpenCC for Portuguese.

`pt` is European Portuguese, `pt-BR` is Brazilian. Mintlify's schema has no `pt-PT`, which is why European Portuguese is plain `pt`.

They differ in vocabulary, and in a grammar pattern that shows up constantly in status text:

| English | `pt` (European) | `pt-BR` (Brazilian) |
|---|---|---|
| team | equipa | time |
| user | utilizador | usuário |
| screen | ecrã | tela |
| registration | registo | cadastro |
| mobile phone | telemóvel | celular |
| we are processing | estamos **a processar** | estamos **processando** |

Each needs its own reviewer. Neither is a derivation of the other.

### New languages

Write the table before drafting. Copy the English column from the Spanish table above — those are the terms that matter for this API — and fill in the target language with a native speaker, not after the fact.
