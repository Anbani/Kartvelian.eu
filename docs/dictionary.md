# Dictionary (`dictionary/<language>.json`)

One JSON array per language, sorted by headword. Feeds `/<language>/dictionary`, ⌘K search and the Svan, Megrelian, Laz word games.

| Tier | Key | Source | Licence |
|---|---|---|---|
| A, verified | `v` | forms the site teaches, each checked in a printed dictionary | CC BY-SA 4.0 (ours) |
| B, Wiktionary | `s` | English Wiktionary via [kaikki.org](https://kaikki.org/dictionary/), snapshot in `meta.json` | CC BY-SA 4.0 |

## Entry

| Field | Holds |
|---|---|
| `w` | headword, Mkhedruli |
| `l` | Latin transliteration |
| `ipa` | IPA in slashes; optional |
| `d` | variety, e.g. Upper Bal; optional |
| `v` | tier A: `g` English gloss, `r` citation in the printed source (headword, entry no., page) |
| `s` | tier B: senses, `[{pos, g: [glosses]}]`; attribution = `https://en.wiktionary.org/wiki/<w>#<Language>` |

## Corrections

- Tier B wrong: fix it on Wiktionary; the next snapshot brings it in. Or open an issue.
- Tier A wrong, or a form missing: issue or PR with the source (book, page, entry). Citations only; never copy text
  from an all-rights-reserved dictionary.
- The JSON is regenerated from the snapshot: hand edits to `s` are overwritten.
