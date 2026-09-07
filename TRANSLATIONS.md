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
7. Add the disclaimer banner for the locale (see below) unless a fluent human has read the pages.
8. Pass both gates.

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

## The AI-translation disclaimer

Any locale whose text has **not** been read by a fluent human carries a banner saying so, in that language, on every page.

It is a per-language `banner` in `docs.json` — not something added to the pages, so it cannot drift out of sync and does not touch the 39 files:

```json
{
  "language": "zh-Hans",
  "banner": {
    "content": "本文档由 AI 翻译…[报告翻译问题](https://github.com/4casters-io/docs/issues/new?labels=translation&…)",
    "type": "warning",
    "dismissible": false
  },
  "tabs": [ … ]
}
```

`dismissible: false` on purpose: it is an accuracy disclaimer, not an announcement. A reader who dismissed it on page one would read the other 38 pages with no warning.

The banner says three things, and all three matter: the translation is machine-made, the English page is authoritative, and here is where to report a mistake. The report link is a **pre-filled GitHub issue** — labelled `translation`, titled with the locale, with a body template asking for the page URL, the wrong text, and a suggested fix. The audience is developers, so a GitHub issue is somewhere they already are, and the repo is public so anyone can file one.

**Remove a locale's banner when, and only when, a fluent human has read the pages.** That is the visible difference between a reviewed language and an unreviewed one.

Currently no banner: `en` (source), `es`, `it`.

### Text for each locale

Keep the three elements. Do not soften "the English version is authoritative" — that is the point of the sentence.

| Locale | Content (`%s` is the report URL) |
|---|---|
| `zh-Hans` | 本文档由 AI 翻译，仅为方便阅读而提供，可能存在错误。**以英文文档为准**——依赖本页内容前请对照英文核对。[报告翻译问题](%s) |
| `zh-Hant` | 本文件由 AI 翻譯，僅為方便閱讀而提供，可能存在錯誤。**以英文文件為準**——依賴本頁內容前請對照英文核對。[報告翻譯問題](%s) |
| `ru` | Эта документация переведена с помощью ИИ для удобства и может содержать ошибки. **Английская версия является официальной** — сверяйтесь с ней, прежде чем полагаться на эту страницу. [Сообщить об ошибке перевода](%s) |
| `fr` | Cette documentation est traduite par IA à titre de commodité et peut contenir des erreurs. **La version anglaise fait foi** — vérifiez-la avant de vous fier à cette page. [Signaler une erreur de traduction](%s) |
| `pt-BR` | Esta documentação foi traduzida por IA por conveniência e pode conter erros. **A versão em inglês é a oficial** — consulte-a antes de confiar nesta página. [Relatar um erro de tradução](%s) |
| `pt` | Esta documentação foi traduzida por IA por conveniência e pode conter erros. **A versão inglesa é a oficial** — consulte-a antes de confiar nesta página. [Comunicar um erro de tradução](%s) |
| `nl` | Deze documentatie is door AI vertaald voor het gemak en kan fouten bevatten. **De Engelse versie is leidend** — controleer die voordat u op deze pagina vertrouwt. [Een vertaalfout melden](%s) |

Banner content supports basic MDX — links, bold, italic. Custom components are not supported.

## When English changes

The translations are now stale, and nothing tells you which ones. Diff the English page against the commit the translation was made from, and re-translate the changed sections.

If a code sample changed, the translation is **broken**, not just stale — rule 2 means the fence content must match, and Gate 1 will fail until it does.

## Glossary

Shared with the frontend (PRO-275) so the app and the docs never render the same term two different ways. Changing a term means changing this table **and every occurrence in the pages, in the same commit**.

### All languages

`WebSocket` and `REST` stay untranslated everywhere. `maker`, `taker`, `heartbeat` and `token` stay untranslated in **Spanish**. Chinese renders heartbeat as `心跳` and token as `令牌`. For maker/taker, the **fee** usage keeps the English loanword (`taker 手续费`, as on Binance/OKX Chinese UIs) — that part is settled idiom. The **party** usage is genuinely mixed in the pages today: 「作为 taker」 in English on `place-order` and `user-feed`, `吃单方` on three market/user pages. One decision for the Chinese reviewer, applied tree-wide in one commit.

