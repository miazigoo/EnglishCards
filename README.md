# 📱 English Flashcards — IT & Backend (Android)

<p align="center">
  <img src="app_english_cards/app/src/main/res/drawable/ic_app_logo.png" width="128" height="128" alt="English Flashcards Logo" />
</p>

<p align="center">
  <b>Современное Android-приложение для эффективного изучения IT, Backend и Python терминологии методом интервального повторения карточек с чистым студийным произношением и живыми примерами в коде.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Android_8.0+-green.svg" alt="Platform" />
  <img src="https://img.shields.io/badge/Kotlin-2.0.21-blue.svg" alt="Kotlin" />
  <img src="https://img.shields.io/badge/Cards-1%2C529_Terms-orange.svg" alt="Cards" />
  <img src="https://img.shields.io/badge/Audio-Edge--TTS_Studio-purple.svg" alt="Audio" />
  <img src="https://img.shields.io/badge/Theme-OLED_Dark-black.svg" alt="OLED Dark Theme" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="License" />
</p>

---

## 🌟 Ключевые особенности

- 📚 **1 529 специализированных IT-карточек:** Полная база терминов, отобранных из реального enterprise бэкенд-проекта (микросервисы, Django ORM, FastAPI, Pydantic v2, PostgreSQL, Celery, Redis, промышленный IoT и PLC).
- 🎙 **Нативное студийное произношение (HD):** Все 1 529 карточек озвучены естественным голосом носителя языка (`en-US-AndrewMultilingualNeural`). Никаких роботизированных искажений или некорректных транслитераций (например, *bug* звучит как */bʌɡ/* — баг, а не «буг»).
- 💡 **Модальное окно с примерами в коде:** На каждой карточке доступна кнопка **«💡 Пример в коде»**, открывающая модальный диалог (`BottomSheet`) с боевым фрагментом кода на Python 3.12 / Django 5+ / FastAPI / Pydantic и кнопкой быстрого копирования `📋 Скопировать`.
- 📊 **Система умного запоминания:**
  - `🟢 Запомнил` — переводит карточку в освоенные.
  - `🟡 Повторить` — отправляет слово в отдельную колоду «🔥 Сложные слова».
  - `⚪ Новое` — статус новых карточек.
  - Сохранение прогресса в `SharedPreferences` с подсчетом процента освоения.
- 🎨 **Премиальный OLED Dark интерфейс:** Глубокая черная тема (`#000000`, `#141418`, `#38BDF8`), адаптированная под 120 FPS экраны, снижающая нагрузку на глаза и экономящая заряд батареи.
- ⚡ **100% Офлайн:** Все аудиофайлы (сжаты до 20 kbps mono via LAME ffmpeg) и база JSON вшиты в APK. Интернет не требуется.

---

## 📂 Структура репозитория

```text
├── app_english_cards/             # Исходный код Android приложения (Kotlin + Gradle)
│   ├── app/
│   │   ├── src/main/
│   │   │   ├── assets/
│   │   │   │   ├── cards.json     # База 1 529 карточек с переводами, IPA и примерами
│   │   │   │   └── audio/         # 1 529 оптимизированных MP3 аудиофайлов
│   │   │   ├── java/com/english/flashcards/
│   │   │   │   ├── audio/         # AudioController (управление воспроизведением и повторами)
│   │   │   │   ├── data/          # FlashcardRepository, ProgressManager
│   │   │   │   ├── model/         # Flashcard, CardStatus
│   │   │   │   └── ui/            # CardPagerAdapter, CategoryMenuAdapter
│   │   │   └── res/               # Layouts, Drawables, Themes, Icons
├── builder_modules/               # Модули сборки и классификации терминов
├── assemble_backend_vocabulary.py # Скрипт парсинга и фильтрации слов из исходников бэкенда
├── enrich_cards_with_examples.py  # Генерация примеров кода и архитектурных пояснений
├── generate_full_assets_v3.py     # Синтез аудио через Edge-TTS и конвертация в MP3
├── docs/                          # Подробная архитектурная и техническая документация
├── TECH_SPEC.md                   # Техническая спецификация проекта
└── README.md                      # Документация проекта
```

---

## 📚 Тематические колоды (13 категорий)

| Категория | Количество карточек | Описание |
| :--- | :---: | :--- |
| **Python: встроенные методы и функции** | 82 | `enumerate()`, `isinstance()`, `zip()`, `getattr()` и методы строк/списков |
| **Django: ORM, модели и QuerySet** | 106 | `select_related()`, `prefetch_related()`, `annotate()`, `F()`, `Q()` |
| **FastAPI, Pydantic & API** | 56 | `Depends()`, `BaseModel`, `Field()`, `status_code`, валидация |
| **Базы данных, SQL & Транзакции** | 62 | `atomic()`, `commit`, `rollback`, `indexes`, `foreign_key` |
| **Backend: архитектура и паттерны (Nouns)** | 145 | `repository`, `adapter`, `middleware`, `payload`, `dependency` |
| **Backend: действия и методы (Verbs)** | 186 | `serialize`, `dispatch`, `authenticate`, `sanitize`, `truncate` |
| **Backend: состояния и флаги (Adjectives)** | 100 | `immutable`, `deprecated`, `redundant`, `persistent`, `stale` |
| **IoT, Оборудование & Сеть (MES/PLC)** | 88 | `payload`, `baudrate`, `firmware`, `checksum`, `socket`, `barcode` |
| **Ошибки, Исключения & Дебаг** | 80 | `traceback`, `breakpoint`, `overflow`, `deadlock`, `unauthorized` |
| **DevOps, Окружение & Инфраструктура** | 80 | `container`, `deploy`, `cluster`, `env`, `scaling`, `ingress` |
| **Общие IT и алгоритмические понятия** | 100 | `concurrency`, `latency`, `throughput`, `cache`, `asynchronous` |
| **Разговорный IT и командная работа** | 90 | `standup`, `blocker`, `refactor`, `roadmap`, `merge_request` |
| **Английский для IT: базовая лексика** | 354 | Общая лексика категорий A2–B2 для чтения документации |

---

## 🛠 Сборка и запуск проекта

### Требования:
- **Android Studio** Hedgehog / Iguana / Ladybug или новее.
- **JDK 17+**.
- **Android SDK:** `compileSdk 34`, `minSdk 26`, `targetSdk 34`.

### Сборка через Gradle CLI:
```bash
cd app_english_cards
./gradlew assembleDebug
```
Готовый APK файл будет расположен в:
`app_english_cards/app/build/outputs/apk/debug/app-debug.apk`

### Установка на смартфон через ADB:
```bash
adb install -r -d app_english_cards/app/build/outputs/apk/debug/app-debug.apk
adb shell am start -n com.english.flashcards/.MainActivity
```

---

## 📋 Формат данных карточек (`cards.json`)

Каждая карточка содержит полную информацию для воспроизведения, обучения и интеграции:

```json
{
  "id": 1,
  "word": "enumerate()",
  "translation": "enumerate() — возвращает кортежи (индекс, значение) при итерации по коллекции",
  "clean_translation": "нумерует элементы",
  "ipa": "/ɪˈnumərˌeɪt/",
  "transcription_ru": "инuмерэйт",
  "category": "Python: встроенные методы и функции",
  "audio": "word_0001.mp3",
  "example": "# Нумерация элементов списка в цикле:\ndevices = ['scanner_1', 'scale_a', 'laser_marker']\nfor idx, name in enumerate(devices, start=1):\n    print(f'Станок #{idx}: {name}')",
  "example_note": "Функция enumerate() избавляет от ручного счетчика i += 1 и возвращает пары (индекс, значение)."
}
```

---

## 📄 Лицензия

Распространяется под лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).
