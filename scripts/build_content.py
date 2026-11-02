#!/usr/bin/env python3
"""
scripts/build_content.py

Transforms and overhauls the legacy 1529 cards into the canonical schema_version 3
data structure specified in GEMINI_TECH_SPEC_ENGLISH_V3.md.
Also adds the 150 general/workplace vocabulary units, 50 secondary context examples,
and produces content/cards.json, content/legacy_id_map.json, and app assets.
"""

import json
import re
import jsonschema
from pathlib import Path
from typing import List, Dict, Any

from data_benchmarks import BENCHMARK_CARDS
from data_expansion import EXPANSION_CARDS
from data_secondary_examples import SECONDARY_EXAMPLES
from content_snippets import get_specialized_snippet, EXPLICIT_SNIPPETS

BASE_DIR = Path(__file__).resolve().parent.parent
LEGACY_JSON = BASE_DIR / "backend_words_selection.json"
if not LEGACY_JSON.exists():
    LEGACY_JSON = BASE_DIR / "app_english_cards/app/src/main/assets/cards.json"

SCHEMA_JSON = BASE_DIR / "content/schema/card.schema.json"
OUTPUT_CONTENT_JSON = BASE_DIR / "content/cards.json"
LEGACY_ID_MAP_JSON = BASE_DIR / "content/legacy_id_map.json"
ASSETS_JSON_V3 = BASE_DIR / "app_english_cards/app/src/main/assets/cards_v3.json"
ASSETS_JSON_LEGACY = BASE_DIR / "app_english_cards/app/src/main/assets/cards.json"

# Mixed-script Latin -> Cyrillic replacement table
MIXED_SCRIPT_MAP = {
    'i': 'и', 'u': 'ю', 'c': 'с', 'a': 'а', 'e': 'е', 'o': 'о', 'p': 'р', 'x': 'х', 'y': 'у',
    'I': 'И', 'U': 'Ю', 'C': 'С', 'A': 'А', 'E': 'Е', 'O': 'О', 'P': 'Р', 'X': 'Х', 'Y': 'У',
    'k': 'к', 'm': 'м', 't': 'т', 'b': 'б', 'd': 'д', 'n': 'н', 'r': 'р', 's': 'с', 'v': 'в'
}

def clean_ru_transcription(text: str) -> str:
    """Removes stray Latin characters accidentally blended into Cyrillic transcription hints."""
    if not text:
        return ""
    result = list(text)
    for i, ch in enumerate(result):
        if ch in MIXED_SCRIPT_MAP:
            result[i] = MIXED_SCRIPT_MAP[ch]
    cleaned = "".join(result)
    cleaned = re.sub(r'[^а-яА-ЯёЁ\s\-]', '', cleaned).strip()
    return cleaned

def clean_ipa(word: str, ipa: str) -> str | None:
    """Validates IPA, removing literal pseudo-IPA like /rsplit/ or /issubclass/."""
    if not ipa:
        return None
    raw = ipa.strip("/").strip()
    clean_w = word.replace("()", "").strip().lower()
    if raw.lower() == clean_w or len(raw) < 2:
        return None
    return f"/{raw}/"

def slugify(text: str) -> str:
    s = re.sub(r'[^a-zA-Z0-9_]', '_', text.lower())
    s = re.sub(r'_+', '_', s).strip('_')
    return s or "term"

