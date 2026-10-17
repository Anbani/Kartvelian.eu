# Verbs (`verbs/georgian.json`)

Georgian conjugation tables behind `/georgian/verbs`. Romanization: national 2002.

| Level | Keys |
|---|---|
| file | `language`, `romanization`, `verbs[]` |
| verb | `id`, `masdar` (verbal noun, Mkhedruli), `masdarTranslit`, `english`, `rootGloss`, `note`, `tenses[]` |
| tense | `id`, `screeve` (Georgian name), `screeveTranslit`, `series` (1–3), `subject` case (`nom`/`erg`/`dat`), `forms[]` |
| form | `person` (`1sg` … `3pl`), `form`, `formTranslit`, `phrase`, `phraseTranslit`, `english`, `segments` |

Wrong form: issue or PR with a grammar reference (book, page, table).