`moneyline`, `spread`, `total` stay in English, with a short gloss in the target language on first use per page.

### Spanish (`es`)

**A native Spanish speaker (David) has made an editing pass over these pages; a full Gate 2 read is still owed.** They are the closest thing to reviewed in the repo and are not to be edited from this table. This table is *derived from them* — it records what the translation already says, so the frontend can match it. If a term here disagrees with `es/pages/`, the pages are right and this table is wrong.

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
| liability | exposición |
| risk (the stake side of a bet) | riesgo |
| american odds | cuotas americanas |
| game | evento |
| league | liga |
| user feed / price feed | feed de usuario / feed de precios |
| in-play | en vivo |

`matched` and `unmatched` as **API field names** stay in English everywhere — they are keys in the payload (rule 2). The Spanish words above are for the concept in prose.

**Numbers are `en-US` format in every language — PM decision (2026-09-01), docs and app alike.** `3,000` stays `3,000` and `1%` stays `1%` in Spanish prose; do not localize separators. The Spanish tree was normalized (it had `3.000` on two pages, `1,000` on two others, and `1 %` throughout two). Rationale: one number format everywhere ahead of locale-separator bugs — `parseFloat("1.234,56")` reads as 1.234.

**Two drift items for the Spanish reviewer:** *exchange* is kept in English on most pages but rendered `intercambio` in 5 — pick one (recommend keeping `exchange`); and one raw English "liability" survives in `websocket/place-order`'s error section where the pages otherwise use `exposición`.

`exposición` and `riesgo` are **not interchangeable**: `exposición` renders *liability* (worst-case exposure across a game), `riesgo` renders *risk* (the stake side of a bet, the `risk`/`bet` field). The frontend must keep them apart the same way.

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

**The zh `注单` (graded wager) / `投注` (bet) distinction is intentional** — it mirrors the API's wager/bet split. Keep it.

**Unsettled — one decision per row, applied tree-wide in one commit, for the Chinese reviewer** (counts are files):

| Concept | Variants in the pages today |
|---|---|
| matched / fill | 成交 26 · 撮合 14 · 匹配 6 |
| maker | English 5 · 挂单方 1 · 做市商 1 · 对手方 2 |
| moneyline | `moneyline` · 单胜盘 · 胜负盘 · 独赢 (and 三项盘 / 三项胜平负 for 1x2) |
| liability | 负债 2 · 责任 1 |

The taker fee-vs-act split above is idiomatic and stays; the *maker* row is genuine drift — three renderings plus English.

**Unsettled: "cancel an order."** The current pages use `取消` (the ordinary word for cancel). `撤单` is the exchange term — what Chinese brokerages use for pulling a resting order — and is more domain-idiomatic. Needs a Chinese speaker to decide, then applied everywhere in one commit, in the docs and the frontend together.

### Traditional Chinese (`zh-Hant`)

Not translated by hand. Generated from `zh-Hans/` by:

```bash
python scripts/gen-zh-hant.py
```

The script runs OpenCC `s2twp` (Taiwan profile) over prose only — code fences and inline code are stashed and restored so rule 2 holds — then applies the Taiwan terms `s2twp` gets wrong:

| `s2twp` gives | Taiwan uses | |
|---|---|---|
| 實時 | 即時 | real-time |
| 賬戶 / 賬號 / 賬單 | 帳戶 / 帳號 / 帳單 | account |
| 登錄 / 注銷 | 登入 / 登出 | log in / out |
| 響應 (響應頭/體) | 回應 (回應標頭/主體) | response |
| 請求頭 / 請求體 | 請求標頭 / 請求主體 | request header/body |
| 返回 | 回傳 | returns (a value) |
| 撥用 / 調用 | 呼叫 | call — `s2twp` mangles 调用 into 撥用, "appropriate funds" |
| 標識(符) | 識別碼 | identifier |
| 載荷 | 酬載 | payload |

The full list is `POST` in `scripts/gen-zh-hant.py`. The script converts fence *labels* and prose but never fence *bodies* or inline code — and it is line-based, so CRLF files are handled.

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
