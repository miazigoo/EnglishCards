#!/usr/bin/env python3
"""
Vocabulary Song Generator:
Generates melodic learning songs with rhythmic English-Russian repetition,
background music, dual-voice alternating vocals (Ava & Andrew),
studio loudness mastering, ID3 tags, and LRC synchronized lyrics.
"""

import os
import re
import sys
import time
import asyncio
import subprocess
from pathlib import Path
from pydub import AudioSegment
import edge_tts
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

BASE_DIR = Path('/home/b00bs/my_less/English')
TSV_PATH = BASE_DIR / 'English_A2_B2_480_FIXED_Anki.tsv'
OUT_DIR = BASE_DIR / 'English_Audio_Songs'
CACHE_DIR = BASE_DIR / 'cache_audio'
BG_DIR = BASE_DIR / 'bg_music'

OUT_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

BG_TRACKS = [
    BG_DIR / 'daily_beetle.mp3',   # Track A: Acoustic guitar
    BG_DIR / 'Bossa_Antigua.mp3',   # Track B: Bossa nova jazz
    BG_DIR / 'Carefree.mp3',       # Track C: Sunny ukulele
]

VOICE_FEMALE = 'en-US-AvaMultilingualNeural'
VOICE_MALE = 'en-US-AndrewMultilingualNeural'

def clean_translation(t: str) -> str:
    # Remove HTML tags if any
    t = re.sub(r'<[^>]+>', '', t)
    # Remove parenthesized clarifications for smooth spoken rhythm
    t = re.sub(r'\s*\([^)]*\)', '', t)
    # Clean whitespace
    return t.strip()

