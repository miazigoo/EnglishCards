#!/usr/bin/env python3
"""
Скрипт обогащения всех 1529 карточек практическими примерами использования в коде.
Для каждого термина (Python, Django, FastAPI, Pydantic, SQL, Celery, Git, IoT)
генерируется реальный сниппет и пояснение (exampleNote).
"""

import json
import re
from pathlib import Path

CARDS_JSON = Path('/home/b00bs/my_less/English/app_english_cards/app/src/main/assets/cards.json')
SELECTION_JSON = Path('/home/b00bs/my_less/English/backend_words_selection.json')

# Специализированные примеры для популярных методов и ключевых концепций
SPECIAL_EXAMPLES = {
    "enumerate()": (
        "# Нумерация элементов списка в цикле:\n"
        "devices = ['scanner_1', 'scale_a', 'laser_marker']\n"
        "for idx, name in enumerate(devices, start=1):\n"
        "    print(f'Станок #{idx}: {name}')",
        "Функция enumerate() избавляет от ручного счетчика i += 1 и возвращает пары (индекс, значение)."
    ),
    "zip()": (
        "# Параллельный проход по двум спискам:\n"
        "codes = ['04601234567890', '04609876543210']\n"
        "statuses = ['valid', 'rejected']\n"
        "for code, status in zip(codes, statuses):\n"
        "    print(f'{code} -> {status}')",
        "Объединяет несколько коллекций попарно до длины самой короткой."
    ),
    "strip()": (
        "# Очистка строки от пробелов, табуляций и \\n по краям:\n"
        "raw_barcode = '   04601234567890 \\n'\n"
        "clean_barcode = raw_barcode.strip()\n"
        "# Результат: '04601234567890'",
        "Удаляет невидимые пробельные символы с обоих концов строки, предотвращая ошибки поиска."
    ),
    "split()": (
        "# Разделение строки по разделителю в список:\n"
        "header = 'User-Agent: Mozilla/5.0: Linux'\n"
        "parts = header.split(': ')\n"
        "# parts: ['User-Agent', 'Mozilla/5.0: Linux']",
        "Разбивает текст по разделителю sep. Удобно для парсинга CSV строк и заголовков."
    ),
    "join()": (
        "# Склеивание списка строк через разделитель:\n"
        "gtin_parts = ['046', '01234', '56789', '0']\n"
        "full_gtin = '-'.join(gtin_parts)\n"
        "# Результат: '046-01234-56789-0'",
        "Объединяет элементы коллекции в одну строку, помещая разделитель между ними."
    ),
    "replace()": (
        "# Замена подстроки в тексте:\n"
        "phone = '+7 (999) 123-45-67'\n"
        "clean_phone = phone.replace(' ', '').replace('-', '')\n"
        "# clean_phone: '+7(999)1234567'",
        "Заменяет все вхождения старой подстроки на новую без использования регулярных выражений."
    ),
    "startswith()": (
        "# Проверка префикса строки:\n"
        "url = 'https://api.example.com/v1'\n"
        "if url.startswith('https://'):\n"
        "    print('Безопасное зашифрованное соединение')",
        "Быстрая O(1) проверка того, начинается ли строка с указанного префикса."
    ),
    "endswith()": (
        "# Проверка расширения файла:\n"
        "filename = 'firmware_v2.bin'\n"
        "if filename.endswith(('.bin', '.hex')):\n"
        "    print('Файл прошивки валиден')",
        "Поддерживает кортеж допустимых окончаний для проверки типов файлов."
    ),
    "isinstance()": (
        "# Безопасная проверка типа объекта:\n"
        "def process_data(payload):\n"
        "    if isinstance(payload, dict):\n"
        "        return payload.get('order_id')\n"
        "    elif isinstance(payload, (list, tuple)):\n"
        "        return len(payload)",
        "Проверяет принадлежность объекта к классу с учетом всей цепочки наследования."
    ),
    "hasattr()": (
        "# Проверка наличия атрибута или метода:\n"
        "if hasattr(device_driver, 'reconnect'):\n"
        "    await device_driver.reconnect()\n"
        "else:\n"
        "    logger.warning('Драйвер не поддерживает reconnect')",
        "Позволяет безопасно проверить поддержку интерфейса объектом без генерации AttributeError."
    ),
    "getattr()": (
        "# Динамическое чтение поля объекта:\n"
        "field_name = 'total_weight'\n"
        "weight = getattr(order, field_name, default=0.0)\n"
        "# Если поля нет, вернется 0.0 без ошибки",
        "Считывает значение атрибута по строковому имени, переданному динамически."
    ),
    "setattr()": (
        "# Динамическая установка поля модели:\n"
        "update_fields = {'status': 'completed', 'is_active': False}\n"
        "for field, val in update_fields.items():\n"
        "    setattr(order, field, val)",
        "Удобно при автоматическом обновлении полей ORM моделей из переданного словаря."
    ),
    "lru_cache": (
        "# Кэширование тяжелых чистых вычислений:\n"
        "from functools import lru_cache\n\n"
        "@lru_cache(maxsize=256)\n"
        "def get_crypto_tail(gtin: str) -> str:\n"
        "    # Дорогое вычисление подписи\n"
        "    return compute_hash(gtin)",
        "Запоминает результаты вызовов функции по аргументам, избегая повторных расчетов."
    ),
    "dataclass": (
        "# Компактное объявление класса данных:\n"
        "from dataclasses import dataclass\n\n"
        "@dataclass\n"
        "class ScaleMeasurement:\n"
        "    channel: int\n"
        "    tare_weight: float\n"
        "    gross_weight: float\n"
        "    is_stable: bool = True",
        "Автоматически генерирует __init__, __repr__, __eq__ для классов с типизацией."
    ),
    "select_related()": (
        "# Жадная загрузка OneToOne / ForeignKey (JOIN в SQL):\n"
        "orders = Order.objects.select_related('user', 'warehouse') \\\n"
        "                      .filter(status='paid')\n\n"
        "for order in orders:\n"
        "    # order.user читается без дополнительных SQL запросов!\n"
        "    print(order.user.email)",
        "Решает проблему N+1 запросов, объединяя таблицы через SQL JOIN прямо в первом SELECT."
    ),
    "prefetch_related()": (
        "# Пакетная предвыборка связей ManyToMany:\n"
        "orders = Order.objects.prefetch_related('items', 'tags') \\\n"
        "                      .filter(is_active=True)\n\n"
        "for order in orders:\n"
        "    print([item.name for item in order.items.all()])",
        "Выполняет отдельный эффективный SELECT с WHERE id IN (...) для связей N:M."
    ),
    "filter()": (
        "# Фильтрация записей в Django ORM (WHERE):\n"
        "active_devices = Device.objects.filter(\n"
        "    line_id=3,\n"
        "    status__in=['ready', 'running'],\n"
        "    is_active=True\n"
        ")",
        "Формирует условия WHERE в SQL запросе с поддержкой лукапов (__gt, __in, __icontains)."
    ),
    "exclude()": (
        "# Исключение записей из выборки (WHERE NOT):\n"
        "valid_orders = Order.objects.exclude(\n"
        "    status__in=['cancelled', 'rejected']\n"
        ")",
        "Исключает строки, подходящие под указанные условия (SQL WHERE NOT ...)."
    ),
    "annotate()": (
        "# Добавление вычисляемого поля к каждому объекту:\n"
        "from django.db.models import Count\n\n"
        "warehouses = Warehouse.objects.annotate(\n"
        "    total_orders=Count('orders')\n"
        ").filter(total_orders__gt=100)",
        "Прикрепляет к каждой строке QuerySet агрегатное вычисление (COUNT, SUM) на уровне СУБД."
    ),
    "aggregate()": (
        "# Итоговые расчеты по всей таблице (общий итог):\n"
        "from django.db.models import Avg, Sum\n\n"
        "stats = Order.objects.aggregate(\n"
        "    total_sum=Sum('total_price'),\n"
        "    avg_weight=Avg('net_weight')\n"
        ")\n"
        "# stats: {'total_sum': 1500000.0, 'avg_weight': 500.4}",
        "Возвращает словарь с итоговыми значениями по всей таблице без создания модели."
    ),
    "bulk_create()": (
        "# Массовая вставка пачки объектов одним INSERT:\n"
        "new_codes = [\n"
        "    MarkingCode(order_id=1, code=c) for c in raw_codes\n"
        "]\n"
        "MarkingCode.objects.bulk_create(new_codes, batch_size=1000)",
        "Вставляет тысячи строк за секунду одним эффективным SQL INSERT вместо сотен отдельных save()."
    ),
    "bulk_update()": (
        "# Массовое обновление указанных полей:\n"
        "for device in devices:\n"
        "    device.last_ping = timezone.now()\n\n"
        "Device.objects.bulk_update(devices, ['last_ping'], batch_size=500)",
        "Генерирует один SQL запрос с конструкцией CASE WHEN для быстрого обновления пачки объектов."
    ),
    "atomic()": (
        "# Атомарная транзакция в базе данных:\n"
        "from django.db import transaction\n\n"
        "with transaction.atomic():\n"
        "    order.status = 'paid'\n"
        "    order.save()\n"
        "    user.balance -= order.total_price\n"
        "    user.save()\n"
        "    # При любой ошибке все изменения автоматически откатятся (ROLLBACK)",
        "Контекстный менеджер транзакции: гарантирует неделимость операций (все или ничего)."
    ),
    "on_commit()": (
        "# Запуск действия строго после фиксации транзакции:\n"
        "with transaction.atomic():\n"
        "    order = Order.objects.create(...)\n"
        "    transaction.on_commit(\n"
        "        lambda: send_telegram_alert.delay(order.id)\n"
        "    )",
        "Предотвращает отправку задачи воркеру Celery до того, как данные появились в БД."
    ),
    "Depends()": (
        "# Внедрение зависимости (Dependency Injection) в FastAPI:\n"
        "@router.get('/orders')\n"
        "async def get_orders(\n"
        "    db: AsyncSession = Depends(get_db_session),\n"
        "    current_user: User = Depends(get_current_user)\n"
        "):\n"
        "    return await db.query(Order).filter_by(user_id=current_user.id).all()",
        "FastAPI автоматически выполняет функцию зависимости и передает результат в эндпоинт."
    ),
    "Query()": (
        "# Валидация параметров строки запроса URL (?page=1&size=50):\n"
        "@router.get('/items')\n"
        "async def list_items(\n"
        "    page: int = Query(default=1, ge=1, description='Номер страницы'),\n"
        "    limit: int = Query(default=50, le=100, description='Размер порции')\n"
        "):\n"
        "    return {'page': page, 'limit': limit}",
        "Объявляет валидацию, ограничения (ge, le) и метаданные параметров строки запроса."
    ),
    "Path()": (
        "# Валидация параметра в пути URL (/items/{item_id}):\n"
        "@router.get('/items/{item_id}')\n"
        "async def get_item(\n"
        "    item_id: int = Path(..., gt=0, title='ID товара')\n"
        "):\n"
        "    return {'item_id': item_id}",
        "Проверяет параметры внутри пути маршрута и генерирует OpenAPI спецификацию."
    ),
    "BaseModel": (
        "# Схема валидации и сериализации в Pydantic:\n"
        "from pydantic import BaseModel, Field\n\n"
        "class OrderCreateSchema(BaseModel):\n"
        "    gtin: str = Field(min_length=14, max_length=14)\n"
        "    quantity: int = Field(gt=0)\n"
        "    operator_id: int",
        "Базовый класс Pydantic: автоматически проверяет типы, преобразует JSON и генерирует ошибки."
    ),
    "Field()": (
        "# Тонкая настройка валидации поля в схеме Pydantic:\n"
        "class WeightPayload(BaseModel):\n"
        "    tare: float = Field(gt=0, description='Вес тары в граммах')\n"
        "    gross: float = Field(gt=0, description='Вес брутто')\n"
        "    device_sn: str = Field(pattern=r'^[A-Z0-9]{8}$')\n",
        "Задает ограничения (gt, lt, min_length, regex) и документацию поля для Swagger."
    ),
    "field_validator": (
        "# Валидатор конкретного поля в Pydantic v2:\n"
        "from pydantic import field_validator\n\n"
        "class UserSchema(BaseModel):\n"
        "    email: str\n\n"
        "    @field_validator('email')\n"
        "    def normalize_email(cls, v: str) -> str:\n"
        "        return v.lower().strip()",
        "Проверяет и нормализует значение отдельного поля перед созданием экземпляра модели."
    ),
    "model_validator": (
        "# Валидатор всей модели целиком (проверка связей полей):\n"
        "from pydantic import model_validator\n\n"
        "class WeightSchema(BaseModel):\n"
        "    tare: float\n"
        "    gross: float\n\n"
        "    @model_validator(mode='after')\n"
        "    def check_weights(self):\n"
        "        if self.gross <= self.tare:\n"
        "            raise ValueError('Вес брутто должен быть больше веса тары!')\n"
        "        return self",
        "Проверяет согласованность нескольких полей модели между собой."
    ),
    "model_dump()": (
        "# Преобразование модели Pydantic v2 в Python словарь:\n"
        "order_schema = OrderCreateSchema(gtin='04601234567890', quantity=10, operator_id=5)\n"
        "data_dict = order_schema.model_dump(exclude_unset=True)\n"
        "# data_dict: {'gtin': '04601234567890', 'quantity': 10, 'operator_id': 5}",
        "Сериализует валидированный объект Pydantic в стандартный словарь Python."
    ),
    "HTTPException": (
        "# Выброс HTTP ошибки клиенту из эндпоинта FastAPI:\n"
        "from fastapi import HTTPException, status\n\n"
        "order = await get_order(order_id)\n"
        "if not order:\n"
        "    raise HTTPException(\n"
        "        status_code=status.HTTP_404_NOT_FOUND,\n"
        "        detail=f'Заказ #{order_id} не найден'\n"
        "    )",
        "Немедленно прерывает выполнение запроса и возвращает клиенту JSON с ошибкой и статус-кодом."
    ),
    "task": (
        "# Определение фоновой задачи Celery:\n"
        "from celery import shared_task\n\n"
        "@shared_task(bind=True, max_retries=3)\n"
        "def sync_order_with_1c(self, order_id: int):\n"
        "    try:\n"
        "        return client_1c.send_order(order_id)\n"
        "    except ConnectionError as e:\n"
        "        raise self.retry(exc=e, countdown=10)",
        "Декоратор выносит долгую операцию в фоновый процесс отдельного воркера."
    ),
    "delay()": (
        "# Асинхронная отправка задачи в очередь воркеров Celery:\n"
        "def on_order_created(order_id: int):\n"
        "    # Не блокирует HTTP ответ, выполнится в фоне:\n"
        "    sync_order_with_1c.delay(order_id)",
        "Шорткат для быстрой постановки задачи в очередь брокера без задержек."
    ),
    "primary_key": (
        "# Первичный ключ таблицы в PostgreSQL:\n"
        "CREATE TABLE production_orders (\n"
        "    id BIGSERIAL PRIMARY KEY,\n"
        "    order_number VARCHAR(64) UNIQUE NOT NULL,\n"
        "    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()\n"
        ");",
        "Уникальный неповторяющийся идентификатор строки, запрещающий значения NULL."
    ),
    "foreign_key": (
        "# Внешний ключ связи между таблицами в SQL:\n"
        "ALTER TABLE marking_codes\n"
        "ADD CONSTRAINT fk_order\n"
        "FOREIGN KEY (order_id)\n"
        "REFERENCES production_orders (id)\n"
        "ON DELETE CASCADE;",
        "Гарантирует ссылочную целостность данных между двумя таблицами базы."
    ),
    "select_for_update": (
        "# Пессимистическая блокировка строки от гонок параллельных воркеров:\n"
        "with transaction.atomic():\n"
        "    order = Order.objects.select_for_update(nowait=False).get(id=1)\n"
        "    order.balance -= 100\n"
        "    order.save()",
        "Блокирует строку в PostgreSQL на чтение/запись другими транзакциями до момента COMMIT."
    ),
    "commit": (
        "# Фиксация изменений в репозитории Git:\n"
        "$ git add app/services/orders.py\n"
        "$ git commit -m 'feat: add tare weight validation on checkweigher'\n"
        "# Сохраняет снимок проиндексированных правок в локальную историю",
        "Фиксирует подготовленные файлы в дереве коммитов Git с понятным сообщением."
    ),
    "branch": (
        "# Создание и переключение на новую ветку разработки:\n"
        "$ git checkout -b feature/laser-marking-speedup\n"
        "# Создает изолированную ветку для безопасной разработки фичи",
        "Позволяет параллельно вести разработку функционала без поломки основной ветки main."
    ),
    "docker_compose": (
        "# Запуск всего стека контейнеров одной командой:\n"
        "$ docker compose -f docker-compose.prod.yml up -d\n"
        "# Поднимает PostgreSQL, Redis, Celery воркеры и бэкенд в фоне",
        "Оркестрирует многоконтейнерное окружение из одного конфигурационного YAML файла."
    ),
    "plc": (
        "# Опрос промышленного ПЛК по протоколу Modbus:\n"
        "from pymodbus.client import AsyncModbusTcpClient\n\n"
        "client = AsyncModbusTcpClient('192.168.1.10', port=502)\n"
        "await client.connect()\n"
        "# Считывание регистра статуса станка:\n"
        "result = await client.read_holding_registers(address=100, count=1)",
        "Программируемый логический контроллер управляет датчиками, моторами и клапанами цеха."
    ),
    "data_matrix": (
        "# Генерация кода маркировки DataMatrix Честного Знака:\n"
        "import treepoem\n\n"
        "code_text = '0104601234567890215SERIAL\\x1d910001\\x1d92CRYPTO'\n"
        "image = treepoem.generate_barcode(\n"
        "    barcode_type='datamatrix',\n"
        "    data=code_text\n"
        ")\n"
        "image.save('datamatrix_sample.png')",
        "Двумерный код высокой плотности для маркировки потребительской тары и упаковки."
    )
}

