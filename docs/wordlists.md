# Georgian word list (`wordlists/georgian.toon`)

677 headwords. Feeds vocabulary cards, Wordle, Waffle, Crossword: one bad gloss shows in four places.
`freq`, `level`: `null` when unknown.

## Schema
`{word|meaning_en|pos|category|difficulty|freq|level|example.ka|example.en}`

## Fields

| Field | Description |
|---|---|
| `word` | Georgian headword (Mkhedruli) |
| `meaning_en` | English gloss; may include `(name)`, `(coin)`, etc. |
| `pos` | Part of speech (noun, verb, adjective, ...) |
| `category` | Wordle-relevance tag (see allowed values below) |
| `difficulty` | Engine-internal bucket (1..5). Drives the slot picker in `the site's Wordle engine`; not surfaced in the UI. |
| `freq` | `log10(1 + paradigm_count)`, 4dp. Compresses Zipfian counts to ~0–6. Cheat: `0`=unattested, `1`=rare, `3`=moderate, `5+`=very common. |
| `level` | CEFR-style level (A1–C2) |
| `example.ka` | Example sentence in Georgian |
| `example.en` | English translation of example |

## Allowed `category` values

| Value | Meaning |
|---|---|
| `common` | Standard noun/verb/adjective (ideal Wordle answer) |
| `anthroponym` | Personal name or surname |
| `toponym` | Place name |
| `ethnonym` | Name of a people/ethnicity |
| `chrematonym` | Brand, company, or institution |
| `eponym` | Common word derived from a proper name |
| `theonym` | Name of a deity |
| `historical` | Obsolete referent (old coins, defunct titles) |
| `archaism` | Outdated form, still legitimate |
| `dialectal` | Regional Georgian (Mingrelian, Svan, Imeretian, ...) |
| `loanword` | Unassimilated foreign borrowing |
| `jargon` | Specialized/technical |
| `colloquial` | Informal/slang |
| `acronym` | Acronym or initialism |

## Precedence

When multiple categories apply: **`anthroponym` > `historical` > `common`**

## TOON Format

This word list is stored as a TOON (Token-Oriented Object Notation) tabular array. Only the subset relevant to `wordlists/georgian.toon` is described below.

### Root header

```
[677|]{word|meaning_en|pos|category|difficulty|freq|level|example.ka|example.en}:
```

- `[677|]` — root array header. `677` is the row count `N`; the trailing `|` declares **pipe** as the active delimiter for this scope.
- `{word|meaning_en|...|example.en}` — field list, pipe-separated, in fixed column order. Field names use the same delimiter declared in the bracket. Dotted keys (`example.ka`, `example.en`) round-trip through the codegen into the nested `example: { ka, en }` shape the runtime expects.
- The header line ends with `:`. Rows follow at depth +1 (2 spaces).

### Rows

Each row is one line at depth +1: nine pipe-separated values in the order declared by the field list. Empty strings round-trip as empty tokens between two pipes.

### Quoting rules in this scope

A value MUST be quoted (`"..."`) only if it contains the active delimiter `|`, a colon `:`, a double quote, a backslash, brackets/braces, leading/trailing whitespace, or control characters, or if it equals `true` / `false` / `null` or looks numeric. Georgian text, internal spaces, punctuation like `.` `?` `!` `/` `(` `)` — all safe unquoted.

Note: `meaning_en` values like `abazi (coin) / Abkhazian` contain `/` and parentheses, which do **not** require quoting under the pipe delimiter.

### Escapes (inside quoted values only)

Only `\\`, `\"`, `\n`, `\r`, `\t` are valid. Any other escape is an error.

### Numbers

`freq` is emitted in canonical decimal form (no exponent, no trailing zeros beyond significant digits, no leading zeros). Decoders accept the printed form and round-trip to the same value.

### Strict-mode invariants

- Every row MUST have exactly **9** values (matching the 9 fields).
- The file MUST contain exactly **677** rows.
- Indentation MUST be a multiple of 2 spaces; tabs are forbidden in indentation.
- No blank lines between rows.

### Minimal example

```
[677|]{word|meaning_en|pos|category|difficulty|freq|level|example.ka|example.en}:
  აბაზი|abazi (coin) / Abkhazian|noun|historical|5|1.8808|C2|აბაზი ძველი ფული იყო.|Abazi was an old coin.
  აბაკი|abacus|noun|common|4|1.5315|C2|აბაკი ძველი დასაანგარიშებელი მოწყობილობაა.|An abacus is an old calculating device.
```