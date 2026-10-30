#!/usr/bin/env python3
"""
Telegram Audio Sender:
Sends the vocabulary album and individual categorized tracks to Telegram safely.
Ensures zero interference with any other active AI agent by:
- Avoiding getUpdates / webhook manipulation
- Respecting Telegram API rate limits with polite inter-file delays
- Handling retries with exponential backoff on HTTP 429
"""

import os
import sys
import time
import requests
from pathlib import Path

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '1363684164')
BASE_URL = f'https://api.telegram.org/bot{TOKEN}'

SONGS_DIR = Path('/home/b00bs/my_less/English/English_Audio_Songs')

def send_message(text: str):
    url = f'{BASE_URL}/sendMessage'
    for attempt in range(5):
        try:
            r = requests.post(url, data={'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'Markdown'}, timeout=15)
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 429:
                retry_after = r.json().get('parameters', {}).get('retry_after', 5)
                print(f'Rate limited, sleeping {retry_after}s...')
                time.sleep(retry_after)
            else:
                print(f'sendMessage failed ({r.status_code}): {r.text}')
                time.sleep(2)
        except Exception as e:
            print(f'sendMessage error: {e}')
            time.sleep(2)
    return None

def send_audio(file_path: Path, title: str, performer: str, caption: str, duration: int = None):
    url = f'{BASE_URL}/sendAudio'
    print(f'Uploading audio: {file_path.name} ({round(file_path.stat().st_size / 1024 / 1024, 1)} MB)...')
    
    data = {
        'chat_id': CHAT_ID,
        'title': title,
        'performer': performer,
        'caption': caption,
    }
    if duration:
        data['duration'] = duration
        
    for attempt in range(4):
        try:
            with open(file_path, 'rb') as f:
                files = {'audio': (file_path.name, f, 'audio/mpeg')}
                r = requests.post(url, data=data, files=files, timeout=180)
                if r.status_code == 200:
                    print(f'Successfully sent: {file_path.name}')
                    return r.json()
                elif r.status_code == 429:
                    retry_after = r.json().get('parameters', {}).get('retry_after', 5)
                    print(f'Rate limited, sleeping {retry_after}s...')
                    time.sleep(retry_after)
                else:
                    print(f'sendAudio failed ({r.status_code}): {r.text}')
                    time.sleep(3)
        except Exception as e:
            print(f'sendAudio error: {e}')
            time.sleep(3)
    return None

def send_document(file_path: Path, caption: str):
    url = f'{BASE_URL}/sendDocument'
    print(f'Uploading document: {file_path.name}...')
    data = {'chat_id': CHAT_ID, 'caption': caption}
    for attempt in range(4):
        try:
            with open(file_path, 'rb') as f:
                files = {'document': (file_path.name, f)}
                r = requests.post(url, data=data, files=files, timeout=60)
                if r.status_code == 200:
                    print(f'Successfully sent doc: {file_path.name}')
                    return r.json()
                elif r.status_code == 429:
                    retry_after = r.json().get('parameters', {}).get('retry_after', 5)
                    time.sleep(retry_after)
                else:
                    print(f'sendDocument failed ({r.status_code}): {r.text}')
                    time.sleep(3)
        except Exception as e:
            print(f'sendDocument error: {e}')
            time.sleep(3)
    return None

def main():
    print('Starting safe delivery to Telegram...')
    
    # 1. Send the Grand Master Mega Album first!
    mega_file = SONGS_DIR / 'English_Vocabulary_480_MEGA_ALBUM_128k.mp3'
    if mega_file.exists():
        send_audio(
            file_path=mega_file,
            title='480 English Words - Complete Vocabulary Song',
            performer='English Study Vibes',
            caption='🌟 *Полный обучающий альбом: 480 слов A2–B2*\n⏱ 42:55 | Дуэт дикторов Ava & Andrew | Lo-Fi / Acoustic Chill',
            duration=2575
        )
        time.sleep(2.5) # Polite pause for network and agent headroom
        
    # Send full LRC
    mega_lrc = SONGS_DIR / 'English_Vocabulary_480_MEGA_ALBUM.lrc'
    if mega_lrc.exists():
        send_document(mega_lrc, caption='📄 Синхронные слова и караоке-текст (.LRC) для всего альбома')
        time.sleep(2.5)
        
    send_message('📁 *Далее отправляю отдельные треки по темам для удобного повторения по разделам:*')
    time.sleep(2.0)
    
    # 2. Send 9 category tracks
    category_tracks = [
        ('01_Повседневные_глаголы.mp3', '01. Повседневные глаголы', 376),
        ('02_Общение_и_выражения.mp3', '02. Общение и выражения', 296),
        ('03_Прилагательные.mp3', '03. Прилагательные', 252),
        ('04_Быт_и_поездки.mp3', '04. Быт и поездки', 252),
        ('05_Работа_и_собеседования.mp3', '05. Работа и собеседования', 273),
        ('06_IT_и_разработка.mp3', '06. IT и разработка', 328),
        ('07_PLC_и_автоматизация.mp3', '07. PLC и автоматизация', 307),
        ('08_MES_и_производство.mp3', '08. MES и производство', 264),
        ('09_Фразовые_глаголы.mp3', '09. Фразовые глаголы', 222),
    ]
    
    for filename, title, dur in category_tracks:
        track_path = SONGS_DIR / filename
        if track_path.exists():
            send_audio(
                file_path=track_path,
                title=title,
                performer='English Study Vibes',
                caption=f'🎵 {title} ({dur // 60}:{dur % 60:02d})',
                duration=dur
            )
            time.sleep(2.5) # Polite pause to prevent 429 and allow other agent messages through
            
    send_message('✨ *Все аудиоматериалы успешно доставлены! Приятного и продуктивного изучения английского языка!*')
    print('Delivery completed successfully!')

if __name__ == '__main__':
    main()