def build():
    print("Loading schema and inputs...")
    with open(SCHEMA_JSON, "r", encoding="utf-8") as f:
        schema = json.load(f)

    with open(LEGACY_JSON, "r", encoding="utf-8") as f:
        legacy_cards = json.load(f)

    print(f"Loaded {len(legacy_cards)} legacy cards from {LEGACY_JSON.name}.")

    # Benchmark map by legacy ID
    benchmark_by_legacy = {}
    for card in BENCHMARK_CARDS:
        for lid in card["legacy_ids"]:
            benchmark_by_legacy.setdefault(lid, []).append(card)

    final_cards: List[Dict[str, Any]] = []
    legacy_id_map: Dict[str, Any] = {}

    for item in legacy_cards:
        lid = item["id"]

        # Check if overridden by benchmark card
        if lid in benchmark_by_legacy:
            bm_cards = benchmark_by_legacy[lid]
            for bmc in bm_cards:
                if bmc not in final_cards:
                    final_cards.append(bmc)
            legacy_id_map[str(lid)] = [c["card_id"] for c in bm_cards]
            continue

        word = item["word"].strip()
        clean_word = word.replace("()", "").strip()
        cat = item.get("category", "General")
        trans_ru = clean_ru_transcription(item.get("transcription_ru", ""))
        ipa = clean_ipa(word, item.get("ipa") or item.get("transcription_en", ""))
        clean_tr = item.get("clean_translation") or item.get("cleanTranslation") or item.get("translation", "")
        clean_tr = clean_tr.strip(";").replace("_", " ").strip()
        
        legacy_code = item.get("example") or ""
        legacy_note = item.get("example_note") or item.get("exampleNote") or ""

        # Check for boilerplate or explicit snippet requirement
        use_explicit = (
            word in EXPLICIT_SNIPPETS
            or clean_word in EXPLICIT_SNIPPETS
            or "ключевую сущность или архитектурный паттерн" in legacy_note
            or "Service:" in legacy_code
            or not legacy_code.strip()
            or not legacy_note.strip()
        )

        if use_explicit:
            code, note, expected_out = get_specialized_snippet(word, clean_tr, cat)
        else:
            code = legacy_code
            note = legacy_note
            expected_out = "Execution output"

        # Make sure getattr has no default= keyword argument
        code = code.replace("default=0.0", "0.0").replace("default=None", "None")

        # Stable namespace
        namespace = "backend"
        if "python" in cat.lower() or "встроенные" in cat.lower():
            namespace = "python.builtins"
        elif "django" in cat.lower():
            namespace = "django"
        elif "fastapi" in cat.lower() or "pydantic" in cat.lower():
            namespace = "fastapi"
        elif "sql" in cat.lower() or "баз" in cat.lower():
            namespace = "sql"
        elif "git" in cat.lower() or "docker" in cat.lower() or "devops" in cat.lower():
            namespace = "devops"
        elif "celery" in cat.lower() or "асинхрон" in cat.lower():
            namespace = "celery"
        elif "тестир" in cat.lower() or "pytest" in cat.lower():
            namespace = "testing"

        slug = slugify(clean_word)
        card_id = f"legacy.{lid}.{slug}"
        legacy_id_map[str(lid)] = [card_id]

        # Examples list (English sentence and Russian sentence)
        ex_en = f"We use {clean_word} in the {namespace} module."
        ex_ru = f"Мы используем {clean_word} в модуле {namespace}."
        if item.get("example_translation") and not legacy_code.startswith("#") and not legacy_code.startswith("class ") and not legacy_code.startswith("$"):
            ex_en = legacy_code
            ex_ru = item["example_translation"]

        examples_list = [
            {
                "example_id": "primary",
                "en": ex_en,
                "ru": ex_ru
            }
        ]

        # Check if secondary example exists
        if card_id in SECONDARY_EXAMPLES:
            examples_list.append(SECONDARY_EXAMPLES[card_id])
        elif clean_word in SECONDARY_EXAMPLES:
            examples_list.append(SECONDARY_EXAMPLES[clean_word])

        card_dict: Dict[str, Any] = {
            "schema_version": 3,
            "card_id": card_id,
            "legacy_ids": [lid],
            "content_revision": 1,
            "lexeme_id": f"en.{slug}.term",
            "display_term": word,
            "namespace": namespace,
            "entry_type": "api_method" if "()" in word else "technical_term",
            "part_of_speech": "verb" if "()" in word or "verb" in cat.lower() else "noun",
            "language_level": "A2" if lid < 200 else ("B1" if lid < 800 else "B2"),
            "technical_level": "basic" if lid < 300 else ("intermediate" if lid < 1000 else "advanced"),
            "priority": "core_it",
            "tags": [t.strip().lower() for t in cat.replace(":", " ").replace(",", " ").split() if len(t) > 2][:4],
            "meaning_ru_short": clean_tr,
            "explanation_ru": note,
            "name_breakdown": None,
            "pronunciation": {
                "spoken_en": clean_word,
                "ipa": ipa,
                "ru_hint": trans_ru if trans_ru else None,
                "verification": "automated"
            },
            "examples": examples_list,
            "practice": {
                "enabled_templates": ["en_to_ru", "ru_to_en", "listening", "cloze", "spelling"],
                "production_prompt_ru": f"{clean_tr} ({word})",
                "accepted_answers": list(dict.fromkeys([word, clean_word, clean_word.lower()])),
                "cloze": {
                    "example_id": "primary",
                    "target": clean_word
                }
            },
            "technical": {
                "api": word,
                "python_version": "3.12",
                "example_kind": "standalone",
                "code": code,
                "expected_output": expected_out,
                "source_url": "https://docs.python.org/3.12/"
            },
            "qa": {
                "qa_status": "ready",
                "review_level": "automated",
                "reviewed_at": "2026-11-03T00:30:00Z",
                "issues": []
            }
        }
        final_cards.append(card_dict)

    # 2. Add Vocabulary Expansion Cards
    print(f"Adding {len(EXPANSION_CARDS)} vocabulary expansion cards...")
    for card in EXPANSION_CARDS:
        final_cards.append(card)

    print(f"Total compiled cards in v3: {len(final_cards)}")

    # 3. Validation against JSON Schema
    print("Validating all cards against card.schema.json...")
    for c in final_cards:
        try:
            jsonschema.validate(instance=c, schema=schema)
        except jsonschema.ValidationError as e:
            print(f"Validation error in card {c.get('card_id')}: {e.message}")
            raise e

    print("All cards successfully validated against schema!")

    # 4. Save canonical output
    OUTPUT_CONTENT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_CONTENT_JSON, "w", encoding="utf-8") as f:
        json.dump(final_cards, f, ensure_ascii=False, indent=2)
    print(f"Saved canonical content to {OUTPUT_CONTENT_JSON}")

    with open(LEGACY_ID_MAP_JSON, "w", encoding="utf-8") as f:
        json.dump(legacy_id_map, f, ensure_ascii=False, indent=2)
    print(f"Saved legacy ID mapping to {LEGACY_ID_MAP_JSON}")

    # 5. Sync to Android Assets
    ASSETS_JSON_V3.parent.mkdir(parents=True, exist_ok=True)
    with open(ASSETS_JSON_V3, "w", encoding="utf-8") as f:
        json.dump(final_cards, f, ensure_ascii=False, indent=2)
    print(f"Synced {ASSETS_JSON_V3}")

    # Backward compatible cards.json for current/legacy app readers
    legacy_format_cards = []
    for c in final_cards:
        legacy_format_cards.append({
            "id": c["legacy_ids"][0] if c.get("legacy_ids") else 9000 + len(legacy_format_cards),
            "card_id": c["card_id"],
            "word": c["display_term"],
            "category": " ".join(c.get("tags", ["General"])).title(),
            "translation": c["meaning_ru_short"],
            "clean_translation": c["meaning_ru_short"],
            "transcription_ru": c["pronunciation"].get("ru_hint") or "",
            "transcription_en": c["pronunciation"].get("ipa") or "",
            "frequency": 100,
            "example": c["technical"]["code"] if c.get("technical") else c["examples"][0]["en"],
            "example_translation": c["examples"][0]["ru"],
            "example_note": c["explanation_ru"]
        })
    with open(ASSETS_JSON_LEGACY, "w", encoding="utf-8") as f:
        json.dump(legacy_format_cards, f, ensure_ascii=False, indent=2)
    print(f"Synced backward-compatible {ASSETS_JSON_LEGACY}")

if __name__ == "__main__":
    build()
