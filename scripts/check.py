"""Validate all content as kartvelian.eu reads it. Same script as CI.

    python3 -m pip install -r scripts/requirements.txt
    python3 scripts/check.py          # repo root; exit 1 + problem list
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

import toons
import yaml

ROOT = Path(__file__).resolve().parent.parent
LANGUAGES = ("georgian", "svan", "megrelian", "laz")
FRONTMATTER = ("language", "level", "levelTitle", "cefr", "module", "pageSlug", "title", "description", "publishedAt")
OPTIONAL = ("updatedAt",)
ICONS = {"sprout", "compass", "pillar", "hourglass", "feather", "book"}
MKHEDRULI = re.compile(r"[ა-ჿ]")
IPA = re.compile(r"^/.+/$")

problems = []


def bad(path, msg):
    problems.append(f"{path.relative_to(ROOT)}: {msg}")


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        bad(path, "no frontmatter (--- … --- at top)")
        return None, text
    try:
        return yaml.safe_load(m.group(1)) or {}, text[m.end():]
    except yaml.YAMLError as e:
        bad(path, f"frontmatter not YAML: {e}")
        return None, text


def check_curricula():
    modules = {}
    for lang in LANGUAGES:
        path = ROOT / "curricula" / f"{lang}.yaml"
        if not path.exists():
            bad(ROOT / "curricula", f"missing {lang}.yaml (all four required)")
            continue
        levels = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("levels") or []
        seen_nums = set()
        for level in levels:
            for key in ("id", "icon", "title", "cefr", "focus", "modules"):
                if not level.get(key):
                    bad(path, f"level {level.get('id', '?')} has no {key}")
            if level.get("icon") and level["icon"] not in ICONS:
                bad(path, f"level {level['id']}: icon must be one of {sorted(ICONS)}")
            for mod in level.get("modules") or []:
                for key in ("num", "title", "blurb", "slug"):
                    if not mod.get(key):
                        bad(path, f"a module in {level.get('id')} has no {key}")
                if mod.get("num") in seen_nums:
                    bad(path, f"module num {mod['num']} used twice")
                seen_nums.add(mod.get("num"))
                modules[(lang, level.get("id"), mod.get("slug"))] = (level, mod)
    return modules


def check_lessons(modules):
    found = set()
    for lang in LANGUAGES:
        folder = ROOT / "lessons" / lang
        if not folder.is_dir():
            bad(ROOT / "lessons", f"missing {lang}/ (all four required)")
            continue
        for path in sorted(folder.iterdir()):
            if path.name == "README.md":
                continue
            if path.suffix != ".md":
                bad(path, "plain .md only (no .mdx)")
                continue
            fm, body = frontmatter(path)
            if fm is None:
                continue
            for key in FRONTMATTER:
                if fm.get(key) in (None, ""):
                    bad(path, f"frontmatter has no {key}")
            for key in set(fm) - set(FRONTMATTER) - set(OPTIONAL):
                bad(path, f"unknown frontmatter key {key}")
            if fm.get("language") != lang:
                bad(path, f"language {fm.get('language')!r} ≠ folder lessons/{lang}/")
            for key in ("publishedAt", *OPTIONAL):
                if key in fm and not isinstance(fm[key], date):
                    bad(path, f"{key}: YYYY-MM-DD")
            if not isinstance(fm.get("module"), int):
                bad(path, "module: number")
            key = (lang, fm.get("level"), fm.get("pageSlug"))
            hit = modules.get(key)
            if not hit:
                bad(path, f"no module {key[1]}/{key[2]} in curricula/{lang}.yaml")
            else:
                level, mod = hit
                if fm.get("module") != mod["num"]:
                    bad(path, f"module {fm.get('module')} ≠ curricula/{lang}.yaml {mod['num']}")
                want = f"level-{str(level['id']).removeprefix('level-')}-{mod['num']}-{mod['slug']}.md"
                if path.name != want:
                    bad(path, f"rename to {want}")
            if re.search(r"^\s*(import|export) ", body, re.M):
                bad(path, "no import/export lines")
            found.add(key)
    for key in modules.keys() - found:
        bad(ROOT / "curricula" / f"{key[0]}.yaml", f"module {key[1]}/{key[2]}: no lesson file")


def check_alphabets():
    for path in sorted((ROOT / "alphabets").glob("*.json")):
        try:
            letters = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            bad(path, f"not valid JSON: {e}")
            continue
        # Georgian IPA: generated. Others: hand-written.
        needs_ipa = not path.stem.startswith("georgian")
        seen = set()
        for i, entry in enumerate(letters, 1):
            where = f"entry {i} ({entry.get('letter', '?')})"
            for key in ("letter", "name", "word", "meaning"):
                if not entry.get(key):
                    bad(path, f"{where} has no {key}")
            for key in ("letterIpa", "wordIpa"):
                if needs_ipa and not entry.get(key):
                    bad(path, f"{where} has no {key}")
                if entry.get(key) and not IPA.match(entry[key]):
                    bad(path, f"{where}: {key} in slashes, /ɑ/")
            if entry.get("letter") in seen:
                bad(path, f"{where}: duplicate letter")
            seen.add(entry.get("letter"))


def check_toon(path, required, headword):
    try:
        rows = toons.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001 - toons has its own error types
        bad(path, f"TOON parse: {e}")
        return
    seen = set()
    for i, row in enumerate(rows, 1):
        for key in required:
            if row.get(key) in (None, ""):
                bad(path, f"row {i} has no {key}")
        word = str(row.get(headword) or "")
        if word and not MKHEDRULI.search(word):
            bad(path, f"row {i}: {headword} {word!r}: no Mkhedruli")
        if any('"' in str(v) for v in row.values()):
            bad(path, f"row {i}: stray quote; quote whole cell (docs/toon.md)")
        if word in seen:
            bad(path, f"row {i}: duplicate {word!r}")
        seen.add(word)


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        bad(path, f"not valid JSON: {e}")
        return None


def check_dictionary():
    for lang in LANGUAGES:
        path = ROOT / "dictionary" / f"{lang}.json"
        if not path.exists():
            bad(ROOT / "dictionary", f"missing {lang}.json (all four required)")
            continue
        entries = load_json(path)
        if entries is None:
            continue
        seen = set()
        for i, e in enumerate(entries, 1):
            w = e.get("w") or ""
            where = f"entry {i} ({w or '?'})"
            if not MKHEDRULI.search(w):
                bad(path, f"{where}: w: Mkhedruli headword")
            symbol = all(s.get("pos") == "symbol" for s in e.get("s") or [{}])
            if not e.get("l") and not symbol:
                bad(path, f"{where} has no l (transliteration)")
            if not e.get("v") and not e.get("s"):
                bad(path, f"{where}: needs v (verified) or s (Wiktionary)")
            if e.get("v") and not e["v"].get("g"):
                bad(path, f"{where}: v has no g (gloss)")
            for s in e.get("s") or []:
                if not s.get("pos") or not s.get("g"):
                    bad(path, f"{where}: each sense needs pos + g")
            if e.get("ipa") and not IPA.match(e["ipa"]):
                bad(path, f"{where}: ipa in slashes, /ɑ/")
            if (w, e.get("d")) in seen:
                bad(path, f"{where}: duplicate headword")
            seen.add((w, e.get("d")))


def check_verbs():
    for path in sorted((ROOT / "verbs").glob("*.json")):
        data = load_json(path)
        if data is None:
            continue
        if data.get("language") != path.stem:
            bad(path, f"language {data.get('language')!r} ≠ file name")
        ids = set()
        for verb in data.get("verbs") or []:
            vid = verb.get("id", "?")
            for key in ("id", "masdar", "masdarTranslit", "english", "tenses"):
                if not verb.get(key):
                    bad(path, f"verb {vid} has no {key}")
            if vid in ids:
                bad(path, f"verb {vid}: duplicate id")
            ids.add(vid)
            for tense in verb.get("tenses") or []:
                tid = f"{vid}/{tense.get('id', '?')}"
                for key in ("id", "screeve", "series", "subject", "forms"):
                    if not tense.get(key):
                        bad(path, f"{tid} has no {key}")
                for form in tense.get("forms") or []:
                    for key in ("person", "form", "formTranslit"):
                        if not form.get(key):
                            bad(path, f"{tid} {form.get('person', '?')} has no {key}")


def main():
    check_lessons(check_curricula())
    check_alphabets()
    for path in sorted((ROOT / "decks").glob("*/*.toon")):
        check_toon(path, ("term", "meaning"), "term")
    check_dictionary()
    check_verbs()
    for path in sorted((ROOT / "wordlists").glob("*.toon")):
        check_toon(path, ("word", "meaning_en", "pos", "category"), "word")
    if problems:
        print("\n".join(problems))
        print(f"\n{len(problems)} problem(s)")
        sys.exit(1)
    print("ok")


if __name__ == "__main__":
    main()
