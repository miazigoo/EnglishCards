"""
Скрипт сборки финального словаря IT / Backend / IoT лексики (1500+ слов).
Объединяет все 18 модулей, убирает дубликаты, сортирует по категориям и
экспортирует в human-readable TXT и structured JSON.
"""

import os
import sys
import json
from collections import defaultdict

sys.path.insert(0, '/home/b00bs/my_less/English/builder_modules')

mods = [
    'mod_python_builtins',
    'mod_django',
    'mod_fastapi_pydantic',
    'mod_backend_verbs',
    'mod_backend_adjectives',
    'mod_backend_nouns',
    'mod_databases_sql',
    'mod_async_celery',
    'mod_http_rest_security',
    'mod_testing_pytest',
    'mod_devops_git_docker',
    'mod_domain_iot',
    'mod_project_extended_1',
    'mod_project_extended_2',
    'mod_project_extended_3',
    'mod_project_extended_4',
    'mod_project_extended_5',
    'mod_project_extended_6'
]

unique_items = {}
for mname in mods:
    m = __import__(mname)
    for item in m.ITEMS:
        # item: (word, cleanTranslation, fullDescription, category, tag)
        norm_w = item[0].lower().strip()
        if norm_w not in unique_items:
            unique_items[norm_w] = item

print(f"Общее количество уникальных отобранных терминов: {len(unique_items)}")

# Группировка по категориям
categories = defaultdict(list)
for norm_w, item in unique_items.items():
    word, clean_tr, full_desc, cat, tag = item
    categories[cat].append({
        "word": word,
        "cleanTranslation": clean_tr,
        "translation": full_desc,
        "category": cat,
        "tag": tag
    })

# Формируем JSON и TXT
json_list = []
txt_lines = [
    "# ==============================================================================",
    "# ПРОФЕССИОНАЛЬНЫЙ СЛОВАРЬ IT, BACKEND, PYTHON, DJANGO, FASTAPI И ПРОМЫШЛЕННОГО IOT",
    f"# Всего отобрано уникальных терминов: {len(unique_items)}",
    "# Источник: проект /home/b00bs/testProgects/devandprod/devandprod_backend",
    "# Для всех методов и спец-функций даны точные практические подсказки их роли в коде.",
    "# ==============================================================================\n"
]

current_id = 1

category_order = [
    "Python: встроенные методы и функции",
    "Django: ORM, модели и QuerySet",
    "FastAPI, Pydantic и валидация",
    "Backend: функции и действия (Verbs)",
    "Backend: свойства, флаги и состояния (Adjectives)",
    "Backend: архитектура, сущности и паттерны (Nouns)",
    "Базы данных, SQL и транзакции",
    "Асинхронность, Celery и очереди задач",
    "HTTP, REST API и безопасность",
    "Тестирование, Mocking и Pytest",
    "Git, Docker, CI/CD и DevOps",
    "Domain: Оборудование, IoT и Маркировка",
    "Сеть, протоколы и передача данных"
]

# Обрабатываем в заданном порядке
for cat in category_order:
    items = categories.get(cat, [])
    if not items:
        continue
    
    txt_lines.append(f"## {cat} ({len(items)} терминов)")
    txt_lines.append("=" * 80)
    
    for entry in items:
        entry["id"] = current_id
        json_list.append(entry)
        
        # Формат: word — cleanTranslation | fullDescription
        txt_lines.append(f"{current_id:04d}. {entry['word']} — {entry['cleanTranslation']} | {entry['translation']}")
        current_id += 1
    
    txt_lines.append("")

# Добавляем оставшиеся категории, если вдруг есть
for cat, items in categories.items():
    if cat in category_order:
        continue
    txt_lines.append(f"## {cat} ({len(items)} терминов)")
    txt_lines.append("=" * 80)
    for entry in items:
        entry["id"] = current_id
        json_list.append(entry)
        txt_lines.append(f"{current_id:04d}. {entry['word']} — {entry['cleanTranslation']} | {entry['translation']}")
        current_id += 1
    txt_lines.append("")

txt_path = "/home/b00bs/my_less/English/backend_words_selection.txt"
json_path = "/home/b00bs/my_less/English/backend_words_selection.json"

with open(txt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(txt_lines))

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(json_list, f, ensure_ascii=False, indent=2)

print(f"Успешно сохранен TXT: {txt_path} ({len(txt_lines)} строк, {os.path.getsize(txt_path):,} байт)")
print(f"Успешно сохранен JSON: {json_path} ({len(json_list)} записей, {os.path.getsize(json_path):,} байт)")
