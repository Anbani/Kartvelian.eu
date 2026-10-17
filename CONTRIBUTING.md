# Contributing

## Report

[Open an issue](../../issues/new/choose): **Correction**, **Native speaker note** or **Lesson idea**. Svan, Megrelian
and Laz input wanted most.

## Edit on GitHub

Pencil icon → change → *Propose changes*. A check runs on the PR; its log names the line to fix.

## Work locally

```bash
git clone https://github.com/<you>/Kartvelian.eu && cd Kartvelian.eu
python3 -m pip install -r scripts/requirements.txt
python3 scripts/check.py      # same check as CI
```

### Lessons

1. Module in `curricula/<language>.yaml` (add it if new; `num` runs across the whole curriculum).
2. File `lessons/<language>/level-<n>-<num>-<slug>.md`; intro level: `level-intro-<num>-<slug>.md`.
3. Frontmatter, all required except `updatedAt`:

```yaml
---
language: "svan"            # georgian | svan | megrelian | laz; matches the folder
level: "intro"              # level id in curricula/<language>.yaml
levelTitle: "Introduction to Svan"
cefr: "–"                   # A1.1 … B1, or –
module: 3                   # module num
pageSlug: "numbers"         # module slug
title: "Numbers in Svan"
description: "One or two sentences for search and link previews."
publishedAt: 2026-11-01
updatedAt: 2026-11-15
---
```

4. Plain Markdown. No imports. HTML only `<mark>` (letter in a word: **ჩა<mark>ჲ</mark>**) and `<figure>`.

### Flashcards

`decks/<language>/<deck>.toon`: one `term|meaning` row per card; update the header count. Format:
[docs/toon.md](docs/toon.md). Georgian: no transliteration or IPA columns (generated).

### Alphabets

`alphabets/<language>.json`, one entry per letter: `letter`, `name`, `word`, `meaning`; Svan, Megrelian, Laz also
`letterIpa`, `wordIpa` in slashes (`/ɑ/`). Georgian IPA is generated.

### Dictionary

`dictionary/<language>.json`: tier B (Wiktionary) is regenerated, fix it upstream; tier A (verified) needs a source.
[docs/dictionary.md](docs/dictionary.md).

### Verbs

`verbs/georgian.json`: one entry per verb, tenses → person forms. [docs/verbs.md](docs/verbs.md).

## Style

[docs/style.md](docs/style.md). In short:

- Readers: non-native learners; text in English.
- Transliteration beside every new Mkhedruli word; one scheme per page.
- Four languages, equal standing.
- Source any form a reader can't check.

## Review

Maintainers review every PR. Svan, Megrelian, Laz forms may need a second speaker or a published source; a source
request is not a rejection.

## License

Contributions: [CC BY-SA 4.0](LICENSE). Conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