def parse_tsv():
    cards = []
    with open(TSV_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip() or line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 2:
                continue
            word = parts[0].strip()
            divs = re.findall(r'<div[^>]*>(.*?)</div>', parts[1])
            if len(divs) >= 4:
                trans = clean_translation(divs[0])
                cat = divs[3].strip()
                cards.append((word, trans, cat))
    return cards

def group_by_category(cards):
    groups = []
    curr_cat = None
    curr_words = []
    for w, t, c in cards:
        if c != curr_cat:
            if curr_cat is not None:
                groups.append((curr_cat, curr_words))
            curr_cat = c
            curr_words = []
        curr_words.append((w, t))
    if curr_cat is not None:
        groups.append((curr_cat, curr_words))
    return groups

async def synth_chunk(text: str, voice: str, out_path: Path, retries=4):
    if out_path.exists() and out_path.stat().st_size > 5000:
        return
    for attempt in range(retries):
        try:
            comm = edge_tts.Communicate(text, voice, rate='+5%')
            await comm.save(str(out_path))
            if out_path.exists() and out_path.stat().st_size > 5000:
                return
        except Exception as e:
            print(f'Retry {attempt+1} for {out_path.name} due to: {e}')
            await asyncio.sleep(2 * (attempt + 1))
    raise RuntimeError(f'Failed to synthesize {out_path.name} after {retries} attempts')

async def generate_category_audio(cat_idx: int, cat_name: str, words: list, sem: asyncio.Semaphore):
    # Group words into verses of 8 words
    VERSE_SIZE = 8
    verses = [words[i:i + VERSE_SIZE] for i in range(0, len(words), VERSE_SIZE)]
    
    cat_cache = CACHE_DIR / f'cat_{cat_idx:02d}'
    cat_cache.mkdir(exist_ok=True)
    
    # 1. Intro
    intro_path = cat_cache / 'intro.mp3'
    intro_text = f'Категория номер {cat_idx}: {cat_name}. Слушаем, поём и учим!'
    async with sem:
        await synth_chunk(intro_text, VOICE_FEMALE if cat_idx % 2 == 1 else VOICE_MALE, intro_path)
    
    # 2. Verses
    verse_files = []
    for v_idx, verse_words in enumerate(verses):
        v_path = cat_cache / f'verse_{v_idx:02d}.mp3'
        voice = VOICE_FEMALE if v_idx % 2 == 0 else VOICE_MALE
        lines = [f'{w} — это {t}. А {w} — это {t}.' for w, t in verse_words]
        v_text = '\n'.join(lines)
        async with sem:
            await synth_chunk(v_text, voice, v_path)
        verse_files.append((v_path, verse_words))
        
    # 3. Outro
    outro_path = cat_cache / 'outro.mp3'
    outro_text = f'Великолепно! Тема {cat_name} успешно пройдена!'
    async with sem:
        await synth_chunk(outro_text, VOICE_MALE if cat_idx % 2 == 1 else VOICE_FEMALE, outro_path)
        
    return intro_path, verse_files, outro_path

def build_category_song(cat_idx: int, cat_name: str, intro_path: Path, verse_files: list, outro_path: Path):
    safe_name = re.sub(r'[\s/]+', '_', cat_name)
    mp3_filename = f'{cat_idx:02d}_{safe_name}.mp3'
    lrc_filename = f'{cat_idx:02d}_{safe_name}.lrc'
    out_mp3 = OUT_DIR / mp3_filename
    out_lrc = OUT_DIR / lrc_filename
    
    print(f'=== Assembling Track {cat_idx}: {cat_name} ===')
    
    # Select background music (cyclical)
    bg_file = BG_TRACKS[(cat_idx - 1) % len(BG_TRACKS)]
    
    # Stitch vocals with precise rhythmic padding
    # Musical intro: 2.0s silence before vocals
    vocal_track = AudioSegment.silent(duration=2000)
    
    lrc_lines = []
    def add_lrc(ms, text):
        mins = int(ms // 60000)
        secs = int((ms % 60000) // 1000)
        cents = int((ms % 1000) // 10)
        lrc_lines.append(f'[{mins:02d}:{secs:02d}.{cents:02d}]{text}')
    
    # Intro
    add_lrc(len(vocal_track), f'--- {cat_idx}. {cat_name} ---')
    intro_seg = AudioSegment.from_file(str(intro_path))
    vocal_track += intro_seg + AudioSegment.silent(duration=1200)
    
    # Verses
    for v_idx, (v_path, v_words) in enumerate(verse_files):
        verse_seg = AudioSegment.from_file(str(v_path))
        verse_start_ms = len(vocal_track)
        
        # Approximate time per word in verse
        dur_per_word = (len(verse_seg) / len(v_words))
        for w_idx, (w, t) in enumerate(v_words):
            w_ms = verse_start_ms + (w_idx * dur_per_word)
            add_lrc(w_ms, f'{w} — {t} (а {w} — {t})')
            
        vocal_track += verse_seg + AudioSegment.silent(duration=800)
        
    # Outro
    add_lrc(len(vocal_track), f'Отлично! Раздел {cat_name} пройден!')
    outro_seg = AudioSegment.from_file(str(outro_path))
    vocal_track += outro_seg + AudioSegment.silent(duration=2500)
    
    total_dur_ms = len(vocal_track)
    total_dur_sec = total_dur_ms / 1000.0
    
    # Export raw vocals to temp wav
    raw_vocals_wav = CACHE_DIR / f'cat_{cat_idx:02d}_vocals.wav'
    vocal_track.export(str(raw_vocals_wav), format='wav')
    
    # Mix with looping background music and master with ffmpeg loudnorm
    # Background volume: 0.22 (-13dB under vocals)
    # Background music loops infinitely to match length, fades out in last 3s
    temp_master = CACHE_DIR / f'cat_{cat_idx:02d}_master.mp3'
    
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-i', str(raw_vocals_wav),
        '-stream_loop', '-1', '-i', str(bg_file),
        '-filter_complex',
        f'[0:a]volume=1.0,aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[v];'
        f'[1:a]volume=0.22,afade=t=out:st={total_dur_sec-3.0}:d=3.0,aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[bg];'
        f'[v][bg]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-16:TP=-1.5:LRA=11[out]',
        '-map', '[out]',
        '-b:a', '192k',
        str(temp_master)
    ]
    res = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f'FFmpeg failed on cat {cat_idx}: {res.stderr}')
        
    # Copy to final output
    temp_master.rename(out_mp3)
    
    # Write LRC file
    with open(out_lrc, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lrc_lines) + '\n')
        
    # Set ID3 tags
    try:
        audio = EasyID3(str(out_mp3))
    except Exception:
        audio = MP3(str(out_mp3))
        audio.add_tags()
        audio = EasyID3(str(out_mp3))
        
    audio['title'] = f'{cat_idx:02d}. {cat_name}'
    audio['artist'] = 'English Study Vibes'
    audio['album'] = 'English A2-B2: 480 Vocabulary Songs'
    audio['tracknumber'] = f'{cat_idx}/9'
    audio['genre'] = 'Educational / Song'
    audio['date'] = '2026'
    audio.save()
    
    print(f'Track {cat_idx} complete: {mp3_filename} ({round(total_dur_sec, 1)}s)')
    return out_mp3

def build_mega_album(track_paths: list):
    mega_mp3 = OUT_DIR / 'English_Vocabulary_480_MEGA_ALBUM.mp3'
    mega_lrc = OUT_DIR / 'English_Vocabulary_480_MEGA_ALBUM.lrc'
    
    print('=== Building Full 480-Word Mega Album ===')
    concat_list = CACHE_DIR / 'concat_list.txt'
    with open(concat_list, 'w', encoding='utf-8') as f:
        for p in track_paths:
            f.write(f"file '{p.resolve()}'\n")
            
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(concat_list),
        '-c', 'copy',
        str(mega_mp3)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f'Mega album concatenation failed: {res.stderr}')
        
    # Combine LRCs
    total_offset_ms = 0.0
    combined_lrc = []
    for idx, p in enumerate(track_paths, 1):
        lrc_file = p.with_suffix('.lrc')
        seg = AudioSegment.from_file(str(p))
        if lrc_file.exists():
            with open(lrc_file, 'r', encoding='utf-8') as f:
                for line in f:
                    m = re.match(r'\[(\d+):(\d+(?:\.\d+)?)\](.*)', line.strip())
                    if m:
                        mins = int(m.group(1))
                        secs = float(m.group(2))
                        ms = (mins * 60 + secs) * 1000 + total_offset_ms
                        out_mins = int(ms // 60000)
                        out_secs = int((ms % 60000) // 1000)
                        out_cents = int((ms % 1000) // 10)
                        combined_lrc.append(f'[{out_mins:02d}:{out_secs:02d}.{out_cents:02d}]{m.group(3)}')
        total_offset_ms += len(seg)
        
    with open(mega_lrc, 'w', encoding='utf-8') as f:
        f.write('\n'.join(combined_lrc) + '\n')
        
    # Set ID3 tags on Mega Album
    try:
        audio = EasyID3(str(mega_mp3))
    except Exception:
        audio = MP3(str(mega_mp3))
        audio.add_tags()
        audio = EasyID3(str(mega_mp3))
        
    audio['title'] = '480 English Words - Complete Vocabulary Song'
    audio['artist'] = 'English Study Vibes'
    audio['album'] = 'English A2-B2: 480 Vocabulary Songs'
    audio['tracknumber'] = '1/1'
    audio['genre'] = 'Educational / Song'
    audio['date'] = '2026'
    audio.save()
    
    print(f'Mega Album Complete: {mega_mp3.name} ({round(total_offset_ms/1000.0, 1)}s)')

async def main():
    cards = parse_tsv()
    print(f'Loaded {len(cards)} cards from TSV.')
    groups = group_by_category(cards)
    print(f'Grouped into {len(groups)} categories:')
    for idx, (cat, words) in enumerate(groups, 1):
        print(f'  {idx}. {cat}: {len(words)} words')
        
    sem = asyncio.Semaphore(4)
    tasks = []
    for idx, (cat, words) in enumerate(groups, 1):
        tasks.append(generate_category_audio(idx, cat, words, sem))
        
    print('\n--- Synthesizing all vocal tracks in parallel ---')
    results = await asyncio.gather(*tasks)
    print('--- Vocal synthesis completed! ---\n')
    
    track_paths = []
    for (idx, (cat, words)), (intro_path, verse_files, outro_path) in zip(enumerate(groups, 1), results):
        p = build_category_song(idx, cat, intro_path, verse_files, outro_path)
        track_paths.append(p)
        
    build_mega_album(track_paths)
    print('\n🎉 ALL DONE! All 480 words assembled into songs with audio and lyrics!')

if __name__ == '__main__':
    asyncio.run(main())
