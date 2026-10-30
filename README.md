# 📱 English Flashcards — IT & Backend (Android)

<p align="center">
  <img src="app_english_cards/app/src/main/res/drawable/ic_app_logo.png" width="120" height="120" alt="English Flashcards Logo" />
</p>

<p align="center">
  <b>Умное Android-приложение для изучения IT, Backend и Python терминологии методом интервального повторения карточек с естественным американским произношением и реальными примерами в коде.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Android_8.0+-3DDC84?style=flat-square&logo=android&logoColor=white" alt="Platform" />
  <img src="https://img.shields.io/badge/Language-Kotlin_2.0-7F52FF?style=flat-square&logo=kotlin&logoColor=white" alt="Kotlin" />
  <img src="https://img.shields.io/badge/Cards-1%2C529_Terms-38BDF8?style=flat-square" alt="Cards" />
  <img src="https://img.shields.io/badge/Audio-Edge--TTS_HD-F59E0B?style=flat-square" alt="Audio" />
  <img src="https://img.shields.io/badge/Theme-OLED_Dark_120Hz-black?style=flat-square" alt="OLED Dark Theme" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square" alt="License" />
</p>

---

## 📸 Скриншоты интерфейса

<table align="center" width="100%">
  <tr>
    <th width="33%" align="center">🏠 Меню и Тематические колоды</th>
    <th width="33%" align="center">🃏 Карточка со статусом и подсказкой</th>
    <th width="33%" align="center">💡 Модалка с боевым примером в коде</th>
  </tr>
  <tr>
    <td align="center">
      <img src="docs/screenshots/screenshot_menu.png" width="95%" alt="Главное меню и колоды" />
    </td>
    <td align="center">
      <img src="docs/screenshots/screenshot_card.png" width="95%" alt="Экран флеш-карточки" />
    </td>
    <td align="center">
      <img src="docs/screenshots/screenshot_modal.png" width="95%" alt="Пример использования в коде" />
    </td>
  </tr>
  <tr>
    <td align="center"><i>Общий прогресс, колода повторения и 13 тематических разделов</i></td>
    <td align="center"><i>IPA-транскрипция, русская подсказка, аудио и кнопки рейтинга</i></td>
    <td align="center"><i>Реальный синтаксис (Python/Django/FastAPI) и кнопка «📋 Скопировать»</i></td>
  </tr>
</table>

---

## 🌟 Ключевые возможности

- 📚 **1 529 специализированных карточек:** Термины и методы, извлеченные из реальной enterprise кодовой базы: микросервисы, Django ORM, FastAPI, Pydantic v2, PostgreSQL, Celery, Redis, промышленный IoT и PLC.
- 🎙 **Естественное американское произношение HD:** Озвучка синтезирована студийным мужским голосом (`en-US-AndrewMultilingualNeural`) с выверенной фонетикой носителя языка. Никаких «буг» вместо *bag* или искаженных ударений.
- 💡 **Контекстные примеры кода (BottomSheet):** Нажатие на кнопку **«💡 Пример в коде»** открывает модальное окно с практическим сниппетом на Python 3.12 / Django 5 / FastAPI и кнопкой быстрого копирования в буфер обмена.
- 📊 **Интервальное обучение и отметки:**
  - `🟢 Запомнил` — фиксирует слово как выученное.
  - `🟡 Повторить` — автоматически добавляет слово в специальную колоду «🔥 Сложные слова».
  - `⚪ Новое` — статус неизученных слов.
  - Прогресс надежно сохраняется в локальной памяти устройства.
- 🖤 **Премиальный OLED Dark интерфейс:** Глубокая черная палитра (`#000000`, `#141418`, `#38BDF8`), плавная прокрутка ViewPager2 на частоте 120 Гц, отсутствие рекламы и полная приватность.
- ⚡ **100% Офлайн-режим:** Вся база данных и 1 529 сжатых аудиофайлов вшиты внутрь приложения (размер APK всего ~38.9 МБ). Интернет для работы не требуется.

---

## 📚 Тематические колоды (13 категорий)

