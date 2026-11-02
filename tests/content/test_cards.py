"""tests/content/test_cards.py

Pytest suite validating content requirements according to GEMINI_TECH_SPEC_ENGLISH_V3.md.
"""

import json
from pathlib import Path
import jsonschema

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CARDS_PATH = BASE_DIR / "content/cards.json"
SCHEMA_PATH = BASE_DIR / "content/schema/card.schema.json"
LESSONS_DIR = BASE_DIR / "content/lessons"

def test_cards_json_schema():
    assert CARDS_PATH.exists()
    assert SCHEMA_PATH.exists()
    with open(CARDS_PATH, "r", encoding="utf-8") as f:
        cards = json.load(f)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)

    assert len(cards) >= 1680
    for card in cards:
        jsonschema.validate(instance=card, schema=schema)

def test_benchmark_rsplit():
    with open(CARDS_PATH, "r", encoding="utf-8") as f:
        cards = json.load(f)
    rsplit = next((c for c in cards if c["card_id"] == "python.str.rsplit.directional"), None)
    assert rsplit is not None
    assert rsplit["name_breakdown"] is not None
    parts = [p["text_en"] for p in rsplit["name_breakdown"]["parts"]]
    assert "right" in parts
    assert "split" in parts
    assert "разделить справа" in rsplit["name_breakdown"]["explanation_ru"]
    assert "['report.final', 'csv']" in rsplit["technical"]["code"]
    assert "['report', 'final.csv']" in rsplit["technical"]["code"]
    assert rsplit["pronunciation"]["ipa"] != "/rsplit/"

def test_benchmark_zip():
    with open(CARDS_PATH, "r", encoding="utf-8") as f:
        cards = json.load(f)
    zip_card = next((c for c in cards if c["card_id"] == "python.builtins.zip"), None)
    assert zip_card is not None
    assert "scores" in zip_card["technical"]["code"]
    assert "('Anna', 90)" in zip_card["technical"]["code"]

def test_benchmark_issubclass():
    with open(CARDS_PATH, "r", encoding="utf-8") as f:
        cards = json.load(f)
    sub = next((c for c in cards if c["card_id"] == "python.builtins.issubclass"), None)
    assert sub is not None
    assert "Animal" in sub["technical"]["code"]
    assert "Dog(Animal)" in sub["technical"]["code"]
    assert "IssubclassService" not in sub["technical"]["code"]

def test_benchmark_getattr():
    with open(CARDS_PATH, "r", encoding="utf-8") as f:
        cards = json.load(f)
    ga = next((c for c in cards if c["card_id"] == "python.builtins.getattr"), None)
    assert ga is not None
    assert "getattr(order, 'total_weight', 0.0)" in ga["technical"]["code"]
    assert "default=" not in ga["technical"]["code"]

def test_filter_separation():
    with open(CARDS_PATH, "r", encoding="utf-8") as f:
        cards = json.load(f)
    f_py = next((c for c in cards if c["card_id"] == "python.builtins.filter"), None)
    f_dj = next((c for c in cards if c["card_id"] == "django.queryset.filter"), None)
    assert f_py is not None
    assert f_dj is not None
    assert f_py["card_id"] != f_dj["card_id"]

def test_no_boilerplate_or_mixed_scripts():
    with open(CARDS_PATH, "r", encoding="utf-8") as f:
        cards = json.load(f)
    for c in cards:
        assert "ключевую сущность или архитектурный паттерн" not in json.dumps(c, ensure_ascii=False)
        ru_hint = c["pronunciation"].get("ru_hint")
        if ru_hint:
            # No latin letters in ru_hint
            assert not any('a' <= ch.lower() <= 'z' for ch in ru_hint), f"Latin in ru_hint: {ru_hint} in {c['card_id']}"

def test_micro_lessons_present():
    lessons = list(LESSONS_DIR.glob("lesson_*.json"))
    assert len(lessons) == 12
    for p in lessons:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert "lesson_id" in data
            assert len(data.get("exercises", [])) == 3
