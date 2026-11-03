#!/usr/bin/env python3
"""
scripts/build_content.py

Canonical content management and publication script conforming to GEMINI_TECH_SPEC_ENGLISH_V4.md (V4-C01).
- Canonical source: content/cards.json
- Preserves manual editorial changes, custom sentences, and revisions.
- Does NOT overwrite editorial content when run with --check or --dry-run.
- Validates schema, IDs, absence of boilerplate templates, and syncs to assets only upon success.
"""

import sys
import json
import argparse
import jsonschema
from pathlib import Path
from typing import List, Dict, Any

BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_CARDS_JSON = BASE_DIR / "content/cards.json"
SCHEMA_JSON = BASE_DIR / "content/schema/card.schema.json"
LEGACY_ID_MAP_JSON = BASE_DIR / "content/legacy_id_map.json"

ASSETS_DIR = BASE_DIR / "app_english_cards/app/src/main/assets"
ASSETS_CARDS_V3_JSON = ASSETS_DIR / "cards_v3.json"
ASSETS_CARDS_LEGACY_JSON = ASSETS_DIR / "cards.json"
ASSETS_LEGACY_ID_MAP_JSON = ASSETS_DIR / "legacy_id_map.json"
ASSETS_LESSONS_DIR = ASSETS_DIR / "lessons"
CONTENT_LESSONS_DIR = BASE_DIR / "content/lessons"

def validate_cards_data(cards: List[Dict[str, Any]], schema: Dict[str, Any]) -> List[str]:
    """Strictly validates all cards for schema adherence, lack of templates, and integrity."""
    errors = []
    
    if len(cards) < 1680:
        errors.append(f"Card count below requirement: {len(cards)} < 1680")

    card_ids = set()
    cards_with_secondary = 0

    for idx, c in enumerate(cards):
        cid = c.get("card_id")
        if not cid:
            errors.append(f"Card at index {idx} missing card_id")
            continue
        if cid in card_ids:
            errors.append(f"Duplicate card_id found: {cid}")
        card_ids.add(cid)

        # 1. Schema check
        try:
            jsonschema.validate(instance=c, schema=schema)
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation error in card {cid}: {e.message}")

        # 2. Template check
        for ex in c.get("examples", []):
            en_text = ex.get("en", "")
            if "We use " in en_text and "in the " in en_text and "module." in en_text:
                errors.append(f"Card {cid} contains generic boilerplate sentence: {en_text}")

        # 3. Leak check
        prompt = c.get("practice", {}).get("production_prompt_ru", "")
        word = c.get("display_term", "")
        clean_w = word.replace("()", "").strip()
        if f"({word})" in prompt or (clean_w and f"({clean_w})" in prompt):
            errors.append(f"Card {cid} leaks English term in Russian prompt: {prompt}")

        # 4. Secondary example check
        if len(c.get("examples", [])) > 1:
            cards_with_secondary += 1

    if cards_with_secondary < 50:
        errors.append(f"Insufficient secondary context examples: {cards_with_secondary} < 50")

    return errors


def check_content() -> bool:
    """Read-only check of canonical content and its sync with assets."""
    print("=== EXECUTING READ-ONLY CONTENT CHECK (--check) ===")
    if not CONTENT_CARDS_JSON.exists():
        print(f"Error: Canonical source {CONTENT_CARDS_JSON} not found!", file=sys.stderr)
        return False

    with open(SCHEMA_JSON, "r", encoding="utf-8") as f:
        schema = json.load(f)

    with open(CONTENT_CARDS_JSON, "r", encoding="utf-8") as f:
        cards = json.load(f)

    errors = validate_cards_data(cards, schema)
    if errors:
        print(f"Content check FAILED with {len(errors)} errors:", file=sys.stderr)
        for err in errors[:10]:
            print(f"  - {err}", file=sys.stderr)
        return False

    # Check sync with assets
    if ASSETS_CARDS_V3_JSON.exists():
        with open(ASSETS_CARDS_V3_JSON, "r", encoding="utf-8") as f:
            assets_cards = json.load(f)
        if len(assets_cards) != len(cards):
            print(f"Warning: assets cards_v3.json count ({len(assets_cards)}) != canonical cards ({len(cards)})", file=sys.stderr)
            return False

    print(f"✓ Canonical content ({len(cards)} cards) is valid, template-free, and synchronized!")
    return True


def publish_content(dry_run: bool = False):
    """Validates and publishes canonical content to app assets."""
    print(f"=== PUBLISHING CONTENT {'(DRY RUN)' if dry_run else ''} ===")
    assert CONTENT_CARDS_JSON.exists(), f"{CONTENT_CARDS_JSON} not found"

    with open(SCHEMA_JSON, "r", encoding="utf-8") as f:
        schema = json.load(f)

    with open(CONTENT_CARDS_JSON, "r", encoding="utf-8") as f:
        cards = json.load(f)

    errors = validate_cards_data(cards, schema)
    if errors:
        print(f"Cannot publish: validation failed with {len(errors)} errors:", file=sys.stderr)
        for err in errors[:10]:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print(f"Validated {len(cards)} canonical cards.")
    if dry_run:
        print("Dry run complete: no files written.")
        return

    # Write to assets
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    with open(ASSETS_CARDS_V3_JSON, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)
    print(f"Published to {ASSETS_CARDS_V3_JSON}")

    with open(ASSETS_CARDS_LEGACY_JSON, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)
    print(f"Published to {ASSETS_CARDS_LEGACY_JSON}")

    # Ensure legacy_id_map and lessons are synced
    if LEGACY_ID_MAP_JSON.exists():
        with open(LEGACY_ID_MAP_JSON, "r", encoding="utf-8") as f:
            id_map = json.load(f)
        with open(ASSETS_LEGACY_ID_MAP_JSON, "w", encoding="utf-8") as f:
            json.dump(id_map, f, ensure_ascii=False, indent=2)
        print(f"Published legacy_id_map to {ASSETS_LEGACY_ID_MAP_JSON}")

    if CONTENT_LESSONS_DIR.exists():
        ASSETS_LESSONS_DIR.mkdir(parents=True, exist_ok=True)
        for l_file in CONTENT_LESSONS_DIR.glob("*.json"):
            dest = ASSETS_LESSONS_DIR / l_file.name
            dest.write_text(l_file.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Synchronized micro-lessons to {ASSETS_LESSONS_DIR}")

    print("=== CONTENT PUBLICATION COMPLETED SUCCESSFULLY ===")


def main():
    parser = argparse.ArgumentParser(description="Canonical Content Management for EnglishCards")
    parser.add_argument("--check", action="store_true", help="Perform read-only check of canonical content and assets")
    parser.add_argument("--dry-run", action="store_true", help="Run validation in memory without writing files")
    parser.add_argument("--publish", action="store_true", help="Validate and publish canonical content to assets")

    args = parser.parse_args()

    if args.check:
        success = check_content()
        sys.exit(0 if success else 1)
    elif args.dry_run:
        publish_content(dry_run=True)
    else:
        publish_content(dry_run=False)

if __name__ == "__main__":
    main()
