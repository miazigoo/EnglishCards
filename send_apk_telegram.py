#!/usr/bin/env python3
"""
Sends the compiled English_Cards_IT_1529_v2.0.apk to Telegram via Bot API.
Safe transmission ensuring zero interference with any other active agents.
"""

import os
import sys
import time
import requests
from pathlib import Path

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '1363684164')
BASE_URL = f'https://api.telegram.org/bot{TOKEN}'
APK_PATH = Path('/home/b00bs/my_less/English/English_Cards_IT_1529_v2.0.apk')

def send_apk():
    if not APK_PATH.exists():
        print(f"Error: {APK_PATH} not found!")
        sys.exit(1)

    url = f"{BASE_URL}/sendDocument"
    size_mb = round(APK_PATH.stat().st_size / 1024 / 1024, 1)
    caption = (
        "🚀 *English Flashcards IT & Backend — Версия 2.1!*\n\n"
        "✨ *Что нового:*\n"
        "• 💡 *Модальное окно с примерами в коде:* на каждой из 1 529 карточек появилась кнопка «💡 Пример в коде»!\n"
        "• 💻 *Реальные контекстные сниппеты:* для каждого слова/метода написан боевой пример использования в Python 3.12, Django 5+, FastAPI, Pydantic v2, PostgreSQL или IoT.\n"
        "• 📋 *Копирование в 1 клик:* кнопка «📋 Скопировать» для быстрой вставки кода в редактор.\n"
        "• 📚 *1 529 карточек:* термины, методы, паттерны и архитектурные сущности.\n"
        "• 🎙 *Американское произношение HD:* естественный студийный голос en-US с правильной фонетикой.\n"
        "• 📊 *Система умного обучения:* отметки «✅ Запомнил» и «⚠️ Повторить», статистика и отдельная колода «🔥 На повторение».\n\n"
        f"📦 Размер файла: {size_mb} МБ. Приложение уже обновлено на смартфоне!"
    )

    print(f"Uploading {APK_PATH.name} ({size_mb} MB) to Telegram chat {CHAT_ID}...")

    for attempt in range(5):
        try:
            with open(APK_PATH, 'rb') as f:
                files = {'document': (APK_PATH.name, f, 'application/vnd.android.package-archive')}
                data = {
                    'chat_id': CHAT_ID,
                    'caption': caption,
                    'parse_mode': 'Markdown'
                }
                r = requests.post(url, data=data, files=files, timeout=300)

            if r.status_code == 200:
                print("APK successfully delivered to Telegram!")
                return True
            elif r.status_code == 429:
                wait = r.json().get('parameters', {}).get('retry_after', 10)
                print(f"Telegram rate limit: waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"sendDocument error ({r.status_code}): {r.text}")
                time.sleep(3)
        except Exception as e:
            print(f"Connection error (attempt {attempt+1}): {e}")
            time.sleep(4)

    return False

if __name__ == '__main__':
    ok = send_apk()
    sys.exit(0 if ok else 1)
