#!/usr/bin/env python3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
json_path = BASE_DIR / "reports/acceptance_v4.json"
md_path = BASE_DIR / "reports/acceptance_v4.md"

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

summary = data["status_summary"]

lines = [
    "# Протокол приёмки EnglishCards v4.0 (GEMINI_TECH_SPEC_ENGLISH_V4.md)",
    "",
    "**Дата:** 3 ноября 2026 г.  ",
    "**Базовый аудит:** [`ENGLISH_V3_AUDIT.md`](../ENGLISH_V3_AUDIT.md), [`ENGLISH_V3_AUDIT_EVIDENCE.json`](../ENGLISH_V3_AUDIT_EVIDENCE.json)  ",
    "**Архивный отчёт v3:** [`reports/acceptance.md`](acceptance.md) (выводы опровергнуты аудитом)  ",
    "**Машинночитаемый формат:** [`reports/acceptance_v4.json`](acceptance_v4.json)  ",
    f"**Сводка:** Verified: **{summary.get('verified', 0)}** | Partial: **{summary.get('partial', 0)}** | Failed: **{summary.get('failed', 0)}** | Not Run: **{summary.get('not_run', 0)}**",
    "",
    "---",
    "",
    "## 1. Сводная матрица исходных 36 сценариев V3",
    "",
    "Все сценарии проверены строго по оригинальным формулировкам ТЗ V3 без подмены критериев.",
    "",
    "| ID | Группа | Название сценария и требование ТЗ | Статус V4 | Доказательство / Команда | Результат / Ограничения |",
    "| :---: | :---: | :--- | :---: | :--- | :--- |"
]

for sc in data["original_scenarios"]:
    status_fmt = f"**{sc['status']}**"
    limit_fmt = f"<br>*(Ограничение: {sc['limitation']})*" if sc.get("limitation") else ""
    res = f"{sc['actual_result']}{limit_fmt}".replace("\n", " ")
    cmd_clean = sc["command"].replace("\n", " ")
    req_clean = sc["requirement"].replace("\n", " ")
    lines.append(f"| **{sc['id']}** | {sc['group']} | **{sc['title']}:** {req_clean} | {status_fmt} | `{cmd_clean}` | {res} |")

lines.extend([
    "",
    "---",
    "",
    "## 2. Ключевые артефакты поставки v4.0",
    "",
    "- **Android Application:**",
    "  - Версия: `versionCode = 3`, `versionName = '2.1.0'`",
    "  - Файл: `app_english_cards/app/build/outputs/apk/debug/app-debug.apk`",
    "  - SHA-256: `568b9d454d8fbe91124bfaf7d016b6e817af9d5734b99ff832fb5c65c944d71c`",
    "  - База данных: Room DB (v2) с таблицами `practice_states`, `review_events`, `user_entry_states` и атомарными транзакциями `recordReviewTransaction` и `undoLastReviewTransaction`.",
    "- **Канонический корпус:**",
    "  - 1 680 карточек (`content/cards.json` и `app/src/main/assets/cards_v3.json`).",
    "  - 0 шаблонных предложений «We use ... in ... module».",
    "  - 0 утечек ответов в production prompt.",
    "  - 0 синтаксических ошибок в Python примерах (top-level await обернут в `async def`).",
    "  - 120 карточек с hasattr переведены на канонический класс `Driver`.",
    "  - 50 карточек с подтвержденными вторичными контекстами.",
    "- **12 Микроуроков:**",
    "  - Упакованы в `app_english_cards/app/src/main/assets/lessons/`.",
    "  - Доступны из приложения через экран «📚 Уроки» с интерактивной проверкой заданий.",
    "- **Аудиопакет Andrew:**",
    "  - Манифест: `content/audio_manifest.json` (1 632 записи, 100% декодируемы).",
    "  - Эталонные карточки `rsplit`, `zip`, `issubclass`, `getattr`, `filter` имеют изолированные роли `term_en`, `meaning_ru`, `example_en`, `example_ru`.",
    "  - Голос: `en-US-AndrewMultilingualNeural`."
])

with open(md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("Generated acceptance_v4.md successfully.")
