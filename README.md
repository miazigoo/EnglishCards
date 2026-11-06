# 📱 English Flashcards — IT, Backend & Workplace English (v4.0)

<p align="center">
  <img src="app_english_cards/app/src/main/res/drawable/ic_app_logo.png" width="120" height="120" alt="English Flashcards Logo" />
</p>

<p align="center">
  <b>Профессиональное Android-приложение для изучения IT, Backend и профессионального английского языка методом научно обоснованного интервального повторения FSRS v4.5 с активным вспоминанием (Active Recall), чистой озвучкой Andrew и реальными примерами кода.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Android_8.0+-3DDC84?style=flat-square&logo=android&logoColor=white" alt="Platform" />
  <img src="https://img.shields.io/badge/Language-Kotlin_2.0-7F52FF?style=flat-square&logo=kotlin&logoColor=white" alt="Kotlin" />
  <img src="https://img.shields.io/badge/Storage-Room_SQLite_v2-38BDF8?style=flat-square" alt="Room" />
  <img src="https://img.shields.io/badge/Algorithm-FSRS_v4.5-8B5CF6?style=flat-square" alt="FSRS" />
  <img src="https://img.shields.io/badge/Cards-2%2C160_Units-22C55E?style=flat-square" alt="Cards" />
  <img src="https://img.shields.io/badge/Lessons-12_Micro--Lessons-F59E0B?style=flat-square" alt="Lessons" />
  <img src="https://img.shields.io/badge/Audio-Single--Segment_HD-06B6D4?style=flat-square" alt="Audio" />
  <img src="https://img.shields.io/badge/Theme-OLED_Dark_120Hz-black?style=flat-square" alt="OLED Dark Theme" />
  <img src="https://img.shields.io/badge/Acceptance-34%2F36_Verified-success?style=flat-square" alt="Acceptance" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square" alt="License" />
</p>

---

## 📸 Скриншоты интерфейса

<table align="center" width="100%">
  <tr>
    <th width="33%" align="center">🏠 Меню и FSRS очередь «Сегодня»</th>
    <th width="33%" align="center">🃏 Активное вспоминание (Active Recall)</th>
    <th width="33%" align="center">💡 Технические детали и реальный код</th>
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
    <td align="center"><i>Очередь «Сегодня», инструменты (Уроки, Поиск, Статистика, Бэкап)</i></td>
    <td align="center"><i>Лицевая сторона со скрытым ответом, педагогический разбор, 4 FSRS оценки и Undo</i></td>
    <td align="center"><i>Реальные сниппеты (Python 3.12 / Django / FastAPI) с кнопкой копирования</i></td>
  </tr>
</table>

---

## 🌟 Ключевые возможности версии 4.0

