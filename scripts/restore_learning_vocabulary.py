#!/usr/bin/env python3
"""Restore the 480 Anki entries and a deduplicated documentation reading deck.

Run after fetch_english_docs_corpus.py. Re-running is idempotent.
"""
import collections
import csv
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "content/cards.json"
TSV = ROOT / "English_A2_B2_480_FIXED_Anki.tsv"
CORPUS = ROOT / "content/documentation_word_frequencies.json"
CONTEXTS = ROOT / "content/anki_contexts.json"
ANKI_DECK = "Anki: 480 слов"
DOC_DECK = "Чтение документации: 500 слов"

# These words appear in prose but the existing technical entry describes a
# different sense (or a proper name). They must not become reading cards.
EXCLUDE = {"can", "fastapi", "get", "put", "having", "none", "any", "true",
           "false", "current", "parameters", "fileresponse", "congratulations",
           "dict", "int", "str", "list", "tuple", "bool", "set", "copy",
           "has", "does", "did", "was", "were", "is", "are", "be"}
TRANSLATION_FIX = {
    "whether or not": "независимо от того, ... или нет",
    "application": "приложение; заявление",
    "batch": "пакет, партия",
    "capacity": "ёмкость, производственная мощность",
    "consumption": "потребление, расход",
    "feature": "функция, возможность продукта",
    "fine": "хорошо; штраф",
    "log": "журнал, запись журнала",
    "performance": "производительность, результативность",
    "reference": "ссылка; рекомендация",
    "release": "выпуск версии, релиз; освобождать",
    "route": "маршрут, путь",
    "tag": "тег, метка",
    "traffic": "трафик, дорожное движение",
    "yield": "выдавать значение; выход годной продукции",
}

DOCUMENTATION_TRANSLATION_FIX = {
    "data": "данные", "view": "представление, вид", "setting": "настройка",
    "time": "время", "text": "текст", "help": "помощь, справка",
    "state": "состояние", "model": "модель", "explanation": "объяснение",
    "lead": "вести; приводить", "except": "кроме", "publish": "публиковать",
    "zero": "ноль; обнулять", "line": "строка, линия", "handling": "обработка",
    "version": "версия", "source": "источник", "value": "значение",
    "order": "порядок; заказ", "number": "число, номер",
    "operation": "операция", "level": "уровень", "step": "шаг",
    "flow": "поток", "frame": "кадр; рамка", "header": "заголовок",
    "status": "состояние, статус", "key": "ключ", "test": "тест; проверять",
    "result": "результат", "action": "действие", "total": "общий; итог",
    "code": "код", "error": "ошибка", "info": "информация",
}


def anki_rows():
    for row in csv.reader(TSV.open(encoding="utf-8"), delimiter="\t"):
        if not row or row[0].startswith("#"):
            continue
        term = row[0].strip()
        divs = BeautifulSoup(row[1], "html.parser").find_all("div")
        meaning = TRANSLATION_FIX.get(term.lower(), divs[0].get_text(" ", strip=True))
        topic = divs[-1].get_text(" ", strip=True)
        yield term, meaning, topic


