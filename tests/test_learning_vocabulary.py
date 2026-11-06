import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANKI = "Anki: 480 слов"
DOC = "Чтение документации: 500 слов"


def test_restored_anki_and_documentation_decks():
    cards = json.loads((ROOT / "content/cards.json").read_text(encoding="utf-8"))
    anki = [c for c in cards if ANKI in c.get("study_collections", [])]
    docs = [c for c in cards if DOC in c.get("study_collections", [])]

    assert len(anki) == 480
    assert len(docs) == 500
    assert len({c["display_term"].casefold() for c in docs}) == 500
    assert len({c["card_id"] for c in cards}) == len(cards)
    assert all(c["meaning_ru_short"].strip() for c in anki + docs)
    assert all(c["pronunciation"]["spoken_en"].strip() for c in anki + docs)
    assert all(c["documentation_source_url"].startswith((
        "https://docs.djangoproject.com/en/5.2/", "https://fastapi.tiangolo.com/"
    )) for c in docs)
    assert next(c for c in anki if c["display_term"] == "whether or not")[
        "meaning_ru_short"] == "независимо от того, ... или нет"


def test_anki_examples_have_context_and_complete_andrew_audio():
    cards = json.loads((ROOT / "content/cards.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "content/audio_manifest.json").read_text(encoding="utf-8"))
    audio = {(entry["card_id"], entry["role"]): entry for entry in manifest}
    anki = [card for card in cards if card["card_id"].startswith("anki.vocab.")]
    assert len(anki) == 480
    for card in anki:
        example = card["examples"][0]
        assert example["en"].strip().lower() != card["display_term"].strip().lower()
        assert example["ru"].strip() != card["meaning_ru_short"].strip()
        for role in ("term_en", "meaning_ru", "example_en", "example_ru"):
            entry = audio[(card["card_id"], role)]
            assert entry["voice"] == "en-US-AndrewMultilingualNeural"
            assert (ROOT / "app_english_cards/app/src/main/assets" / entry["file_path"]).is_file()


def test_guided_readings_have_comprehension_checks():
    readings = json.loads((ROOT / "content/readings.json").read_text(encoding="utf-8"))
    assert len(readings) == 10
    assert len({item["id"] for item in readings}) == len(readings)
    for item in readings:
        assert len(item["passage"].split()) >= 65
        assert item["source_url"].startswith((
            "https://docs.djangoproject.com/en/5.2/", "https://fastapi.tiangolo.com/"
        ))
        assert len(item["questions"]) >= 2
        assert all(0 <= q["correct"] < len(q["options_ru"]) for q in item["questions"])
