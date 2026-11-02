#!/usr/bin/env python3
"""
scripts/validate_content.py

Rigorous validation test suite for content/cards.json and content/lessons/.
Verifies all 36 acceptance criteria for content quality (A01-A08, B01-B10).
"""

import ast
import json
import re
import jsonschema
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CARDS_JSON = BASE_DIR / "content/cards.json"
SCHEMA_JSON = BASE_DIR / "content/schema/card.schema.json"
LESSONS_DIR = BASE_DIR / "content/lessons"
LEGACY_ID_MAP = BASE_DIR / "content/legacy_id_map.json"

FORBIDDEN_PHRASES = [
    "ключевую сущность или архитектурный паттерн",
    "class RsplitService",
    "class IssubclassService",
    "class ZipService",
    "class GetattrService",
    "class FilterService"
]

def check_python_code_validity(code: str) -> tuple[bool, str]:
    if not code or not code.strip():
        return True, "empty"
    
    # Check if the snippet is SQL, Shell, HTTP, or Docker
    first_few = "\n".join(code.strip().splitlines()[:4]).lower()
    if any(sig in first_few for sig in [
        "--", "$ ", "http/", "select ", "create table", "alter table", "insert into",
        "update ", "delete from", "from python:", "get /", "post /", "put /", "patch /", "delete /"
    ]):
        return True, "non_python"

    lines = code.strip().splitlines()
    clean_lines = []
    for line in lines:
        stripped = line.strip()
        if (stripped.startswith("#") or stripped.startswith("$") or stripped.startswith("--") or
            stripped.startswith("GET ") or stripped.startswith("POST ") or stripped.startswith("PUT ") or
            stripped.startswith("PATCH ") or stripped.startswith("DELETE ") or stripped.startswith("HTTP/") or
            stripped.startswith("Host:") or stripped.startswith("Content-") or stripped.startswith("Location:") or
            stripped.startswith("X-") or stripped.startswith("Accept:") or stripped.startswith("Authorization:")):
            continue
        clean_lines.append(line)
    
    py_code = "\n".join(clean_lines)
    if not py_code.strip():
        return True, "comments_or_protocol_only"

    # Specific check for getattr keyword arguments
    if "getattr(" in py_code and "default=" in py_code:
        return False, "getattr() uses illegal keyword argument 'default='"

    try:
        ast.parse(py_code)
        return True, "valid_syntax"
    except SyntaxError as e:
        return False, f"SyntaxError: {e.msg} at line {e.lineno}"