def main():
    cards = json.loads(CARDS.read_text(encoding="utf-8"))
    docs = json.loads(CORPUS.read_text(encoding="utf-8"))
    freq = collections.Counter()
    origins = collections.defaultdict(list)
    for url, data in docs.items():
        for term, count in data["frequencies"].items():
            freq[term] += count
            origins[term].append(url)

    original = list(anki_rows())
    contexts = json.loads(CONTEXTS.read_text(encoding="utf-8")) if CONTEXTS.exists() else {}
    assert len(original) == 480 and len({x[0].lower() for x in original}) == 480
    cards = [c for c in cards if not c["card_id"].startswith("anki.vocab.")]
    for card in cards:
        if DOC_DECK in card.get("study_collections", []):
            card["study_collections"] = [
                name for name in card["study_collections"] if name != DOC_DECK
            ]
            card.pop("documentation_source_url", None)
            card.pop("documentation_frequency", None)
    next_id = max((lid for c in cards for lid in c.get("legacy_ids", [])), default=0) + 1
    anki_by_term = {}
    for term, meaning, topic in original:
        key = term.lower()
        cid = f"anki.vocab.{len(anki_by_term)+1:03d}"
        context = contexts.get(cid)
        card = {
            "schema_version": 3, "card_id": cid, "legacy_ids": [next_id],
            "content_revision": 1, "lexeme_id": "en." + re.sub(r"[^a-z0-9]+", ".", key).strip("."),
            "display_term": term, "namespace": None,
            "entry_type": "workplace_phrase" if " " in term else "general_word",
            "part_of_speech": None, "language_level": None, "technical_level": None,
            "priority": "core_english", "tags": ["anki", topic],
            "study_collections": [ANKI_DECK],
            "meaning_ru_short": meaning,
            "explanation_ru": f"Исходный словарь Anki: {topic}. Учите английское слово и русский смысл.",
            "name_breakdown": None,
            "pronunciation": {"spoken_en": term, "ipa": None, "ru_hint": None,
                              "verification": "audio_andrew"},
            # Original TSV has no example sentences. A word-pair is displayed
            # instead of inventing an unreviewed or grammatically wrong sentence.
            "examples": [{"example_id": "context" if context else "word_pair",
                          "en": context["en"] if context else term,
                          "ru": context["ru"] if context else meaning,
                          **({"source_url": context["source_url"]} if context and context.get("source_url") else {})}],
            "practice": {"enabled_templates": ["en_to_ru", "ru_to_en", "listening", "spelling"] + (["cloze"] if context else []),
                         "production_prompt_ru": meaning, "accepted_answers": [term],
                         "cloze": {"example_id": "context", "target": term}
                         if context and re.search(r"(?<![A-Za-z])" + re.escape(term) + r"(?![A-Za-z])", context["en"], re.I)
                         else None},
            "technical": None,
            "qa": {"qa_status": "ready", "review_level": "model_reviewed" if context and context.get("editorial") else "automated",
                   "reviewed_at": "2026-11-03T00:00:00Z", "issues": []},
        }
        next_id += 1
        cards.append(card)
        anki_by_term[key] = card

    existing = {}
    for c in cards:
        key = c["display_term"].lower()
        if re.fullmatch(r"[a-z]+", key) and key not in anki_by_term:
            existing.setdefault(key, c)

    candidates = sorted(((anki_by_term.keys() | existing.keys()) & freq.keys()) - EXCLUDE,
                        key=lambda term: (-freq[term], term))
    assert len(candidates) >= 500, f"Only {len(candidates)} documentation words"
    selected = candidates[:500]
    for term in selected:
        card = anki_by_term.get(term) or existing[term]
        if term in DOCUMENTATION_TRANSLATION_FIX and term not in anki_by_term:
            card["meaning_ru_short"] = DOCUMENTATION_TRANSLATION_FIX[term]
            card["practice"]["production_prompt_ru"] = card["meaning_ru_short"]
        collections_ = card.setdefault("study_collections", [])
        if DOC_DECK not in collections_:
            collections_.append(DOC_DECK)
        card["documentation_source_url"] = origins[term][0]
        card["documentation_frequency"] = freq[term]

    assert len({x.lower() for x in selected}) == 500
    CARDS.write_text(json.dumps(cards, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = {"sources": len(docs), "original_anki": 480, "documentation_words": 500,
              "documentation_anki_overlap": sum(x in anki_by_term for x in selected),
              "documentation_words_list": selected,
              "translation_corrections": TRANSLATION_FIX}
    (ROOT / "content/vocabulary_restore_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(report | {"documentation_words_list": "[500 terms]"})


if __name__ == "__main__":
    main()
