#!/usr/bin/env python3
"""
scripts/audit_content.py

Audits the baseline cards.json dataset (1529 cards) against the quality criteria
specified in GEMINI_TECH_SPEC_ENGLISH_V3.md.
Produces reports/content_audit.json and reports/content_audit.md.
"""

import json
import re
import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_JSON = BASE_DIR / "app_english_cards/app/src/main/assets/cards.json"
REPORT_JSON = BASE_DIR / "reports/content_audit.json"
REPORT_MD = BASE_DIR / "reports/content_audit.md"

def contains_latin_in_cyrillic(text: str) -> bool:
    """Checks if a string primarily in Russian/Cyrillic contains unexpected Latin characters."""
    if not text:
        return False
    # Check for mixed script characters common in OCR/bad generation
    latin_chars = set(re.findall(r'[a-zA-Z]', text))
    cyrillic_chars = set(re.findall(r'[а-яА-ЯёЁ]', text))
    return bool(latin_chars and cyrillic_chars)

def check_python_code(code_str: str) -> tuple[bool, str]:
    """Validates Python syntax and checks for known anti-patterns."""
    if not code_str or not code_str.strip():
        return False, "Empty code snippet"
    try:
        tree = ast.parse(code_str)
        # Check for getattr keyword default
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = getattr(node.func, "id", None)
                if func == "getattr":
                    for kw in node.keywords:
                        if kw.arg == "default":
                            return False, "getattr() uses illegal keyword argument 'default='"
        return True, "Valid syntax"
    except SyntaxError as e:
        return False, f"SyntaxError: {e.msg}"

def run_audit():
    print(f"Loading {SOURCE_JSON}...")
    with open(SOURCE_JSON, "r", encoding="utf-8") as f:
        cards = json.load(f)

    total_cards = len(cards)
    print(f"Total cards loaded: {total_cards}")

    audit_records = []
    template_notes_count = 0
    mixed_transcription_count = 0
    bogus_ipa_count = 0
    code_issues_count = 0

    for card in cards:
        cid = card["id"]
        word = card.get("word", "")
        translation = card.get("translation", "")
        clean_tr = card.get("clean_translation", "")
        example = card.get("example", "")
        example_note = card.get("example_note", "")
        ipa = card.get("ipa", "")
        trans_ru = card.get("transcription_ru", "")
        category = card.get("category", "")

        issues = []
        action = "keep"

        # 1. Template check
        is_template = "ключевую сущность или архитектурный паттерн" in example_note
        if is_template:
            template_notes_count += 1
            issues.append("template_example_note")
            action = "fix"

        # 2. Transcription checks
        if contains_latin_in_cyrillic(trans_ru):
            mixed_transcription_count += 1
            issues.append(f"mixed_script_ru_transcription: '{trans_ru}'")
            action = "fix"

        # 3. IPA checks
        if ipa == f"/{word.replace('()', '')}/" or (len(word) > 4 and ipa.strip("/").lower() == word.lower().replace("()", "")):
            bogus_ipa_count += 1
            issues.append(f"bogus_literal_ipa: '{ipa}'")
            action = "fix"

        # 4. Code checks
        is_valid_code, code_msg = check_python_code(example)
        if not is_valid_code and "django" not in example.lower() and "select" not in example.lower():
            code_issues_count += 1
            issues.append(f"code_issue: {code_msg}")
            action = "fix"

        # 5. Benchmark cards checks
        if word == "rsplit()":
            issues.append("rsplit_needs_pedagogical_breakdown_and_comparison")
            action = "fix"
        elif word == "zip()":
            issues.append("zip_needs_positional_pairing_explanation")
            action = "fix"
        elif word == "issubclass()":
            issues.append("issubclass_needs_animal_dog_inheritance_example")
            action = "fix"
        elif word == "getattr()":
            issues.append("getattr_has_keyword_arg_error")
            action = "fix"
        elif word == "filter()":
            issues.append("filter_needs_builtin_vs_queryset_separation")
            action = "split"

        audit_records.append({
            "legacy_id": cid,
            "word": word,
            "category": category,
            "action": action,
            "issues": issues,
            "clean_translation": clean_tr,
            "ipa": ipa,
            "transcription_ru": trans_ru
        })

    # Summary
    summary = {
        "total_cards_audited": total_cards,
        "cards_with_template_notes": template_notes_count,
        "cards_with_mixed_script_transcription": mixed_transcription_count,
        "cards_with_bogus_ipa": bogus_ipa_count,
        "cards_with_code_syntax_issues": code_issues_count,
        "cards_requiring_fix": sum(1 for r in audit_records if r["action"] in ("fix", "split")),
        "cards_intact": sum(1 for r in audit_records if r["action"] == "keep")
    }

    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "records": audit_records}, f, ensure_ascii=False, indent=2)

    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write("# Отчет аудита контента baseline cards.json (1529 карточек)\n\n")
        f.write(f"- **Всего карточек проверено:** {total_cards}\n")
        f.write(f"- **Карточек с шаблонными заметками («ключевая сущность / паттерн»):** {template_notes_count} ({template_notes_count/total_cards*100:.1f}%)\n")
        f.write(f"- **Карточек со смешанной латиницей/кириллицей в транскрипции:** {mixed_transcription_count}\n")
        f.write(f"- **Карточек с фиктивной IPA транскрипцией:** {bogus_ipa_count}\n")
        f.write(f"- **Карточек с ошибками в коде:** {code_issues_count}\n")
        f.write(f"- **Требуют исправления/обогащения:** {summary['cards_requiring_fix']}\n\n")
        f.write("## Ключевые дефекты эталонных карточек\n\n")
        f.write("1. **`rsplit()` (ID 45):** содержит `RsplitService` и псевдо-IPA `/rsplit/`. Требует разбора `right + split` («разделить справа»), сравнения с `split()` и сохранения порядка результата слева направо.\n")
        f.write("2. **`zip()` (ID 1):** переводится только как «сшивает итераторы». Требует ясного объяснения попарного объединения по позициям и примера с именами и оценками.\n")
        f.write("3. **`issubclass()` (ID 4):** содержит `IssubclassService`. Требует реальных классов `Animal`/`Dog` и проверки наследования.\n")
        f.write("4. **`getattr()` (ID 6):** содержит вызов `getattr(order, field_name, default=0.0)` с запрещенным именованным аргументом. Требует позиционного аргумента `getattr(order, 'total_weight', 0.0)`.\n")
        f.write("5. **`filter()` (ID 17):** смешивает `python.builtins.filter` и `QuerySet.filter`. Требует разделения на две самостоятельные единицы.\n\n")
        f.write("## Пример записей с замечаниями\n\n")
        f.write("| ID | Термин | Категория | Действие | Замечания |\n")
        f.write("| :---: | :--- | :--- | :---: | :--- |\n")
        for r in audit_records[:30]:
            if r["issues"]:
                f.write(f"| {r['legacy_id']} | `{r['word']}` | {r['category']} | **{r['action']}** | {', '.join(r['issues'])} |\n")

    print(f"Audit report saved to {REPORT_JSON} and {REPORT_MD}")

if __name__ == "__main__":
    run_audit()
