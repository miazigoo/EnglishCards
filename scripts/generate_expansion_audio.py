#!/usr/bin/env python3
"""
scripts/generate_expansion_audio.py

Generates missing audio segments (term_en, meaning_ru, example_en, example_ru)
and unified fallback audio (audio/word_XXXX.mp3) for the 150 expansion cards (2000-2149).
Voice: en-US-AndrewMultilingualNeural via edge-tts.
"""

import sys
import os
import json
import asyncio
import hashlib
from pathlib import Path
from typing import Dict, Any, List
import edge_tts
from pydub import AudioSegment

BASE_DIR = Path(__file__).resolve().parent.parent
CARDS_JSON = BASE_DIR / "content/cards.json"
MANIFEST_JSON = BASE_DIR / "content/audio_manifest.json"
APP_MANIFEST_JSON = BASE_DIR / "app_english_cards/app/src/main/assets/audio_manifest.json"
SEGMENTS_DIR = BASE_DIR / "app_english_cards/app/src/main/assets/audio/segments"
LEGACY_DIR = BASE_DIR / "app_english_cards/app/src/main/assets/audio"

VOICE = "en-US-AndrewMultilingualNeural"
PROVIDER = "edge-tts"

def compute_input_hash(spoken_text: str, role: str, lang: str, voice: str) -> str:
    canonical = {
        "spoken_text": spoken_text.strip(),
        "role": role,
        "lang": lang,
        "voice": voice,
        "provider": PROVIDER,
        "rate": "+0%",
        "pitch": "+0Hz"
    }
    payload = json.dumps(canonical, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def compute_file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

sem = asyncio.Semaphore(6)

async def synthesize_with_retry(spoken_text: str, out_file: Path) -> tuple[int, str]:
    if out_file.exists() and out_file.stat().st_size > 200:
        try:
            aud = AudioSegment.from_file(str(out_file), format="mp3")
            if len(aud) > 50:
                return len(aud), compute_file_sha256(out_file)
        except Exception:
            pass

    out_file.parent.mkdir(parents=True, exist_ok=True)
    temp_file = out_file.with_suffix(".tmp.mp3")

    for attempt in range(4):
        try:
            async with sem:
                communicate = edge_tts.Communicate(spoken_text, voice=VOICE, rate="+0%", pitch="+0Hz")
                with open(temp_file, "wb") as f:
                    async for chunk in communicate.stream():
                        if chunk["type"] == "audio":
                            f.write(chunk["data"])

            if not temp_file.exists() or temp_file.stat().st_size < 200:
                raise ValueError("Generated file is too small")

            audio = AudioSegment.from_file(str(temp_file), format="mp3")
            duration_ms = len(audio)
            if duration_ms < 50:
                raise ValueError("Decoded duration too short")

            temp_file.replace(out_file)
            return duration_ms, compute_file_sha256(out_file)
        except Exception as e:
            if temp_file.exists():
                temp_file.unlink(missing_ok=True)
            if attempt == 3:
                raise RuntimeError(f"Failed to synthesize '{spoken_text}': {e}")
            await asyncio.sleep(1.0 * (attempt + 1))

    raise RuntimeError(f"Could not synthesize '{spoken_text}'")

async def process_card(card: Dict[str, Any]) -> List[Dict[str, Any]]:
    cid = card["card_id"]
    lid = card["legacy_ids"][0] if card.get("legacy_ids") else None
    display_term = card["display_term"]
    meaning_ru = card["meaning_ru_short"]

    examples = card.get("examples", [])
    ex_en = examples[0]["en"] if examples else ""
    ex_ru = examples[0]["ru"] if examples else ""

    tasks_info = [
        ("term_en", "en", display_term),
        ("meaning_ru", "ru", meaning_ru),
    ]
    if ex_en:
        tasks_info.append(("example_en", "en", ex_en))
    if ex_ru:
        tasks_info.append(("example_ru", "ru", ex_ru))

    entries = []
    generated_files = {}

    for role, lang, text in tasks_info:
        in_hash = compute_input_hash(text, role, lang, VOICE)
        seg_id = f"seg_{in_hash[:16]}"
        file_name = f"{seg_id}.mp3"
        file_path = SEGMENTS_DIR / file_name
        rel_path = f"audio/segments/{file_name}"

        try:
            duration_ms, file_sha256 = await synthesize_with_retry(text, file_path)
            entries.append({
                "segment_id": seg_id,
                "card_id": cid,
                "role": role,
                "lang": lang,
                "spoken_text": text,
                "voice": VOICE,
                "provider": PROVIDER,
                "input_hash": in_hash,
                "file_path": rel_path,
                "file_sha256": file_sha256,
                "duration_ms": duration_ms,
                "validation_status": "ready"
            })
            generated_files[role] = file_path
        except Exception as e:
            print(f"Error synthesizing {cid} {role}: {e}", file=sys.stderr)

    # Generate fallback combined file word_XXXX.mp3 if legacy_id is present
    if lid is not None and "term_en" in generated_files and "meaning_ru" in generated_files:
        legacy_file = LEGACY_DIR / f"word_{lid:04d}.mp3"
        if not legacy_file.exists():
            try:
                term_aud = AudioSegment.from_file(str(generated_files["term_en"]), format="mp3")
                silence = AudioSegment.silent(duration=450)
                mean_aud = AudioSegment.from_file(str(generated_files["meaning_ru"]), format="mp3")
                combined = term_aud + silence + mean_aud
                combined.export(str(legacy_file), format="mp3")
                
                l_hash = f"legacy_{lid:04d}"
                entries.append({
                    "segment_id": f"legacy_{lid:04d}",
                    "card_id": cid,
                    "role": "combined_legacy",
                    "lang": "en+ru",
                    "spoken_text": display_term,
                    "voice": VOICE,
                    "provider": PROVIDER,
                    "input_hash": l_hash,
                    "file_path": f"audio/word_{lid:04d}.mp3",
                    "file_sha256": compute_file_sha256(legacy_file),
                    "duration_ms": len(combined),
                    "validation_status": "ready"
                })
            except Exception as e:
                print(f"Error creating combined fallback for {cid} ({lid}): {e}", file=sys.stderr)

    return entries

async def main():
    SEGMENTS_DIR.mkdir(parents=True, exist_ok=True)
    LEGACY_DIR.mkdir(parents=True, exist_ok=True)

    with open(CARDS_JSON, "r", encoding="utf-8") as f:
        cards = json.load(f)

    # Find cards missing from manifest
    with open(MANIFEST_JSON, "r", encoding="utf-8") as f:
        existing_manifest = json.load(f)

    manifest_cids = {m.get("card_id") for m in existing_manifest}
    target_cards = [c for c in cards if c.get("card_id") not in manifest_cids]
    print(f"Targeting {len(target_cards)} cards without audio in manifest...")

    all_new_entries = []
    batch_size = 15
    for i in range(0, len(target_cards), batch_size):
        batch = target_cards[i:i + batch_size]
        print(f"Processing batch {i+1}-{min(i+batch_size, len(target_cards))} of {len(target_cards)}...")
        results = await asyncio.gather(*(process_card(c) for c in batch))
        for res in results:
            all_new_entries.extend(res)

    print(f"Generated {len(all_new_entries)} new segment and fallback entries.")

    # Combine with existing manifest
    combined_manifest = existing_manifest + all_new_entries

    with open(MANIFEST_JSON, "w", encoding="utf-8") as f:
        json.dump(combined_manifest, f, ensure_ascii=False, indent=2)

    with open(APP_MANIFEST_JSON, "w", encoding="utf-8") as f:
        json.dump(combined_manifest, f, ensure_ascii=False, indent=2)

    print("Successfully updated both content/audio_manifest.json and assets/audio_manifest.json!")

if __name__ == "__main__":
    asyncio.run(main())
