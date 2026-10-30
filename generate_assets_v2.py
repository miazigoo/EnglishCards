#!/usr/bin/env python3
"""
Dual-pass Native Audio Generator:
Synthesizes English words in pure en-US mode (eliminating Russian transliteration artifacts like 'буг' instead of 'баг'),
synthesizes Russian translations in pure Russian mode,
and stitches them cleanly with pydub into a 2x repetition format.
"""

import asyncio
import io
import json
import os
import re
import sys
import time
from pathlib import Path
import edge_tts
from pydub import AudioSegment

TSV_PATH = Path('/home/b00bs/my_less/English/English_A2_B2_480_FIXED_Anki.tsv')
OUTPUT_DIR = Path('/home/b00bs/my_less/English/app_english_cards/app/src/main/assets')
AUDIO_DIR = OUTPUT_DIR / 'audio'
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

VOICE = 'en-US-AndrewMultilingualNeural'
CONCURRENCY = 10

PAUSE_SHORT = AudioSegment.silent(duration=300)   # 300ms pause between word and translation
PAUSE_MED = AudioSegment.silent(duration=700)     # 700ms pause between repetitions

def clean_for_speech(translation: str) -> str:
    cleaned = re.sub(r'\(.*?\)', '', translation).strip()
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned

def parse_tsv():
    cards = []
    with open(TSV_PATH, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('\t')
            if len(parts) < 2:
                continue
            front = parts[0].strip()
            back = parts[1].strip()
            divs = re.findall(r'<div[^>]*>(.*?)</div>', back)
            if len(divs) < 4:
                continue
            translation = divs[0].strip()
            ipa = divs[1].replace('🔊', '').strip()
            ru_hint = divs[2].replace('Примерно:', '').strip()
            category = divs[3].strip()

            clean_tr = clean_for_speech(translation)
            card_id = len(cards) + 1
            audio_filename = f'word_{card_id:03d}.mp3'

            cards.append({
                'id': card_id,
                'word': front,
                'translation': translation,
                'clean_translation': clean_tr,
                'ipa': ipa,
                'transcription_ru': ru_hint,
                'category': category,
                'audio': audio_filename
            })
    return cards

async def get_audio_bytes(communicate):
    buf = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buf.write(chunk["data"])
    buf.seek(0)
    return buf.getvalue()

async def synthesize_card(sem, card, total):
    cid = card['id']
    audio_file = AUDIO_DIR / card['audio']
    word = card['word']
    clean_tr = card['clean_translation']

    # Capitalized pure English word (dot forces proper declarative intonation)
    en_text = f"{word[0].upper() + word[1:] if len(word) > 1 else word.upper()}."
    ru_text = f"это {clean_tr}."

    for attempt in range(5):
        try:
            async with sem:
                # 1. English pass
                c_en = edge_tts.Communicate(en_text, VOICE)
                en_bytes = await get_audio_bytes(c_en)
                if not en_bytes or len(en_bytes) < 500:
                    raise ValueError(f"Empty EN audio for {word}")

                # 2. Russian pass
                c_ru = edge_tts.Communicate(ru_text, VOICE)
                ru_bytes = await get_audio_bytes(c_ru)
                if not ru_bytes or len(ru_bytes) < 500:
                    raise ValueError(f"Empty RU audio for {word}")

                # 3. Stitch with pydub
                s_en = AudioSegment.from_file(io.BytesIO(en_bytes), format="mp3")
                s_ru = AudioSegment.from_file(io.BytesIO(ru_bytes), format="mp3")

                # Format: [Word] -> [это перевод] -> [Word] -> [это перевод]
                combined = s_en + PAUSE_SHORT + s_ru + PAUSE_MED + s_en + PAUSE_SHORT + s_ru

                # Export to final mp3
                combined.export(str(audio_file), format="mp3", bitrate="48k")

                if audio_file.exists() and audio_file.stat().st_size > 2000:
                    if cid % 20 == 0 or cid == total:
                        print(f"[{cid}/{total}] Native pronunciation generated: '{word}' -> {audio_file.name}")
                    return True
        except Exception as e:
            if attempt == 4:
                print(f"FAILED card {cid} ({word}): {e}", file=sys.stderr)
            await asyncio.sleep(1.0 + attempt * 1.5)
    return False

async def main():
    print("Parsing TSV...")
    cards = parse_tsv()
    print(f"Parsed {len(cards)} cards.")

    print(f"Starting dual-pass synthesis for {len(cards)} cards...")
    sem = asyncio.Semaphore(CONCURRENCY)
    start_time = time.time()
    tasks = [synthesize_card(sem, card, len(cards)) for card in cards]
    results = await asyncio.gather(*tasks)

    succeeded = sum(1 for r in results if r)
    elapsed = time.time() - start_time
    print(f"Generation complete! {succeeded}/{len(cards)} files ready in {elapsed:.1f}s.")

if __name__ == '__main__':
    asyncio.run(main())