| Категория | Карточек | Примеры терминов и методов |
| :--- | :---: | :--- |
| **Python: встроенные методы и функции** | 82 | `enumerate()`, `isinstance()`, `zip()`, `getattr()`, `strip()`, `split()` |
| **Django: ORM, модели и QuerySet** | 106 | `select_related()`, `prefetch_related()`, `annotate()`, `aggregate()`, `F()`, `Q()` |
| **FastAPI, Pydantic & API** | 56 | `Depends()`, `BaseModel`, `Field()`, `status_code`, `response_model` |
| **Базы данных, SQL & Транзакции** | 62 | `atomic()`, `commit`, `rollback`, `indexes`, `foreign_key`, `cascade` |
| **Backend: архитектура и паттерны (Nouns)** | 145 | `repository`, `adapter`, `middleware`, `payload`, `dependency`, `singleton` |
| **Backend: действия и методы (Verbs)** | 186 | `serialize`, `dispatch`, `authenticate`, `sanitize`, `truncate`, `paginate` |
| **Backend: свойства и флаги (Adjectives)** | 100 | `immutable`, `deprecated`, `redundant`, `persistent`, `stale`, `concurrent` |
| **IoT, Оборудование & Сеть (MES/PLC)** | 88 | `baudrate`, `firmware`, `checksum`, `socket`, `barcode`, `handshake` |
| **Ошибки, Исключения & Дебаг** | 80 | `traceback`, `breakpoint`, `overflow`, `deadlock`, `unauthorized`, `fatal` |
| **DevOps, Окружение & Инфраструктура** | 80 | `container`, `deploy`, `cluster`, `env`, `scaling`, `ingress`, `orchestration` |
| **Общие IT и алгоритмические понятия** | 100 | `concurrency`, `latency`, `throughput`, `cache`, `asynchronous`, `idempotent` |
| **Разговорный IT и командная работа** | 90 | `standup`, `blocker`, `refactor`, `roadmap`, `merge_request`, `review` |
| **Английский для IT: базовая лексика** | 354 | Общая базовая лексика A2–B2 для чтения технической документации |

---

## 📂 Структура проекта

```text
├── app_english_cards/             # Исходный код Android приложения (Kotlin + Gradle)
│   ├── app/
│   │   ├── src/main/
│   │   │   ├── assets/
│   │   │   │   ├── cards.json     # 1 529 карточек (слова, переводы, транскрипции, примеры кода)
│   │   │   │   └── audio/         # 1 529 оптимизированных MP3 треков (20 kbps mono)
│   │   │   ├── java/com/english/flashcards/
│   │   │   │   ├── audio/         # Управление воспроизведением и повторами звука
│   │   │   │   ├── data/          # Репозиторий карточек и менеджер прогресса
│   │   │   │   ├── model/         # Модели данных Flashcard и CardStatus
│   │   │   │   └── ui/            # ViewPager2 CardPagerAdapter, CategoryMenuAdapter
│   │   │   └── res/               # Разметка интерфейса, OLED темная тема, векторные иконки
├── docs/
│   ├── ARCHITECTURE.md            # Техническое описание архитектуры приложения
│   └── screenshots/               # Скриншоты приложения для документации
├── builder_modules/               # Модули сборки и классификации терминологии
├── assemble_backend_vocabulary.py # Парсер и сборщик лексики из backend-проекта
├── enrich_cards_with_examples.py  # Генератор боевых примеров кода и пояснений
├── generate_full_assets_v3.py     # Конвейер синтеза звука Edge-TTS и сжатия LAME
├── TECH_SPEC.md                   # Техническая спецификация
└── README.md                      # Документация проекта
```

---

## 🛠 Сборка и установка

### Требования
* **Android Studio** (Hedgehog 2023.1.1 или новее)
* **JDK 17** или новее
* **Android SDK:** `compileSdk 34`, `minSdk 26`, `targetSdk 34`

### Сборка через Gradle CLI:
```bash
cd app_english_cards
./gradlew assembleDebug
```
Собранный файл будет находиться по пути:
`app_english_cards/app/build/outputs/apk/debug/app-debug.apk`

### Установка на телефон через ADB:
```bash
adb install -r -d app_english_cards/app/build/outputs/apk/debug/app-debug.apk
adb shell am start -n com.english.flashcards/.MainActivity
```

---

## 📋 Формат данных карточек (`cards.json`)

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

Проект распространяется под лицензией [MIT](LICENSE).