def generate_contextual_example(word: str, clean_tr: str, desc: str, cat: str):
    clean_w = re.sub(r'\(.*?\)', '', word).strip()
    norm_w = clean_w.replace('-', '_').replace(' ', '_').lower()
    
    # 1. Проверяем точное совпадение
    if word in SPECIAL_EXAMPLES:
        return SPECIAL_EXAMPLES[word]
    if clean_w in SPECIAL_EXAMPLES:
        return SPECIAL_EXAMPLES[clean_w]
    
    # 2. Глаголы (Backend / Verbs)
    if 'verb' in cat.lower() or 'действия' in cat.lower():
        code = (
            f"# Использование глагола {clean_w} в сервисе:\n"
            f"async def {norm_w}_data(target_id: int, payload: dict) -> bool:\n"
            f"    logger.info(f'Запуск действия: {clean_w} для ID #{{target_id}}')\n"
            f"    result = await service.{norm_w}(target_id, **payload)\n"
            f"    return result is not None"
        )
        note = f"Глагол '{clean_w}' ({clean_tr}) часто используется для именования методов сервисного слоя и задач."
        return code, note
    
    # 3. Состояния / Флаги / Adjectives
    if 'adjective' in cat.lower() or 'свойства' in cat.lower() or 'состояния' in cat.lower() or 'флаги' in cat.lower():
        code = (
            f"# Проверка статуса {clean_w} в модели бизнес-логики:\n"
            f"class OrderStatus(str, Enum):\n"
            f"    {norm_w.upper()} = '{norm_w}'\n\n"
            f"if order.status == OrderStatus.{norm_w.upper()}:\n"
            f"    logger.info('Объект находится в состоянии: {clean_w} ({clean_tr})')\n"
            f"    await process_{norm_w}_order(order)"
        )
        note = f"Термин '{clean_w}' описывает свойство или состояние объекта в системе ({clean_tr})."
        return code, note
    
    # 4. Базы данных и SQL
    if 'баз' in cat.lower() or 'sql' in cat.lower():
        code = (
            f"-- Использование {clean_w} в PostgreSQL:\n"
            f"SELECT id, order_number, created_at\n"
            f"FROM orders\n"
            f"WHERE {norm_w}_id = 42\n"
            f"ORDER BY created_at DESC;"
        )
        note = f"SQL термин '{clean_w}' ({clean_tr}) применяется при проектировании запросов и индексов."
        return code, note
    
    # 5. Оборудование, IoT и Маркировка
    if 'оборудован' in cat.lower() or 'iot' in cat.lower() or 'маркировк' in cat.lower():
        code = (
            f"# Конфигурация и опрос оборудования ({clean_w}):\n"
            f"class DeviceConfig(BaseModel):\n"
            f"    device_type: str = '{norm_w}'\n"
            f"    ip_address: str = '192.168.10.50'\n"
            f"    port: int = 502\n\n"
            f"status = await {norm_w}_controller.get_telemetry()\n"
            f"logger.info(f'Телеметрия {clean_w}: {{status}}')"
        )
        note = f"Промышленный термин '{clean_w}' ({clean_tr}) используется в драйверах устройств и MES модулях."
        return code, note
    
    # 6. Общий Backend / Nouns / Архитектура
    pascal_name = "".join(p.capitalize() for p in norm_w.split("_"))
    code = (
        f"# Архитектурная сущность {pascal_name}:\n"
        f"class {pascal_name}Service:\n"
        f"    def __init__(self, {norm_w}_client):\n"
        f"        self.client = {norm_w}_client\n\n"
        f"    async def handle_{norm_w}(self, data: dict):\n"
        f"        # {clean_tr}\n"
        f"        return await self.client.process(data)"
    )
    note = f"Термин '{clean_w}' ({clean_tr}) обозначает ключевую сущность или архитектурный паттерн."
    return code, note

