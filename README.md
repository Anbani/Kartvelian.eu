# Kartvelian.eu content

Lessons, curricula, alphabets, flashcards, dictionary and verb tables behind **[kartvelian.eu](https://kartvelian.eu)**: Georgian,
Svan, Megrelian and Laz for English speakers. Plain text, [CC BY-SA 4.0](LICENSE), open to corrections.

| Path | Holds | On the site |
|---|---|---|
| [`lessons/<language>/`](lessons) | one Markdown file per lesson | `/<language>/curriculum/…` |
| [`curricula/<language>.yaml`](curricula) | levels → modules | `/<language>/curriculum` |
| [`alphabets/<language>.json`](alphabets) | letters, names, words, IPA | `/<language>/alphabet`, alphabet cards |
| [`decks/<language>/*.toon`](decks) | flashcards, `term\|meaning` | `/<language>/flashcards`, Anki decks |
| [`dictionary/<language>.json`](dictionary) | headwords: verified + Wiktionary | `/<language>/dictionary`, search; Svan, Megrelian, Laz games |
| [`verbs/georgian.json`](verbs) | conjugation tables | `/georgian/verbs` |
| [`wordlists/georgian.toon`](wordlists) | Georgian game + vocabulary words | vocabulary cards, Georgian Wordle, Waffle, Crossword |

| | Georgian | Svan | Megrelian | Laz |
|---|---|---|---|---|
| Lessons | 19 | 2 | 2 | 2 |
| Alphabet | 33 | 37 + vowel marks | 36 | 35, Mkhedruli + Latin |
| Decks | phrases, vocabulary | wanted | wanted | wanted |
| Dictionary | 22,000 (33 verified) | 307 (66 verified) | 685 (54 verified) | 2,030 (53 verified) |
| Verbs | 32 | wanted | wanted | wanted |

Same scaffold for all four; Svan, Megrelian and Laz need content most.

## Contribute

- Typo or wrong translation: pencil icon on GitHub → propose change.
- Problem, no edit: [open an issue](../../issues/new/choose).
- Larger change: fork, edit, `python3 -m pip install -r scripts/requirements.txt && python3 scripts/check.py`, PR.

Details: [CONTRIBUTING.md](CONTRIBUTING.md). Georgian transliteration and IPA are generated; never type them in decks.

## Site sync

kartvelian.eu builds from its own copy; maintainers sync merged PRs into it. Site code is not here.

## License

[CC BY-SA 4.0](LICENSE). Dictionary senses marked `s`: English Wiktionary contributors, via kaikki.org, CC BY-SA
4.0 ([docs/dictionary.md](docs/dictionary.md)). Credit "Kartvelian.eu contributors" with a link; share adaptations alike. PRs are licensed
the same way.