- 📚 **Словарные колоды:** исходные 480 слов Anki возвращены в приложение; отдельная колода содержит 500 уникальных английских слов, найденных в 42 разделах официальной документации Django и FastAPI. Пересечение колод использует одну карточку, поэтому прогресс не раздваивается.
- 🎙 **Перезаписанная озвучка слов:** английское слово и русский смысл записаны отдельными файлами голосом `en-US-AndrewMultilingualNeural`. Старая озвучка Anki в этих колодах не используется.
- 📝 **Проверенные смыслы:** исправлены ошибочный перевод `whether or not` и многозначные слова вроде `application`, `yield`, `release`. Контекстные фразы дополнены там, где исходный Anki-файл содержал только слово и перевод.
- ✍️ **Тренировка с проверкой:** очередь «Сегодня» учитывает английский → русский и русский → английский отдельно. Во втором направлении нужно написать слово. Диктант проверяет слово по звучанию, а упражнение с пропуском — в предложении. Просмотр и прослушивание карточек не оцениваются как знания.
- 📖 **Читаю документацию:** 10 коротких текстов по Django и FastAPI, перевод слова по нажатию, добавление незнакомого слова в повторение и вопросы на понимание.
- 🗣 **Контекст ко всем 480 словам Anki:** английская фраза, русский перевод и отдельная озвучка Andrew для каждой фразы. Источники части двуязычных примеров — [Tatoeba](https://tatoeba.org), текстовые данные распространяются по [CC BY 2.0 FR](https://creativecommons.org/licenses/by/2.0/fr/); остальные примеры подготовлены для этого проекта. Идентификаторы исходных предложений хранятся в `content/anki_contexts.json`.

Для обновления материала: `python3 scripts/fetch_english_docs_corpus.py`, `python3 scripts/fetch_anki_contexts.py`, `python3 scripts/curate_anki_contexts.py`, `python3 scripts/restore_learning_vocabulary.py`, `python3 scripts/build_readings.py`, затем `.venv/bin/python scripts/build_content.py --publish` и `.venv/bin/python scripts/generate_learning_vocabulary_audio.py`.

- 🎯 **Настоящая очередь повторения «Сегодня»:**
  - Кнопка «Сегодня» загружает строго наступившие по расписанию FSRS карточки (`due <= now`) плюс 10 новых карточек в день.
  - Повтор «Снова» (Again) возвращает карточку в очередь по реальному интервалу шага, а не по кругу всей базы.
- 👁 **Режим активного вспоминания (Active Recall) без подсказок:**
  - Лицевая сторона показывает только стимул (термин). Перевод, разбор имени (`name_breakdown`), примеры, технический код и кнопки оценки скрыты до нажатия **«👁 Показать ответ»**.
  - **Никаких аудиоспойлеров:** автовоспроизведение и тапы до раскрытия ответа озвучивают только изучаемый термин (`playPrompt`), переводной трек до действия пользователя отключен.
- ↩ **Кнопка «Отмена» (Undo):**
  - Возможность мгновенно отменить ошибочно поставленную оценку прямо в плеере.
  - Атомарная Room-транзакция (`undoLastReviewTransaction`) восстанавливает предыдущее состояние интервала и помечает событие отмененным.
- 🧠 **Проверенный алгоритм FSRS v4.5:**
  - Исправлена ветка `Hard`: интервал рассчитывается из `nextInterval(s)` с учетом целевого retention (0.80, 0.90, 0.97) и строго соблюдает `maximumInterval`.
  - Монотонный замер времени размышления (`SystemClock.elapsedRealtime()`) с защитой от искажения статистики.
  - Уникальный UUID `attemptId` защищает от дублирования при двойном тапе.
- 📚 **2 160 карточек:**
  - **0 шаблонных фраз:** 1 524 шаблонных предложения `We use ... in ... module.` заменены живыми естественными фразами и точными русскими переводами.
  - Удалены утечки ответов в скобках из всех проверочных формулировок.
  - Исправлены все 120 сниппетов `hasattr` на эталонный класс `Driver`, устранены синтаксические ошибки top-level `await`.
  - 50 карточек снабжены вторыми контекстными примерами.
- 🎓 **12 интерактивных микроуроков («📚 Уроки»):**
  - Упакованы в assets APK (`assets/lessons/`) и доступны в удобном диалоговом окне.
  - Правило, живые примеры и 3 практических упражнения с мгновенной валидацией и разбором ошибок.
- 🔍 **Полнотекстовый словарь и поиск («🔍 Поиск»):**
  - Мгновенный поиск по 2 160 карточкам: по термину, русскому переводу, тегам и коду.
- 📊 **Честная статистика («📊 Статистика»):**
  - Раздельный учет активных сессий и времени пассивного слушания.
  - Подсчет успешных ответов, процента удержания и текущего долга повторений.
- 💾 **Резервное копирование и экспорт («💾 Бэкап»):**
  - Экспорт прогресса FSRS и истории ответов в JSON через буфер обмена.
  - Импорт с проверкой схемы и транзакционным восстановлением базы.
- 🎙 **Студийная озвучка Andrew без склеенных повторов:**
  - Основной голос: `en-US-AndrewMultilingualNeural`.
  - Одиночные сегменты (`term_en`, `meaning_ru`, `example_en`, `example_ru`) с точным счетчиком повторений (2x, 3x).
  - Для `rsplit` гарантированы разбор right + split, перевод «разделить справа» и объяснение сохранения порядка.
- ☀️ **Режим бодрствования экрана:**
  - Во время активного изучения карточек экран устройства не гаснет (`FLAG_KEEP_SCREEN_ON`).
- ⚡ **100% Офлайн:**
  - Работает автономно в авиарежиме без обращений к сети.

---

## 📋 Протокол приёмки (Acceptance Matrix)

Подробные результаты проверки 36 исходных сценариев спецификации зафиксированы в документах:
- [Отчёт о приёмке v4 (Markdown)](reports/acceptance_v4.md)
- [Машинночитаемый отчёт (JSON)](reports/acceptance_v4.json)

---

## 🛠 Архитектура и стек технологий

- **Платформа:** Android 8.0+ (API 24 - 35)
- **Язык разработки:** Kotlin 2.0 / Java 17
- **База данных:** AndroidX Room 2.6.1 (SQLite, v2)
- **Асинхронность:** Kotlin Coroutines & LifecycleScope
- **Интервальное повторение:** FSRS v4.5 Scheduler (Open Spaced Repetition)
- **UI:** Material Components 3, ViewPager2, BottomSheetDialog, ViewBinding
- **Аудио:** Android MediaPlayer с AssetFileDescriptor и сессионными токенами отмены

---

## 🧪 Запуск тестов и валидация

```bash
# 1. Валидация контента и JSON Schema (Python 3.12+)
python3 scripts/validate_content.py

# 2. Проверка канонического источника (read-only check)
python3 scripts/build_content.py --check

# 3. Запуск тестового набора pytest
pytest tests/

# 4. Валидация аудиофайлов и манифеста
python3 scripts/validate_audio.py

# 5. Модульные тесты Android (FSRSScheduler, Room)
cd app_english_cards && ./gradlew testDebugUnitTest

# 6. Сборка Debug APK
cd app_english_cards && ./gradlew assembleDebug
```