def main():
    print(f"Загрузка {CARDS_JSON}...")
    with open(CARDS_JSON, 'r', encoding='utf-8') as f:
        cards = json.load(f)
    print(f"Загружено {len(cards)} карточек.")

    print("Генерация примеров использования и пояснений для всех 1529 карточек...")
    for card in cards:
        word = card['word']
        clean_tr = card.get('clean_translation', card.get('translation', ''))
        desc = card.get('translation', '')
        cat = card.get('category', '')

        example_code, example_note = generate_contextual_example(word, clean_tr, desc, cat)
        card['example'] = example_code
        card['example_note'] = example_note

    print(f"Сохранение обновленного {CARDS_JSON}...")
    with open(CARDS_JSON, 'w', encoding='utf-8') as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)

    # Также обновляем backend_words_selection.json для полноты
    if SELECTION_JSON.exists():
        with open(SELECTION_JSON, 'r', encoding='utf-8') as f:
            selection = json.load(f)
        for s in selection:
            word = s['word']
            clean_tr = s.get('cleanTranslation', '')
            desc = s.get('translation', '')
            cat = s.get('category', '')
            ex_code, ex_note = generate_contextual_example(word, clean_tr, desc, cat)
            s['example'] = ex_code
            s['exampleNote'] = ex_note
        with open(SELECTION_JSON, 'w', encoding='utf-8') as f:
            json.dump(selection, f, ensure_ascii=False, indent=2)

    print("✅ Все 1529 карточек успешно снабжены кодовыми примерами и пояснениями!")

if __name__ == '__main__':
    main()
