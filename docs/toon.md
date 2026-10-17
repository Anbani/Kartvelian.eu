# TOON

Decks and the dictionary: one header line, one row per line, cells split by `|`.

```
[3|]{term|meaning}:
  გამარჯობა|Hello
  "კარგად, მადლობა"|I'm fine, thanks
  ნახვამდის|Goodbye
```

- `[3|]`: row count (keep it current) and separator.
- `{term|meaning}`: columns, in order.
- Rows indented two spaces.
- Cell with a comma, `|`, colon or edge spaces: quote the whole cell. Never quote mid-cell.
- Empty value: `null`.

`python3 scripts/check.py` names the broken row.
