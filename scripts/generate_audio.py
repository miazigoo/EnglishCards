#!/usr/bin/env python3
"""
scripts/generate_audio.py

Reproducible speech synthesis pipeline conforming to Sections 9 & 10 of GEMINI_TECH_SPEC_ENGLISH_V3.md.
Generates single-segment speech files using en-US-AndrewMultilingualNeural with managed retries,
backoff, rate limiting, and volume normalization.
Maintains input hashes (SHA-256) and produces content/audio_manifest.json.
"""

import asyncio
import hashlib
import io
import json
from pathlib import Path
from typing import Dict, Any, List
import edge_tts
from pydub import AudioSegment

BASE_DIR = Path(__file__).resolve().parent.parent
CARDS_JSON = BASE_DIR / "content/cards.json"
MANIFEST_JSON = BASE_DIR / "content/audio_manifest.json"
SEGMENTS_DIR = BASE_DIR / "app_english_cards/app/src/main/assets/audio/segments"
LEGACY_AUDIO_DIR = BASE_DIR / "app_english_cards/app/src/main/assets/audio"

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

def compute_file_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

async def synthesize_segment(spoken_text: str, out_file: Path) -> tuple[int, str]:
    """Synthesizes text using Edge-TTS with managed retries and backoff."""
    last_err = None
    for attempt in range(4):
        try:
            c = edge_tts.Communicate(spoken_text, VOICE)
            buf = io.BytesIO()
            async for chunk in c.stream():
                if chunk["type"] == "audio":
                    buf.write(chunk["data"])
            buf.seek(0)
            data = buf.getvalue()
            if data and len(data) >= 200:
                # Normalize peak with pydub to -1.0 dBFS
                audio = AudioSegment.from_file(io.BytesIO(data), format="mp3")
                if audio.max_dBFS > -100:
                    change_in_dBFS = -1.0 - audio.max_dBFS
                    normalized = audio.apply_gain(change_in_dBFS)
                else:
                    normalized = audio

                out_file.parent.mkdir(parents=True, exist_ok=True)
                temp_file = out_file.with_suffix(".tmp.mp3")
                normalized.export(str(temp_file), format="mp3", bitrate="64k")
                temp_file.replace(out_file)

                file_hash = compute_file_sha256(out_file)
                duration_ms = len(normalized)
                return duration_ms, file_hash
        except Exception as e:
            last_err = e
            wait_sec = (attempt + 1) * 1.5
            await asyncio.sleep(wait_sec)
    
    raise RuntimeError(f"Failed to synthesize '{spoken_text}' after 4 attempts: {last_err}")

async def run_pipeline(pilot_limit: int = 26):
    print("=== STARTING AUDIO SYNTHESIS PIPELINE ===")
    SEGMENTS_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(CARDS_JSON, "r", encoding="utf-8") as f:
        cards = json.load(f)

    manifest_entries: List[Dict[str, Any]] = []
    existing_manifest = {}
    if MANIFEST_JSON.exists():
        with open(MANIFEST_JSON, "r", encoding="utf-8") as f:
            for entry in json.load(f):
                existing_manifest[entry["input_hash"]] = entry

    # Priority pilot set
    benchmark_ids = [
        "python.str.rsplit.directional",
        "python.builtins.zip",
        "python.builtins.issubclass",
        "python.builtins.getattr",
        "python.builtins.filter",
        "django.queryset.filter"
    ]
    
    pilot_cards = []
    for c in cards:
        if c["card_id"] in benchmark_ids:
            pilot_cards.append(c)
    for c in cards:
        if len(pilot_cards) >= pilot_limit:
            break
        if c not in pilot_cards:
            pilot_cards.append(c)

    print(f"Synthesizing pilot audio batch for {len(pilot_cards)} cards...")
    
    for idx, card in enumerate(pilot_cards, 1):
        cid = card["card_id"]
        spoken_en = card["pronunciation"].get("spoken_en") or card["display_term"].replace("()", "")
        meaning_ru = card["meaning_ru_short"]
        ex_en = card["examples"][0]["en"] if card.get("examples") else ""
        ex_ru = card["examples"][0]["ru"] if card.get("examples") else ""

        segments_to_gen = [
            ("term_en", "en", spoken_en),
            ("meaning_ru", "ru", meaning_ru),
        ]
        if ex_en:
            segments_to_gen.append(("example_en", "en", ex_en))
        if ex_ru:
            segments_to_gen.append(("example_ru", "ru", ex_ru))

        print(f"[{idx}/{len(pilot_cards)}] Processing card {cid} ({spoken_en})...")

        for role, lang, text in segments_to_gen:
            in_hash = compute_input_hash(text, role, lang, VOICE)
            seg_id = f"seg_{in_hash[:16]}"
            file_name = f"{seg_id}.mp3"
            file_path = SEGMENTS_DIR / file_name
            rel_path = f"audio/segments/{file_name}"

            if in_hash in existing_manifest and file_path.exists() and file_path.stat().st_size > 500:
                manifest_entries.append(existing_manifest[in_hash])
                print(f"   ✓ Cached {role} ({file_name})")
                continue

            try:
                duration_ms, file_sha256 = await synthesize_segment(text, file_path)
                entry = {
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
                }
                manifest_entries.append(entry)
                existing_manifest[in_hash] = entry
                print(f"   ✓ Generated {role} ({duration_ms}ms, {file_name})")
                await asyncio.sleep(0.5)  # respectful pause to avoid websocket rate limits
            except Exception as e:
                print(f"   ✗ Error synthesizing {role} for {cid}: {e}")

    # Map legacy audio files
    for card in cards:
        if card.get("legacy_ids"):
            lid = card["legacy_ids"][0]
            legacy_file = LEGACY_AUDIO_DIR / f"word_{lid:04d}.mp3"
            if legacy_file.exists():
                entry = {
                    "segment_id": f"legacy_{lid:04d}",
                    "card_id": card["card_id"],
                    "role": "combined_legacy",
                    "lang": "en+ru",
                    "spoken_text": card["display_term"],
                    "voice": VOICE,
                    "provider": "edge-tts",
                    "input_hash": f"legacy_{lid:04d}",
                    "file_path": f"audio/word_{lid:04d}.mp3",
                    "file_sha256": compute_file_sha256(legacy_file),
                    "duration_ms": 3000,
                    "validation_status": "legacy_compatible"
                }
                manifest_entries.append(entry)

    MANIFEST_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST_JSON, "w", encoding="utf-8") as f:
        json.dump(manifest_entries, f, ensure_ascii=False, indent=2)

    app_manifest = BASE_DIR / "app_english_cards/app/src/main/assets/audio_manifest.json"
    with open(app_manifest, "w", encoding="utf-8") as f:
        json.dump(manifest_entries, f, ensure_ascii=False, indent=2)

    print(f"Successfully wrote manifest with {len(manifest_entries)} segments to {MANIFEST_JSON}")
    print("=== AUDIO PIPELINE COMPLETED ===")

if __name__ == "__main__":
    asyncio.run(run_pipeline(pilot_limit=26))