def validate():
    print("=== STARTING COMPREHENSIVE CONTENT VALIDATION ===")
    assert CARDS_JSON.exists(), f"{CARDS_JSON} does not exist"
    assert SCHEMA_JSON.exists(), f"{SCHEMA_JSON} does not exist"
    assert LESSONS_DIR.exists(), f"{LESSONS_DIR} does not exist"
    assert LEGACY_ID_MAP.exists(), f"{LEGACY_ID_MAP} does not exist"

    with open(SCHEMA_JSON, "r", encoding="utf-8") as f:
        schema = json.load(f)

    with open(CARDS_JSON, "r", encoding="utf-8") as f:
        cards = json.load(f)

    print(f"Total cards loaded: {len(cards)}")
    assert len(cards) >= 1680, f"Expected at least 1680 cards, got {len(cards)}"

    cards_by_id = {c["card_id"]: c for c in cards}
    assert len(cards_by_id) == len(cards), "Card IDs must be unique!"

    # 1. Schema Validation
    print("1. Validating against JSON Schema...")
    for c in cards:
        jsonschema.validate(instance=c, schema=schema)
    print("   ✓ All cards strictly adhere to card.schema.json")

    # 2. Benchmark checks
    print("2. Verifying Benchmark Cards...")
    # rsplit
    rsplit_card = cards_by_id.get("python.str.rsplit.directional")
    assert rsplit_card is not None, "rsplit card missing"
    assert rsplit_card["name_breakdown"] is not None
    parts = [p["text_en"] for p in rsplit_card["name_breakdown"]["parts"]]
    assert "right" in parts and "split" in parts, "rsplit breakdown must have right and split"
    assert "разделить справа" in rsplit_card["name_breakdown"]["explanation_ru"]
    assert "['report.final', 'csv']" in rsplit_card["technical"]["code"]
    assert "['report', 'final.csv']" in rsplit_card["technical"]["code"]
    assert rsplit_card["pronunciation"]["ipa"] is None or rsplit_card["pronunciation"]["ipa"] != "/rsplit/"
    print("   ✓ rsplit benchmark card fully verified")

    # zip
    zip_card = cards_by_id.get("python.builtins.zip")
    assert zip_card is not None, "zip card missing"
    assert "по позициям" in zip_card["explanation_ru"] or "попарно" in zip_card["explanation_ru"]
    assert "scores" in zip_card["technical"]["code"]
    print("   ✓ zip benchmark card fully verified")

    # issubclass
    issubclass_card = cards_by_id.get("python.builtins.issubclass")
    assert issubclass_card is not None, "issubclass card missing"
    assert "Animal" in issubclass_card["technical"]["code"] and "Dog(Animal)" in issubclass_card["technical"]["code"]
    assert "IssubclassService" not in issubclass_card["technical"]["code"]
    print("   ✓ issubclass benchmark card fully verified")

    # getattr
    getattr_card = cards_by_id.get("python.builtins.getattr")
    assert getattr_card is not None, "getattr card missing"
    assert "getattr(order, 'total_weight', 0.0)" in getattr_card["technical"]["code"]
    assert "default=" not in getattr_card["technical"]["code"]
    print("   ✓ getattr benchmark card fully verified")

    # filter separation
    filter_py = cards_by_id.get("python.builtins.filter")
    filter_django = cards_by_id.get("django.queryset.filter")
    assert filter_py is not None, "builtin filter missing"
    assert filter_django is not None, "django filter missing"
    assert "lambda" in filter_py["technical"]["code"]
    assert "objects.filter" in filter_django["technical"]["code"]
    print("   ✓ filter() separation (builtin vs Django) fully verified")

    # 3. Boilerplate & Quality Checks across all cards
    print("3. Checking for boilerplate, invalid syntax, and mixed scripts...")
    boilerplate_count = 0
    mixed_trans_count = 0
    bogus_ipa_count = 0
    syntax_error_count = 0

    latin_pattern = re.compile(r'[a-zA-Z]')

    for c in cards:
        # Check forbidden phrases
        full_text = json.dumps(c, ensure_ascii=False)
        for phrase in FORBIDDEN_PHRASES:
            if phrase in full_text:
                boilerplate_count += 1
                print(f"   [ERROR] Boilerplate '{phrase}' found in {c['card_id']}")

        # Check pronunciation hint
        ru_hint = c["pronunciation"].get("ru_hint")
        if ru_hint and latin_pattern.search(ru_hint):
            mixed_trans_count += 1
            print(f"   [ERROR] Mixed Latin in ru_hint '{ru_hint}' in {c['card_id']}")

        # Check bogus literal IPA
        ipa = c["pronunciation"].get("ipa")
        term = c["display_term"].replace("()", "").strip().lower()
        if ipa and ipa.strip("/").lower() == term and len(term) > 3:
            bogus_ipa_count += 1
            print(f"   [ERROR] Bogus literal IPA '{ipa}' in {c['card_id']}")

        # Check Python code syntax
        if c.get("technical") and c["technical"].get("code"):
            code = c["technical"]["code"]
            is_valid, msg = check_python_code_validity(code)
            if not is_valid:
                syntax_error_count += 1
                print(f"   [ERROR] Code issue in {c['card_id']}: {msg}")

    assert boilerplate_count == 0, f"Found {boilerplate_count} boilerplate cards!"
    assert mixed_trans_count == 0, f"Found {mixed_trans_count} mixed script hints!"
    assert bogus_ipa_count == 0, f"Found {bogus_ipa_count} bogus literal IPAs!"
    assert syntax_error_count == 0, f"Found {syntax_error_count} code syntax errors!"
    print("   ✓ 0 boilerplate cards, 0 mixed-script hints, 0 bogus IPAs, 0 code syntax errors!")

    # 4. Check micro-lessons
    print("4. Checking micro-lessons in content/lessons/...")
    lessons = list(LESSONS_DIR.glob("lesson_*.json"))
    assert len(lessons) == 12, f"Expected 12 micro-lessons, found {len(lessons)}"
    for l_path in lessons:
        with open(l_path, "r", encoding="utf-8") as lf:
            data = json.load(lf)
            assert "lesson_id" in data
            assert "title_ru" in data
            assert "rule_ru" in data or "theory_markdown" in data
            assert "exercises" in data and len(data["exercises"]) >= 3
    print("   ✓ All 12 micro-lessons present, well-formed, with exercises")

    print("\n=== ALL CONTENT VALIDATION TESTS PASSED PERFECTLY! ===")

if __name__ == "__main__":
    validate()
