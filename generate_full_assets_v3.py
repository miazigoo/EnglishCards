#!/usr/bin/env python3
"""
Скрипт генерации полного пакета ассетов для приложения English Flashcards:
1. Загружает 1529 отобранных IT/Backend/IoT слов из backend_words_selection.json.
2. Генерирует точные IPA транскрипции и русские фонетические подсказки.
3. Выполняет dual-pass синтез через Edge-TTS (en-US-AndrewMultilingualNeural):
   - Чистый изолированный en-US проход для идеального американского произношения.
   - Чистый русский проход для перевода.
   - Склейка через pydub с паузами в формате 2x повторения.
4. Сохраняет аудио в app/src/main/assets/audio/word_XXXX.mp3.
5. Формирует финальный cards.json в app/src/main/assets/cards.json.
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
import eng_to_ipa as ipa

SOURCE_JSON = Path('/home/b00bs/my_less/English/backend_words_selection.json')
ASSETS_DIR = Path('/home/b00bs/my_less/English/app_english_cards/app/src/main/assets')
AUDIO_DIR = ASSETS_DIR / 'audio'
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
CARDS_JSON = ASSETS_DIR / 'cards.json'

VOICE = 'en-US-AndrewMultilingualNeural'
CONCURRENCY = 15

PAUSE_SHORT = AudioSegment.silent(duration=300)   # 300ms между словом и переводом
PAUSE_MED = AudioSegment.silent(duration=700)     # 700ms между повторами

SPECIAL_PRONUNCIATIONS = {
    'strip()': 'Strip.',
    'split()': 'Split.',
    'join()': 'Join.',
    'select_related()': 'Select related.',
    'prefetch_related()': 'Prefetch related.',
    'isinstance()': 'Is instance.',
    'issubclass()': 'Is subclass.',
    'hasattr()': 'Has attr.',
    'getattr()': 'Get attr.',
    'setattr()': 'Set attr.',
    'delattr()': 'Del attr.',
    'Depends()': 'Depends.',
    'BaseModel': 'Base Model.',
    'Field()': 'Field.',
    'HTTPException': 'H T T P Exception.',
    'JSONResponse': 'JSON Response.',
    'StreamingResponse': 'Streaming Response.',
    'FileResponse': 'File Response.',
    'CORSMiddleware': 'CORS Middleware.',
    'OAuth2PasswordBearer': 'OAuth 2 Password Bearer.',
    'OAuth2PasswordRequestForm': 'OAuth 2 Password Request Form.',
    'HTTPBearer': 'H T T P Bearer.',
    'modbus_rtu': 'Modbus R T U.',
    'modbus_tcp': 'Modbus T C P.',
    'gtin': 'G TIN.',
    'data_matrix': 'Data Matrix.',
    'jwt': 'J W T.',
    'api_key': 'A P I Key.',
    'csrf_token': 'C S R F Token.',
    'plc': 'P L C.',
    'hmi_panel': 'H M I Panel.',
    'oee_efficiency': 'O E E Efficiency.',
    'scada': 'SCADA.',
    'opc_ua': 'O P C U A.',
    'sql': 'S Q L.',
    'orm': 'O R M.',
    'iot': 'I o T.',
    'mes': 'M E S.',
    'wms': 'W M S.',
    'erp': 'E R P.'
}

def clean_word_for_en_speech(word: str) -> str:
    if word in SPECIAL_PRONUNCIATIONS:
        return SPECIAL_PRONUNCIATIONS[word]
    w = re.sub(r'\(.*?\)', '', word).strip()
    w = w.replace('_', ' ')
    w = re.sub(r'([a-z])([A-Z])', r'\1 \2', w)
    w = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', w)
    w = re.sub(r'\s+', ' ', w).strip()
    return f"{w[0].upper() + w[1:] if len(w) > 1 else w.upper()}."

def clean_tr_for_ru_speech(clean_tr: str) -> str:
    cleaned = re.sub(r'\(.*?\)', '', clean_tr).strip()
    cleaned = re.sub(r'\s+', ' ', cleaned)
    # Удаляем лишние точки или тире в конце
    cleaned = cleaned.rstrip('.,;:-')
    return f"это {cleaned}."

def ipa_to_ru_transcription(ipa_str: str) -> str:
    s = ipa_str.replace('/', '').replace('*', '').strip()
    replacements = [
        ('ˈ', ''), ('ˌ', ''),
        ('dʒ', 'дж'), ('tʃ', 'ч'), ('ʧ', 'ч'), ('ʤ', 'дж'),
        ('ʃ', 'ш'), ('ʒ', 'ж'), ('θ', 'с'), ('ð', 'з'),
        ('ŋ', 'нг'),
        ('aɪ', 'ай'), ('eɪ', 'эй'), ('ɔɪ', 'ой'), ('aʊ', 'ау'), ('oʊ', 'оу'), ('əʊ', 'оу'),
        ('iː', 'и'), ('uː', 'у'), ('ɔː', 'о'), ('ɑː', 'а'), ('ɜː', 'ер'),
        ('ɪ', 'и'), ('ɛ', 'э'), ('æ', 'э'), ('ʌ', 'а'), ('ə', 'е'),
        ('ʊ', 'у'), ('ɒ', 'о'), ('ɑ', 'а'), ('ɔ', 'о'),
        ('j', 'й'), ('w', 'в'), ('r', 'р'), ('l', 'л'),
        ('m', 'м'), ('n', 'н'), ('p', 'п'), ('b', 'б'),
        ('t', 'т'), ('d', 'д'), ('k', 'к'), ('g', 'г'),
        ('f', 'ф'), ('v', 'в'), ('s', 'с'), ('z', 'з'),
        ('h', 'х')
    ]
    res = s
    for sym, ru in replacements:
        res = res.replace(sym, ru)
    # Коррекция частых сочетаний
    res = res.replace('белк', 'балк').replace('бефер', 'бафер')
    return res

def get_word_transcriptions(word: str):
    clean = re.sub(r'\(.*?\)', '', word).strip()
    clean = clean.replace('_', ' ')
    clean = re.sub(r'([a-z])([A-Z])', r'\1 \2', clean)
    clean = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', clean)
    parts = clean.split()
    
    ipa_parts = []
    ru_parts = []
    for p in parts:
        conv = ipa.convert(p.lower())
        if conv.endswith('*'):
            conv = conv[:-1]
        ipa_parts.append(conv)
        ru_parts.append(ipa_to_ru_transcription(conv))
        
    full_ipa = '/' + ' '.join(ipa_parts) + '/'
    full_ru = ' '.join(ru_parts)
    return full_ipa, full_ru

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

    # Если файл уже существует и нормального размера (> 5KB) — пропускаем
    if audio_file.exists() and audio_file.stat().st_size > 5000:
        return True

    en_text = clean_word_for_en_speech(word)
    ru_text = clean_tr_for_ru_speech(clean_tr)

    for attempt in range(5):
        try:
            async with sem:
                # 1. English pass
                c_en = edge_tts.Communicate(en_text, VOICE)
                en_bytes = await get_audio_bytes(c_en)
                if not en_bytes or len(en_bytes) < 400:
                    raise ValueError(f"Empty EN audio for {word}")

                # 2. Russian pass
                c_ru = edge_tts.Communicate(ru_text, VOICE)
                ru_bytes = await get_audio_bytes(c_ru)
                if not ru_bytes or len(ru_bytes) < 400:
                    raise ValueError(f"Empty RU audio for {clean_tr}")

                # 3. Stitch with pydub (EN -> RU -> EN -> RU)
                s_en = AudioSegment.from_file(io.BytesIO(en_bytes), format="mp3")
                s_ru = AudioSegment.from_file(io.BytesIO(ru_bytes), format="mp3")

                combined = s_en + PAUSE_SHORT + s_ru + PAUSE_MED + s_en + PAUSE_SHORT + s_ru
                combined.export(str(audio_file), format="mp3", bitrate="48k")

                if audio_file.exists() and audio_file.stat().st_size > 3000:
                    if cid % 25 == 0 or cid == total or cid <= 5:
                        print(f"[{cid:04d}/{total:04d}] Готово: '{word}' -> '{clean_tr}' ({audio_file.stat().st_size:,} байт)")
                    return True
        except Exception as e:
            if attempt == 4:
                print(f"❌ Ошибка синтеза карточки #{cid} ({word}): {e}", file=sys.stderr)
            await asyncio.sleep(1.0 + attempt * 1.5)
    return False

async def main():
    print(f"Загрузка базы слов из {SOURCE_JSON}...")
    with open(SOURCE_JSON, 'r', encoding='utf-8') as f:
        raw_items = json.load(f)
    print(f"Загружено {len(raw_items)} слов.")

    # Удаляем старые 3-значные файлы word_XXX.mp3 (word_001.mp3 - word_480.mp3), чтобы не засорять проект
    old_files = list(AUDIO_DIR.glob('word_[0-9][0-9][0-9].mp3'))
    if old_files:
        print(f"Удаление {len(old_files)} старых файлов предыдущей колоды...")
        for of in old_files:
            try:
                of.unlink()
            except Exception:
                pass

    cards = []
    print("Генерация IPA транскрипций и русских фонетических подсказок...")
    for item in raw_items:
        cid = item['id']
        word = item['word']
        clean_tr = item['cleanTranslation']
        full_desc = item['translation']
        category = item['category']
        audio_name = f"word_{cid:04d}.mp3"

        ipa_trans, ru_hint = get_word_transcriptions(word)

        cards.append({
            "id": cid,
            "word": word,
            "translation": full_desc,
            "clean_translation": clean_tr,
            "ipa": ipa_trans,
            "transcription_ru": ru_hint,
            "category": category,
            "audio": audio_name
        })

    # Сохраняем cards.json сразу в assets
    print(f"Сохранение cards.json ({len(cards)} карточек)...")
    with open(CARDS_JSON, 'w', encoding='utf-8') as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)

    total = len(cards)
    print(f"Старт параллельного dual-pass синтеза аудио для {total} карточек (concurrency={CONCURRENCY})...")
    start_time = time.time()
    sem = asyncio.Semaphore(CONCURRENCY)

    tasks = [synthesize_card(sem, card, total) for card in cards]
    results = await asyncio.gather(*tasks)

    succeeded = sum(1 for r in results if r)
    elapsed = time.time() - start_time
    print(f"---")
    print(f"Синтез завершен! Успешно создано: {succeeded}/{total} аудиофайлов за {elapsed:.1f} сек.")
    print(f"Все файлы размещены в {AUDIO_DIR}")

if __name__ == '__main__':
    asyncio.run(main())
