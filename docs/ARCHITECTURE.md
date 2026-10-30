# 🏛 Архитектура приложения English Flashcards

## 1. Обзор архитектуры

Приложение построено по принципам модульности, автономности (offline-first) и высокой производительности на Android-устройствах (включая поддержку дисплеев 120 Гц).

```text
┌─────────────────────────────────────────────────────────────┐
│                       UI Layer (XML)                        │
│   MainActivity ────► ViewPager2 ────► CardPagerAdapter      │
│         │                                    │              │
│         ▼                                    ▼              │
│   CategoryMenuAdapter             BottomSheetDialog (Modal) │
└───────────────────────┬──────────────────────┬──────────────┘
                        │                      │
┌───────────────────────▼──────────────────────▼──────────────┐
│                      Domain / Business                      │
│   AudioController (Loop, Repetition, Safe Error Handling)  │
│   ProgressManager (SharedPreferences Status Tracking)       │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                         Data Layer                          │
│   FlashcardRepository (AssetManager -> cards.json)          │
│   Assets: /audio/word_*.mp3 (1,529 LAME 20kbps MP3 tracks)  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Ключевые компоненты

### 2.1 UI Layer
- **`MainActivity.kt`**: Главный координатор приложения. Управляет переключением между экраном-заставкой (Splash with smooth progress animation), меню выбора категорий и интерактивным плеером карточек.
- **`CardPagerAdapter.kt`**: Оптимизированный адаптер для `ViewPager2`. Отвечает за рендеринг карточки, подсветку статуса (`Запомнил` / `Повторить` / `Новое`), плавную анимацию бэйджей и обработку клика по кнопке «💡 Пример в коде».
- **`CategoryMenuAdapter.kt`**: Отображение списка из 13 тематических колод со шкалой прогресса по каждой категории.

### 2.2 Аудио-подсистема (`AudioController.kt`)
- Использует нативный `android.media.MediaPlayer` с загрузкой дескрипторов из `assets/audio/word_XXXX.mp3` через `AssetFileDescriptor`.
- Поддерживает режимы повтора: 1x, 2x, 3x для каждого слова.
- Автоматический переход к следующей карточке (Auto-Advance) по завершении цикла повторов.
- Безопасная обработка фокусов аудио и паузы жизненного цикла Android (`onPause`, `onDestroy`).

### 2.3 Система прогресса (`ProgressManager.kt`)
- Сохраняет идентификаторы карточек в `SharedPreferences` под тремя состояниями:
  - `LEARNED` (Освоенные карточки, зеленый бэйдж)
  - `HARD` (Карточки, требующие повторения, желтый бэйдж)
  - `NEW` (Новые слова)
- Обеспечивает мгновенный пересчет агрегированной статистики по всей колоде и по отдельным категориям.

---

## 3. Модальное окно примеров в коде (`dialog_card_example.xml`)
- Реализовано на базе `com.google.android.material.bottomsheet.BottomSheetDialog`.
- Моноширинный блок кода обернут в `HorizontalScrollView` для удобного чтения широких строк кода без нежелательных переносов.
- Интегрирован `android.content.ClipboardManager` для копирования фрагмента в системный буфер обмена нажатием на `btnCopyCode`.

---

## 4. Пайплайн подготовки данных (Python)
- **`assemble_backend_vocabulary.py`**: Токенизация и лемматизация терминов из реального кодовой базы FastAPI/Django backend (`devandprod_backend`).
- **`enrich_cards_with_examples.py`**: Интеллектуальное обогащение карточек контекстными сниппетами кода и практическими заметками.
- **`generate_full_assets_v3.py`**: Синтез речи через Microsoft Edge-TTS (`en-US-AndrewMultilingualNeural`) и пакетное сжатие в 20 kbps MP3 mono через `ffmpeg`.
