#!/usr/bin/env python3
"""
Generates cards.json and all 480 audio files using Microsoft Andrew Multilingual Neural Voice.
Format: "{Word} — это {Translation}. {Word} — это {Translation}."
Single clear male voice, 2 repetitions with natural pacing.
"""

import asyncio
import json
import os
import re
import sys
import time
from pathlib import Path
import edge_tts

TSV_PATH = Path('/home/b00bs/my_less/English/English_A2_B2_480_FIXED_Anki.tsv')
OUTPUT_DIR = Path('/home/b00bs/my_less/English/app_english_cards/app/src/main/assets')
AUDIO_DIR = OUTPUT_DIR / 'audio'
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

VOICE = 'en-US-AndrewMultilingualNeural'
CONCURRENCY = 10

def clean_for_speech(translation: str) -> str:
    # Remove parenthesized acronyms or explanations e.g. "(BOM)", "(Git)"
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

async def synthesize_one(sem, card, total):
    cid = card['id']
    audio_file = AUDIO_DIR / card['audio']
    if audio_file.exists() and audio_file.stat().st_size > 2000:
        return True

    word = card['word']
    clean_tr = card['clean_translation']
    # 2 clear repetitions:
    # "Word — это перевод. Word — это перевод."
    capitalized_word = word[0].upper() + word[1:] if len(word) > 1 else word.upper()
    text = f"{capitalized_word} — это {clean_tr}. {capitalized_word} — это {clean_tr}."

    for attempt in range(5):
        try:
            async with sem:
                communicate = edge_tts.Communicate(text, VOICE)
                await communicate.save(str(audio_file))
                if audio_file.exists() and audio_file.stat().st_size > 1000:
                    if cid % 20 == 0 or cid == total:
                        print(f"[{cid}/{total}] Synthesized: {word} -> {audio_file.name}")
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

    # Save cards.json
    cards_json_path = OUTPUT_DIR / 'cards.json'
    with open(cards_json_path, 'w', encoding='utf-8') as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)
    print(f"Saved {cards_json_path}")

    # Synthesize audio
    print(f"Starting audio synthesis for {len(cards)} cards using {VOICE} (Concurrency={CONCURRENCY})...")
    sem = asyncio.Semaphore(CONCURRENCY)
    start_time = time.time()
    tasks = [synthesize_one(sem, card, len(cards)) for card in cards]
    results = await asyncio.gather(*tasks)

    succeeded = sum(1 for r in results if r)
    elapsed = time.time() - start_time
    print(f"Synthesis complete! {succeeded}/{len(cards)} files ready in {elapsed:.1f}s.")

if __name__ == '__main__':
    asyncio.run(main())
