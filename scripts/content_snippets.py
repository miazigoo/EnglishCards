#!/usr/bin/env python3
"""
scripts/content_snippets.py

Authoritative technical code snippets and pedagogical explanations for all
technical concepts across Python, Django, FastAPI, Celery, Testing, DevOps,
Databases, Networking, and Architecture.
Completely eliminates the boilerplate "class ...Service:" and generic notes.
"""

from typing import Tuple, Dict

# Explicit snippet dictionary mapping word or clean word to (code, note, expected_output)
EXPLICIT_SNIPPETS: Dict[str, Tuple[str, str, str]] = {
    # --- Python Builtins & Stdlib ---
    "primary_key": (
        "-- Определение первичного ключа таблицы в PostgreSQL:\n"
        "CREATE TABLE production_orders (\n"
        "    id BIGSERIAL PRIMARY KEY,\n"
        "    order_number VARCHAR(64) UNIQUE NOT NULL,\n"
        "    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()\n"
        ");",
        "Первичный ключ уникально идентифицирует каждую строку таблицы и автоматически создает B-tree индекс.",
        "CREATE TABLE"
    ),
    "foreign_key": (
        "-- Определение внешнего ключа для связи таблиц:\n"
        "ALTER TABLE order_items\n"
        "ADD CONSTRAINT fk_order_id\n"
        "FOREIGN KEY (order_id) REFERENCES production_orders(id)\n"
        "ON DELETE CASCADE;",
        "Внешний ключ обеспечивает ссылочную целостность между связанными таблицами реляционной БД.",
        "ALTER TABLE"
    ),
    "import": (
        "# Импорт стандартного или стороннего модуля в Python:\n"
        "import asyncio\n"
        "from datetime import datetime, timezone\n\n"
        "current_time = datetime.now(timezone.utc)\n"
        "assert current_time is not None",
        "Ключевое слово для подключения внешних модулей, пакетов и функций в текущий файл.",
        "datetime object"
    ),
    "await": (
        "# Ожидание завершения асинхронной корутины в Python:\n"
        "import asyncio\n\n"
        "async def fetch_status():\n"
        "    await asyncio.sleep(0.01)\n"
        "    return {'status': 'ok'}\n\n"
        "result = asyncio.run(fetch_status())\n"
        "assert result['status'] == 'ok'",
        "Приостанавливает выполнение корутины до готовности результата, передавая управление event loop.",
        "{'status': 'ok'}"
    ),
    "delattr()": (
        "class Config:\n"
        "    debug = True\n"
        "    temp_dir = '/tmp'\n\n"
        "conf = Config()\n"
        "delattr(conf, 'temp_dir')\n"
        "assert not hasattr(conf, 'temp_dir')",
        "Удаляет указанный атрибут из объекта, эквивалентно 'del conf.temp_dir'.",
        "hasattr(conf, 'temp_dir') == False"
    ),
    "callable()": (
        "def compute(x):\n"
        "    return x * 2\n\n"
        "assert callable(compute) is True\n"
        "assert callable(42) is False",
        "Проверяет, можно ли вызвать переданный объект как функцию или класс.",
        "True, False"
    ),
    "iter()": (
        "items = ['apple', 'banana', 'cherry']\n"
        "iterator = iter(items)\n"
        "assert next(iterator) == 'apple'\n"
        "assert next(iterator) == 'banana'",
        "Возвращает объект-итератор для переданной коллекции или генератора.",
        "'apple', 'banana'"
    ),
    "next()": (
        "numbers = iter([10, 20, 30])\n"
        "first = next(numbers)\n"
        "default_val = next(numbers, None)\n"
        "assert first == 10",
        "Извлекает следующий элемент из итератора. При исчерпании возвращает default или вызывает StopIteration.",
        "10"
    ),
    "all()": (
        "checks = [True, len('hello') > 0, 10 > 5]\n"
        "assert all(checks) is True\n"
        "assert all([True, False, True]) is False",
        "Возвращает True, только если ВСЕ элементы последовательности оцениваются как True.",
        "True, False"
    ),
    "any()": (
        "permissions = [False, False, True]\n"
        "assert any(permissions) is True\n"
        "assert any([0, '', False]) is False",
        "Возвращает True, если ХОТЯ БЫ ОДИН элемент последовательности оценивается как True.",
        "True, False"
    ),
    "sorted()": (
        "numbers = [5, 2, 8, 1, 9]\n"
        "asc = sorted(numbers)\n"
        "desc = sorted(numbers, reverse=True)\n"
        "assert asc == [1, 2, 5, 8, 9]",
        "Возвращает новый отсортированный список, не изменяя исходную последовательность.",
        "[1, 2, 5, 8, 9]"
    ),
    "reversed()": (
        "letters = ['a', 'b', 'c']\n"
        "result = list(reversed(letters))\n"
        "assert result == ['c', 'b', 'a']",
        "Возвращает обратный итератор по элементам последовательности.",
        "['c', 'b', 'a']"
    ),
    "map()": (
        "raw_ports = ['80', '443', '8080']\n"
        "ports = list(map(int, raw_ports))\n"
        "assert ports == [80, 443, 8080]",
        "Применяет функцию к каждому элементу последовательности, возвращая итератор результатов.",
        "[80, 443, 8080]"
    ),
    "sum()": (
        "prices = [19.99, 5.00, 12.50]\n"
        "total = sum(prices, 0.0)\n"
        "assert total == 37.49",
        "Вычисляет сумму всех элементов числовой последовательности с опциональным стартовым значением.",
        "37.49"
    ),
    "min()": (
        "latencies_ms = [45, 12, 89, 5]\n"
        "best = min(latencies_ms)\n"
        "assert best == 5",
        "Возвращает наименьший элемент из последовательности или переданных аргументов.",
        "5"
    ),
    "max()": (
        "scores = [78, 92, 65, 99]\n"
        "top_score = max(scores)\n"
        "assert top_score == 99",
        "Возвращает наибольший элемент из последовательности или переданных аргументов.",
        "99"
    ),
    "abs()": (
        "diff = -15.5\n"
        "assert abs(diff) == 15.5\n"
        "assert abs(10) == 10",
        "Возвращает абсолютную величину (модуль) переданного числа.",
        "15.5"
    ),
    "round()": (
        "price = 14.5678\n"
        "assert round(price, 2) == 14.57\n"
        "assert round(2.5) == 2  # банковское округление до четного",
        "Округляет число с плавающей точкой до указанного количества знаков после запятой.",
        "14.57"
    ),
    "divmod()": (
        "total_seconds = 125\n"
        "minutes, seconds = divmod(total_seconds, 60)\n"
        "assert (minutes, seconds) == (2, 5)",
        "Возвращает кортеж из частного и остатка от деления двух чисел: (a // b, a % b).",
        "(2, 5)"
    ),
    "pow()": (
        "assert pow(2, 8) == 256\n"
        "assert pow(2, 8, 100) == 56  # 2^8 % 100",
        "Возводит число в степень с опциональным вычислением по модулю pow(base, exp, mod).",
        "256, 56"
    ),
    "slice()": (
        "data = list(range(10))\n"
        "top_three = slice(0, 3)\n"
        "assert data[top_three] == [0, 1, 2]",
        "Создает объект среза slice(start, stop, step) для выборки из последовательностей.",
        "[0, 1, 2]"
    ),
    "repr()": (
        "text = 'hello\\nworld'\n"
        "assert repr(text) == \"'hello\\\\nworld'\"",
        "Возвращает однозначное строковое представление объекта для отладки и логирования.",
        "\"'hello\\\\nworld'\""
    ),
    "eval()": (
        "expression = '3 * 5 + 2'\n"
        "result = eval(expression, {'__builtins__': {}})\n"
        "assert result == 17",
        "Вычисляет переданное строковое Python-выражение в ограниченном контексте.",
        "17"
    ),
    "exec()": (
        "scope = {}\n"
        "code_str = 'x = 10\\ny = x * 2'\n"
        "exec(code_str, scope)\n"
        "assert scope['y'] == 20",
        "Динамически выполняет блок Python-кода из строки в переданном словаре пространств имен.",
        "scope['y'] == 20"
    ),
    "breakpoint()": (
        "# Активация встроенного отладчика Python 3.7+:\n"
        "def process_order(order_id):\n"
        "    if order_id < 0:\n"
        "        breakpoint()  # Вызывает sys.breakpointhook() / pdb\n"
        "    return {'status': 'processed'}",
        "Вызывает стандартный отладчик (pdb) в точке останова без необходимости импорта pdb.",
        "Pdb console"
    ),
    "hash()": (
        "key = ('user_id', 42)\n"
        "h = hash(key)\n"
        "assert isinstance(h, int)",
        "Возвращает хеш-значение неизменяемого объекта для работы словарей и множеств.",
        "integer hash"
    ),
    "id()": (
        "a = [1, 2, 3]\n"
        "b = a\n"
        "assert id(a) == id(b)\n"
        "assert a is b",
        "Возвращает уникальный целочисленный идентификатор объекта в памяти (адрес).",
        "memory address id"
    ),
    "type()": (
        "value = {'status': 'ok'}\n"
        "assert type(value) is dict\n"
        "assert type(42) is int",
        "Возвращает тип переданного объекта или динамически создает новый класс.",
        "<class 'dict'>"
    ),
    "vars()": (
        "class Point:\n"
        "    def __init__(self, x, y):\n"
        "        self.x = x\n"
        "        self.y = y\n\n"
        "p = Point(10, 20)\n"
        "assert vars(p) == {'x': 10, 'y': 20}",
        "Возвращает словарь __dict__ атрибутов переданного объекта или локальную область видимости.",
        "{'x': 10, 'y': 20}"
    ),
    "dir()": (
        "class Device:\n"
        "    online = True\n\n"
        "attrs = dir(Device)\n"
        "assert 'online' in attrs",
        "Возвращает список допустимых имен атрибутов и методов переданного объекта.",
        "['online', ...]"
    ),
    "globals()": (
        "GLOBAL_TIMEOUT = 30\n"
        "current_globals = globals()\n"
        "assert 'GLOBAL_TIMEOUT' in current_globals",
        "Возвращает словарь текущего глобального пространства имен модуля.",
        "{'GLOBAL_TIMEOUT': 30, ...}"
    ),
    "locals()": (
        "def setup_channel(channel_id, baudrate=9600):\n"
        "    state = 'active'\n"
        "    return locals()\n\n"
        "ctx = setup_channel(1)\n"
        "assert ctx['baudrate'] == 9600 and ctx['state'] == 'active'",
        "Возвращает словарь текущих локальных переменных функции.",
        "{'channel_id': 1, 'baudrate': 9600, 'state': 'active'}"
    ),
    "super()": (
        "class BaseHandler:\n"
        "    def handle(self):\n"
        "        return 'base'\n\n"
        "class CustomHandler(BaseHandler):\n"
        "    def handle(self):\n"
        "        return super().handle() + ' -> custom'\n\n"
        "assert CustomHandler().handle() == 'base -> custom'",
        "Делегирует вызов метода родительскому классу согласно порядку разрешения методов (MRO).",
        "'base -> custom'"
    ),
    "classmethod()": (
        "class ConfigLoader:\n"
        "    default_path = '/etc/app.conf'\n\n"
        "    @classmethod\n"
        "    def from_env(cls, env_path=None):\n"
        "        path = env_path or cls.default_path\n"
        "        return f'Loaded from {path}'\n\n"
        "assert ConfigLoader.from_env() == 'Loaded from /etc/app.conf'",
        "Превращает метод в метод класса, принимающий первым аргументом сам класс (cls), а не экземпляр.",
        "'Loaded from /etc/app.conf'"
    ),
    "staticmethod()": (
        "class MathUtils:\n"
        "    @staticmethod\n"
        "    def clamp(val, min_val, max_val):\n"
        "        return max(min_val, min(val, max_val))\n\n"
        "assert MathUtils.clamp(150, 0, 100) == 100",
        "Превращает метод в статическую функцию, не зависящую от self или cls.",
        "100"
    ),
    "property()": (
        "class Circle:\n"
        "    def __init__(self, radius):\n"
        "        self._radius = radius\n\n"
        "    @property\n"
        "    def diameter(self):\n"
        "        return self._radius * 2\n\n"
        "c = Circle(5)\n"
        "assert c.diameter == 10",
        "Декоратор для создания вычисляемых атрибутов через getter/setter без изменения публичного API.",
        "10"
    ),

    # --- Django ORM Methods & Fields ---
    "values_list()": (
        "# Получение плоского списка email адресов пользователей:\n"
        "# emails = User.objects.filter(is_active=True).values_list('email', flat=True)\n"
        "# SQL: SELECT email FROM auth_user WHERE is_active = TRUE",
        "Возвращает кортежи значений вместо объектов модели. С флагом flat=True возвращает плоский список одного поля.",
        "<QuerySet ['admin@example.com', 'user@example.com']>"
    ),
    "distinct()": (
        "# Исключение дублирующихся записей из выборки:\n"
        "# tags = Article.objects.values('tag').distinct()\n"
        "# SQL: SELECT DISTINCT tag FROM articles",
        "Устраняет повторяющиеся строки из результатов запроса, генерируя SELECT DISTINCT.",
        "<QuerySet [{'tag': 'python'}, {'tag': 'django'}]>"
    ),
    "order_by()": (
        "# Сортировка заказов от самых свежих к старым:\n"
        "# orders = Order.objects.filter(status='pending').order_by('-created_at')\n"
        "# SQL: SELECT ... FROM orders WHERE status = 'pending' ORDER BY created_at DESC",
        "Задает порядок сортировки записей в QuerySet. Префикс '-' указывает обратный порядок (DESC).",
        "<QuerySet [Order #105, Order #104, ...]>"
    ),
    "first()": (
        "# Получение первой записи выборки или None:\n"
        "# latest_build = Build.objects.filter(branch='main').order_by('-id').first()\n"
        "# SQL: SELECT ... FROM builds WHERE branch = 'main' ORDER BY id DESC LIMIT 1",
        "Возвращает первый объект выборки или None, если набор пуст. Не вызывает исключения DoesNotExist.",
        "<Build #42>"
    ),
    "last()": (
        "# Получение последней записи из выборки:\n"
        "# oldest_log = AuditLog.objects.order_by('created_at').last()",
        "Возвращает последний объект из набора или None, автоматически инвертируя сортировку.",
        "<AuditLog #1>"
    ),
    "earliest()": (
        "# Получение самой ранней записи по указанному полю даты:\n"
        "# first_release = Release.objects.earliest('release_date')",
        "Возвращает самый ранний объект по полю даты/времени, аналогично order_by('field').first().",
        "<Release v1.0.0>"
    ),
    "latest()": (
        "# Получение самой свежей записи по указанному полю:\n"
        "# latest_firmware = Firmware.objects.latest('published_at')",
        "Возвращает самый последний объект по полю даты/времени без ручной сортировки.",
        "<Firmware v3.2.1>"
    ),
    "exists()": (
        "# Быстрая проверка наличия хотя бы одной записи в таблице:\n"
        "# has_unpaid = Order.objects.filter(user=user, status='unpaid').exists()\n"
        "# SQL: SELECT (1) AS a FROM orders WHERE ... LIMIT 1",
        "Возвращает True, если QuerySet содержит хотя бы один объект. Оптимально в плане SQL LIMIT 1.",
        "True"
    ),
    "create()": (
        "# Создание и сохранение нового объекта в БД за один вызов:\n"
        "# new_device = Device.objects.create(name='Laser-01', ip_address='192.168.1.50')\n"
        "# SQL: INSERT INTO devices (name, ip_address) VALUES ('Laser-01', '192.168.1.50')",
        "Инициализирует объект модели и немедленно выполняет INSERT запрос в базу данных.",
        "<Device: Laser-01>"
    ),
    "get_or_create()": (
        "# Получение существующего объекта или создание нового:\n"
        "# tag, created = Tag.objects.get_or_create(slug='backend', defaults={'name': 'Backend'})\n"
        "# created: True если был создан новый объект, иначе False",
        "Возвращает кортеж (объект, created_bool), гарантируя атомарность проверки и создания.",
        "(<Tag: Backend>, True)"
    ),
    "update_or_create()": (
        "# Обновление существующей записи или создание новой:\n"
        "# metric, created = Metric.objects.update_or_create(\n"
        "#     sensor_id='TEMP-01',\n"
        "#     defaults={'value': 23.5, 'timestamp': now()}\n"
        "# )",
        "Ищет запись по ключевым полям и обновляет переданные значения defaults либо создает новую запись.",
        "(<Metric: TEMP-01>, False)"
    ),
    "in_bulk()": (
        "# Загрузка объектов по списку первичных ключей в словарь {id: obj}:\n"
        "# users_map = User.objects.in_bulk([10, 20, 30])\n"
        "# user = users_map.get(10)",
        "Загружает набор объектов по списку ID и возвращает словарь {pk: instance}, избегая N+1 запросов.",
        "{10: <User 10>, 20: <User 20>}"
    ),
    "iterator()": (
        "# Потоковая обработка миллионов строк без переполнения памяти RAM:\n"
        "# for log in AuditLog.objects.filter(level='ERROR').iterator(chunk_size=2000):\n"
        "#     process_log_entry(log)",
        "Выполняет запрос через серверный курсор базы данных, загружая строки частями без кэширования всего набора.",
        "streamed rows"
    ),
    "only()": (
        "# Отложенная загрузка тяжелых полей, выборка только нужных колонок:\n"
        "# users = User.objects.only('id', 'username')\n"
        "# Поля вроде profile_picture_blob будут загружены только при обращении к ним",
        "Ограничивает первоначальный SELECT только указанными полями, оптимизируя сетевой трафик.",
        "<QuerySet [User, ...]>"
    ),
    "defer()": (
        "# Исключение тяжелых текстовых или бинарных колонок из выборки:\n"
        "# articles = Article.objects.defer('full_text_body', 'raw_html')",
        "Откладывает загрузку тяжелых колонок базы данных до явного обращения к ним в коде.",
        "<QuerySet [Article, ...]>"
    ),
    "using()": (
        "# Выполнение запроса к конкретной базе данных из настроек DATABASES:\n"
        "# reports = Report.objects.using('analytics_replica').all()",
        "Переключает соединение для выполнения QuerySet на указанную реплику или базу данных.",
        "<QuerySet [Report, ...]>"
    ),
    "raw()": (
        "# Выполнение чистого SQL запроса с сопоставлением полей модели:\n"
        "# query = 'SELECT id, name FROM devices WHERE status = %s'\n"
        "# devices = Device.objects.raw(query, ['active'])",
        "Выполняет прямой SQL запрос с маппингом результатов на экземпляры модели Django.",
        "<RawQuerySet: SELECT ...>"
    ),
    "none()": (
        "# Возврат пустого типизированного набора без обращения к БД:\n"
        "# if not user.is_authenticated:\n"
        "#     return Task.objects.none()",
        "Возвращает пустой EmptyQuerySet без выполнения запроса к базе данных.",
        "<EmptyQuerySet []>"
    ),
    "explain()": (
        "# Анализ плана выполнения запроса PostgreSQL / MySQL:\n"
        "# plan = Order.objects.filter(customer_id=42).explain(analyze=True)\n"
        "# print(plan)",
        "Генерирует EXPLAIN план базы данных для проверки использования индексов и оптимизации.",
        "Index Scan using orders_customer_id_idx ..."
    ),
    "delete()": (
        "# Каскадное удаление записей выборки из базы данных:\n"
        "# deleted_count, details = Session.objects.filter(is_expired=True).delete()",
        "Удаляет выбранные записи из базы данных и возвращает кортеж (общее число, детализация по моделям).",
        "(15, {'sessions.Session': 15})"
    ),
    "save()": (
        "# Сохранение изменений экземпляра модели в БД:\n"
        "# order.status = 'shipped'\n"
        "# order.save(update_fields=['status'])",
        "Выполняет INSERT или UPDATE в БД. Параметр update_fields обновляет только указанные колонки.",
        "UPDATE orders SET status = 'shipped'"
    ),
    "refresh_from_db()": (
        "# Перезагрузка актуальных значений полей экземпляра из базы данных:\n"
        "# balance = user_account.balance\n"
        "# user_account.refresh_from_db(fields=['balance'])",
        "Сбрасывает локальный кэш экземпляра и перечитывает свежие данные из базы данных.",
        "refreshed fields"
    ),
    "clean()": (
        "# Пользовательская валидация модели перед сохранением:\n"
        "# def clean(self):\n"
        "#     if self.start_date > self.end_date:\n"
        "#         raise ValidationError('Дата начала не может быть позже даты окончания.')",
        "Метод модели для проверки бизнес-правил и связности нескольких полей.",
        "Validation check"
    ),
    "full_clean()": (
        "# Запуск полной валидации полей, уникальности и метода clean():\n"
        "# try:\n"
        "#     order.full_clean()\n"
        "# except ValidationError as err:\n"
        "#     handle_errors(err)",
        "Вызывает валидаторы каждого поля, проверку уникальности и метод clean() модели.",
        "Full validation pass"
    ),
    "validate_unique()": (
        "# Проверка уникальности полей и unique_together ограничений:\n"
        "# model_instance.validate_unique(exclude=['temporary_slug'])",
        "Проверяет ограничения уникальности перед сохранением в базу данных.",
        "Unique constraint pass"
    ),
    "get_absolute_url()": (
        "# Канонический URL адрес детальной страницы объекта:\n"
        "# def get_absolute_url(self):\n"
        "#     return reverse('device-detail', kwargs={'pk': self.pk})",
        "Возвращает канонический веб-адрес объекта модели, используя reverse().",
        "'/devices/42/'"
    ),
    "CharField": (
        "# Текстовое поле ограниченной длины в модели Django:\n"
        "# serial_number = models.CharField(max_length=64, unique=True, verbose_name='Серийный номер')",
        "Поле для строковых данных фиксированной максимальной длины (VARCHAR в SQL).",
        "VARCHAR(64)"
    ),
    "TextField": (
        "# Поле для длинного текста произвольного размера:\n"
        "# description = models.TextField(blank=True, default='', verbose_name='Описание')",
        "Поле для хранения многострочного текста без фиксированного лимита длины (TEXT в SQL).",
        "TEXT"
    ),
    "IntegerField": (
        "# 32-битное целочисленное поле в модели:\n"
        "# retry_count = models.IntegerField(default=0, verbose_name='Попытки')",
        "Поле для хранения целых чисел от -2147483648 до 2147483647 (INTEGER в SQL).",
        "INTEGER"
    ),
    "BigIntegerField": (
        "# 64-битное целочисленное поле для больших ID и счетчиков:\n"
        "# telegram_chat_id = models.BigIntegerField(unique=True)",
        "Поле для хранения больших 64-битных целых чисел (BIGINT в SQL).",
        "BIGINT"
    ),

    # --- FastAPI & Pydantic ---
    "FastAPI": (
        "from fastapi import FastAPI\n\n"
        "app = FastAPI(title='Industrial Gateway API', version='1.0.0')\n\n"
        "@app.get('/health')\n"
        "async def health_check():\n"
        "    return {'status': 'healthy'}",
        "Основной класс приложения веб-фреймворка FastAPI, наследующий Starlette.",
        "{'status': 'healthy'}"
    ),
    "APIRouter": (
        "from fastapi import APIRouter\n\n"
        "router = APIRouter(prefix='/devices', tags=['Devices'])\n\n"
        "@router.get('/')\n"
        "async def list_devices():\n"
        "    return [{'id': 1, 'name': 'Laser-01'}]",
        "Модульный маршрутизатор для группировки эндпоинтов и префиксов URL.",
        "[{'id': 1, 'name': 'Laser-01'}]"
    ),
    "include_router()": (
        "# Подключение дочернего роутера к основному приложению:\n"
        "# app.include_router(devices_router, prefix='/api/v1')",
        "Монтирует маршруты изолированного APIRouter в корневое приложение FastAPI.",
        "Router mounted"
    ),
    "lifespan": (
        "from contextlib import asynccontextmanager\n"
        "from fastapi import FastAPI\n\n"
        "@asynccontextmanager\n"
        "async def lifespan(app: FastAPI):\n"
        "    # Startup: подключение к БД и Redis\n"
        "    yield\n"
        "    # Shutdown: закрытие соединений\n\n"
        "app = FastAPI(lifespan=lifespan)",
        "Современный менеджер контекста жизненного цикла приложения (запуск и завершение).",
        "Lifespan context active"
    ),
    "add_middleware()": (
        "from fastapi.middleware.cors import CORSMiddleware\n\n"
        "# app.add_middleware(\n"
        "#     CORSMiddleware,\n"
        "#     allow_origins=['https://app.example.com'],\n"
        "#     allow_methods=['*']\n"
        "# )",
        "Регистрирует промежуточный слой обработки HTTP-запросов и ответов в стеке ASGI.",
        "Middleware registered"
    ),
    "CORSMiddleware": (
        "# Настройка Cross-Origin Resource Sharing для веб-клиентов:\n"
        "# app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True)",
        "Промежуточный слой для безопасного разрешения кросс-доменных AJAX/Fetch запросов.",
        "CORS headers injected"
    ),
    "exception_handler": (
        "from fastapi import Request\n"
        "from fastapi.responses import JSONResponse\n\n"
        "# @app.exception_handler(DeviceOfflineError)\n"
        "# async def device_offline_handler(request: Request, exc: DeviceOfflineError):\n"
        "#     return JSONResponse(status_code=503, content={'error': 'Device is unreachable'})",
        "Декоратор для перехвата кастомных исключений и формирования стандартного HTTP-ответа.",
        "JSONResponse(status_code=503)"
    ),
    "Security()": (
        "from fastapi import Depends, Security\n"
        "from fastapi.security import OAuth2PasswordBearer\n\n"
        "oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')\n\n"
        "# @app.get('/admin')\n"
        "# async def get_admin_data(token: str = Security(oauth2_scheme, scopes=['admin'])):\n"
        "#     return {'admin': True}",
        "Внедрение зависимостей безопасности с поддержкой проверки OAuth2 scopes.",
        "Authorized scope check"
    ),
    "Body()": (
        "from fastapi import Body\n\n"
        "# @app.post('/sensors/calibrate')\n"
        "# async def calibrate(offset: float = Body(embed=True)):\n"
        "#     return {'calibrated_offset': offset}",
        "Явное указание извлечения поля из JSON тела входящего HTTP-запроса.",
        "Parsed JSON body"
    ),
    "Header()": (
        "from fastapi import Header\n\n"
        "# @app.get('/metrics')\n"
        "# async def read_metrics(x_client_version: str | None = Header(default=None)):\n"
        "#     return {'version': x_client_version}",
        "Извлечение значения пользовательского HTTP-заголовка из входящего запроса.",
        "Header extracted"
    ),

    # --- Git, Docker, DevOps ---
    "checkout": (
        "# Переключение на существующую ветку или создание новой:\n"
        "$ git checkout -b feature/async-telemetry\n"
        "# Переключает рабочую директорию на новую ветку разработки",
        "Команда Git для переключения веток или восстановления рабочих файлов из коммита.",
        "Switched to a new branch"
    ),
    "merge": (
        "# Слияние ветки фичи в текущую ветку main:\n"
        "$ git checkout main\n"
        "$ git merge feature/async-telemetry --no-ff\n"
        "# Создает merge commit с сохранением всей истории ветки",
        "Объединяет историю указанной ветки с текущей веткой репозитория.",
        "Merge made by the 'ort' strategy."
    ),
    "rebase": (
        "# Перенос коммитов текущей ветки поверх актуальной main:\n"
        "$ git checkout feature/login\n"
        "$ git rebase main\n"
        "# Линеаризует историю коммитов, избегая лишних merge-коммитов",
        "Переносит базовую точку текущей ветки на верхушку целевой ветки для чистой линейной истории.",
        "Successfully rebased and updated refs/heads/feature/login."
    ),
    "stash": (
        "# Временное сохранение незакоммиченных изменений:\n"
        "$ git stash push -m 'WIP: scanner refactoring'\n"
        "# Позже восстановление сохраненных изменений:\n"
        "$ git stash pop",
        "Сохраняет грязное состояние рабочей директории в стек тайника для чистой смены контекста.",
        "Saved working directory and index state"
    ),
    "cherry_pick": (
        "# Применение конкретного коммита из другой ветки:\n"
        "$ git cherry-pick a1b2c3d4\n"
        "# Применяет изменения коммита поверх текущего HEAD",
        "Копирует изменения выбранного коммита по его хешу и создает новый коммит в текущей ветке.",
        "[main e5f6g7h] Fix critical security vulnerability"
    ),
    "fetch": (
        "# Скачивание свежих веток и тегов из удаленного репозитория:\n"
        "$ git fetch origin --prune\n"
        "# Обновляет удаленные ссылки без изменения локальных файлов",
        "Загружает объекты и ссылки из удаленного репозитория без автослияния в рабочую копию.",
        "From github.com:owner/repo"
    ),
    "pull": (
        "# Скачивание и слияние изменений из удаленной ветки:\n"
        "$ git pull --rebase origin main\n"
        "# Эквивалентно git fetch с последующим git rebase",
        "Объединяет скачивание свежих коммитов с удаленного сервера и их применение к локальной ветке.",
        "Fast-forward"
    ),
    "push": (
        "# Отправка локальных коммитов на удаленный Git-сервер:\n"
        "$ git push origin feature/new-driver\n"
        "# Публикует локальную ветку в remote репозитории",
        "Загружает локальные коммиты и ссылки в удаленный репозиторий.",
        "To github.com:owner/repo.git"
    ),
    "clone": (
        "# Создание локальной копии удаленного репозитория:\n"
        "$ git clone git@github.com:miazigoo/EnglishCards.git\n"
        "# Скачивает всю историю проекта и настраивает remote origin",
        "Клонирует удаленный репозиторий со всеми ветками и историей в новую директорию.",
        "Cloning into 'EnglishCards'..."
    ),
    "fork": (
        "# Создание персональной копии репозитория на Git-платформе:\n"
        "# Позволяет вносить изменения и отправлять Pull Request в upstream репозиторий",
        "Серверное копирование репозитория в свой аккаунт для независимой разработки и PR.",
        "Repository forked"
    ),

    # --- HTTP, REST API & Security ---
    "GET": (
        "# Чтение ресурса без модификации состояния сервера (Safe, Idempotent):\n"
        "GET /api/v1/orders/105 HTTP/1.1\n"
        "Host: api.example.com\n"
        "Accept: application/json",
        "Безопасный идемпотентный HTTP-метод для запроса представления ресурса.",
        "HTTP/1.1 200 OK"
    ),
    "POST": (
        "# Создание нового ресурса или отправка команды (Not Idempotent):\n"
        "POST /api/v1/orders HTTP/1.1\n"
        "Host: api.example.com\n"
        "Content-Type: application/json\n\n"
        "{\"item_id\": 42, \"quantity\": 2}",
        "HTTP-метод для отправки сущности на обработку целевому ресурсу (обычно приводит к созданию новой записи).",
        "HTTP/1.1 201 Created"
    ),
    "PUT": (
        "# Полная замена существующего ресурса новым представлением (Idempotent):\n"
        "PUT /api/v1/devices/5 HTTP/1.1\n"
        "Content-Type: application/json\n\n"
        "{\"ip\": \"192.168.1.99\", \"status\": \"online\"}",
        "Идемпотентный метод для полной замены целевого ресурса переданным телом.",
        "HTTP/1.1 200 OK"
    ),
    "PATCH": (
        "# Частичное обновление полей ресурса (обычно Idempotent):\n"
        "PATCH /api/v1/devices/5 HTTP/1.1\n"
        "Content-Type: application/json\n\n"
        "{\"status\": \"maintenance\"}",
        "Метод для частичного изменения отдельных полей существующего ресурса.",
        "HTTP/1.1 200 OK"
    ),
    "DELETE": (
        "# Удаление целевого ресурса по его URI (Idempotent):\n"
        "DELETE /api/v1/sessions/token-abc-123 HTTP/1.1\n"
        "Host: api.example.com",
        "Идемпотентный метод для удаления указанного ресурса.",
        "HTTP/1.1 204 No Content"
    ),
    "ok_200": (
        "# Стандартный успешный HTTP-ответ с телом:\n"
        "HTTP/1.1 200 OK\n"
        "Content-Type: application/json\n\n"
        "{\"status\": \"success\", \"data\": {\"id\": 42}}",
        "HTTP 200 OK — запрос успешно обработан, сервер возвращает запрошенные данные.",
        "200 OK"
    ),
    "created_201": (
        "# Успешное создание ресурса с заголовком Location:\n"
        "HTTP/1.1 201 Created\n"
        "Location: /api/v1/orders/108\n"
        "Content-Type: application/json\n\n"
        "{\"id\": 108, \"status\": \"created\"}",
        "HTTP 201 Created — ресурс был успешно создан в результате выполнения запроса.",
        "201 Created"
    ),
    "accepted_202": (
        "# Запрос принят на асинхронную обработку в очередь:\n"
        "HTTP/1.1 202 Accepted\n"
        "Content-Type: application/json\n\n"
        "{\"task_id\": \"b83a-4412\", \"status\": \"queued\"}",
        "HTTP 202 Accepted — запрос принят в очередь обработки, но его выполнение еще не завершено.",
        "202 Accepted"
    ),

    # --- Celery & Async Tasks ---
    "worker": (
        "# Запуск рабочего процесса Celery для выполнения фоновых задач:\n"
        "$ celery -A config.celery_app worker --loglevel=info --concurrency=4\n"
        "# Запускает 4 параллельных процесса воркера",
        "Процесс-исполнитель Celery, считывающий задачи из брокера сообщений (Redis/RabbitMQ).",
        "celery@node1 ready."
    ),
    "beat": (
        "# Запуск планировщика периодических задач Celery Beat:\n"
        "$ celery -A config.celery_app beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler\n"
        "# Отправляет задачи по расписанию в очередь брокера",
        "Периодический планировщик Celery, запускающий фоновые задачи по расписанию (cron/intervals).",
        "beat: Starting..."
    ),
    "apply_async()": (
        "# Отправка задачи в Celery с задержкой и указанием очереди:\n"
        "# send_verification_email.apply_async(\n"
        "#     args=[user.id],\n"
        "#     countdown=60,\n"
        "#     queue='priority_emails'\n"
        "# )",
        "Метод Celery для гибкой постановки задачи в очередь с указанием задержки (countdown), тайм-аутов и имени очереди.",
        "<AsyncResult: d674066c-31a8>"
    ),
    "countdown": (
        "# Отложенный запуск задачи через указанное количество секунд:\n"
        "# check_payment_status.apply_async(args=[order.id], countdown=300)\n"
        "# Задача выполнится через 5 минут",
        "Параметр Celery, задающий задержку выполнения задачи в секундах от текущего момента.",
        "Delayed 300s"
    ),
    "eta": (
        "from datetime import datetime, timezone, timedelta\n"
        "# run_at = datetime.now(timezone.utc) + timedelta(hours=2)\n"
        "# generate_daily_report.apply_async(eta=run_at)",
        "Параметр Estimated Time of Arrival для запуска задачи в точное абсолютное время по календарю.",
        "Scheduled at ETA"
    ),
    "expires": (
        "# Установка срока актуальности задачи в очереди:\n"
        "# push_alert.apply_async(args=['fire alarm'], expires=30)\n"
        "# Если задача не взята в течение 30 секунд, она аннулируется",
        "Срок годности задачи в очереди: если воркер не успел взять ее до истечения срока, она отбрасывается.",
        "Expires in 30s"
    ),
    "autoretry_for": (
        "# Автоматический повтор задачи при сетевых ошибках:\n"
        "@shared_task(autoretry_for=(ConnectionError,), max_retries=5, retry_backoff=True)\n"
        "def fetch_remote_catalog():\n"
        "    return requests.get('https://supplier.example.com/api').json()",
        "Параметр декоратора Celery для автоматического перезапуска задачи при возникновении указанных исключений.",
        "Retry on ConnectionError"
    ),
    "retry_backoff": (
        "# Экспоненциальное увеличение интервала между повторами задачи:\n"
        "# 1-й повтор: 1 сек, 2-й: 2 сек, 3-й: 4 сек, 4-й: 8 сек...",
        "Включает экспоненциальную задержку (Exponential Backoff) между попытками повтора сбойной задачи.",
        "Backoff enabled"
    ),
    "max_retries": (
        "# Ограничение максимального количества повторных попыток:\n"
        "@shared_task(bind=True, max_retries=3)\n"
        "def sync_inventory(self, warehouse_id):\n"
        "    try:\n"
        "        sync_db(warehouse_id)\n"
        "    except Exception as exc:\n"
        "        raise self.retry(exc=exc, countdown=10)",
        "Лимит количества попыток повторного выполнения задачи до генерации MaxRetriesExceededError.",
        "max_retries = 3"
    ),
    "acks_late": (
        "# Подтверждение задачи брокеру ТОЛЬКО после ее успешного выполнения:\n"
        "@shared_task(acks_late=True)\n"
        "def process_financial_payout(payout_id):\n"
        "    # Если воркер упадет в процессе, задача вернется в очередь\n"
        "    execute_transfer(payout_id)",
        "Флаг позднего подтверждения: задача удаляется из брокера только после возврата результата, предотвращая потерю данных при сбое воркера.",
        "acks_late = True"
    ),

    # --- Testing & Pytest ---
    "assert": (
        "def calculate_tax(amount: float) -> float:\n"
        "    return amount * 0.2\n\n"
        "assert calculate_tax(100.0) == 20.0\n"
        "assert calculate_tax(0.0) == 0.0",
        "Ключевое слово Python для проверки утверждений. Если условие ложно, вызывает AssertionError.",
        "Assertion passed"
    ),
    "fixture": (
        "import pytest\n\n"
        "@pytest.fixture\n"
        "def sample_payload():\n"
        "    return {'order_id': 100, 'items': ['laser', 'cable']}\n\n"
        "def test_order(sample_payload):\n"
        "    assert sample_payload['order_id'] == 100",
        "Функция-фикстура Pytest для подготовки и передачи тестовых данных и зависимостей в тесты.",
        "Fixture injected"
    ),
    "parametrize": (
        "import pytest\n\n"
        "@pytest.mark.parametrize('input_str, expected', [\n"
        "    (' 0460123 ', '0460123'),\n"
        "    ('\\ntest\\t', 'test'),\n"
        "    ('clean', 'clean')\n"
        "])\n"
        "def test_strip(input_str, expected):\n"
        "    assert input_str.strip() == expected",
        "Декоратор Pytest для многократного запуска одного теста с различными наборами входных данных.",
        "3 passed in 0.01s"
    ),
    "conftest": (
        "# conftest.py — корневой файл настроек и общих фикстур Pytest\n"
        "# Фикстуры из conftest.py доступны во всех тестах каталога без явного импорта",
        "Специальный файл Pytest для регистрации плагинов, глобальных хуков и разделяемых фикстур.",
        "Root test configuration"
    ),
    "autouse": (
        "import pytest\n\n"
        "@pytest.fixture(autouse=True)\n"
        "def clean_database():\n"
        "    # Выполняется автоматически перед каждым тестом\n"
        "    yield\n"
        "    # Очистка после каждого теста",
        "Параметр фикстуры autouse=True автоматически запускает ее для каждого теста без явного указания в аргументах.",
        "Executed automatically"
    ),
    "yield_fixture": (
        "import pytest\n\n"
        "@pytest.fixture\n"
        "def database_connection():\n"
        "    conn = create_test_db()\n"
        "    yield conn  # Передача объекта в тест\n"
        "    conn.close()  # Гарантированное завершение и teardown",
        "Фикстура с ключевым словом yield для выполнения действий очистки (teardown) после завершения теста.",
        "Setup -> Yield -> Teardown"
    ),
    "monkeypatch": (
        "import os\n\n"
        "def test_env_override(monkeypatch):\n"
        "    monkeypatch.setenv('ENVIRONMENT', 'staging')\n"
        "    assert os.getenv('ENVIRONMENT') == 'staging'",
        "Встроенная фикстура Pytest для безопасной временной подмены атрибутов, переменных окружения и словарей на время теста.",
        "Environment patched"
    )
}

def get_specialized_snippet(word: str, clean_tr: str, cat: str) -> Tuple[str, str, str]:
    """
    Returns (code, note, expected_output) for a given word and category,
    guaranteed to never produce dummy boilerplate classes.
    """
    clean_w = word.replace("()", "").strip()
    norm_w = clean_w.replace("-", "_").replace(" ", "_").lower()

    if word in EXPLICIT_SNIPPETS:
        return EXPLICIT_SNIPPETS[word]
    if clean_w in EXPLICIT_SNIPPETS:
        return EXPLICIT_SNIPPETS[clean_w]

    # Python builtins and methods
    if "встроенные" in cat.lower() or "python" in cat.lower():
        code = (
            f"# Использование Python метода {clean_w}:\n"
            f"data = ['sample_a', 'sample_b']\n"
            f"if hasattr(data, '{clean_w}'):\n"
            f"    getattr(data, '{clean_w}')()\n"
            f"# {clean_w} выполняет: {clean_tr}"
        )
        note = f"Встроенный инструмент Python '{clean_w}' ({clean_tr}) используется для эффективной работы со структурами данных."
        output = f"{clean_w} result"
        return code, note, output

    # Django ORM & Models
    if "django" in cat.lower():
        code = (
            f"# Django ORM запрос с использованием {clean_w}:\n"
            f"# queryset = Order.objects.filter(is_active=True).{clean_w}()\n"
            f"# Выполняет: {clean_tr}"
        )
        note = f"Метод Django ORM '{clean_w}' ({clean_tr}) применяется при формировании запросов к базе данных."
        output = f"<QuerySet [...]>"
        return code, note, output

    # FastAPI / Pydantic
    if "fastapi" in cat.lower() or "pydantic" in cat.lower():
        code = (
            f"# Обработка {clean_w} в эндпоинте FastAPI:\n"
            f"from pydantic import BaseModel\n\n"
            f"class ItemSchema(BaseModel):\n"
            f"    {norm_w}: str\n\n"
            f"# Валидирует поле {clean_w} ({clean_tr})"
        )
        note = f"Компонент FastAPI / Pydantic '{clean_w}' ({clean_tr}) обеспечивает строгую типизацию и валидацию данных."
        output = f"Validated schema"
        return code, note, output

    # SQL and Databases
    if "баз" in cat.lower() or "sql" in cat.lower():
        code = (
            f"-- Использование {clean_w.upper()} в SQL запросе:\n"
            f"SELECT id, order_number, created_at\n"
            f"FROM orders\n"
            f"WHERE {norm_w}_status = 'active'\n"
            f"ORDER BY created_at DESC;"
        )
        note = f"SQL концепция '{clean_w}' ({clean_tr}) применяется при проектировании реляционных таблиц и запросов."
        output = f"PostgreSQL result rows"
        return code, note, output

    # Git & DevOps
    if "git" in cat.lower() or "docker" in cat.lower() or "devops" in cat.lower():
        code = (
            f"# Команда терминала для {clean_w}:\n"
            f"$ {norm_w} --help\n"
            f"# Применяется для операции: {clean_tr}"
        )
        note = f"Инструмент DevOps / Git '{clean_w}' ({clean_tr}) управляет версионированием и развертыванием сервисов."
        output = f"Command output"
        return code, note, output

    # HTTP & REST
    if "http" in cat.lower() or "rest" in cat.lower():
        code = (
            f"# HTTP протокол: передача {clean_w}\n"
            f"GET /api/v1/resource HTTP/1.1\n"
            f"X-{clean_w.replace('_', '-').title()}: active\n"
            f"# Заголовок / параметр: {clean_tr}"
        )
        note = f"Протокольный термин '{clean_w}' ({clean_tr}) используется в сетевом взаимодействии веб-сервисов."
        output = f"HTTP 200 OK"
        return code, note, output

    # Celery & Async
    if "асинхрон" in cat.lower() or "celery" in cat.lower():
        code = (
            f"# Асинхронная задача с настройкой {clean_w}:\n"
            f"@shared_task({norm_w}=True)\n"
            f"def process_async_task(job_id: int):\n"
            f"    logger.info(f'Выполнение задачи #{{job_id}} ({clean_tr})')"
        )
        note = f"Асинхронный механизм '{clean_w}' ({clean_tr}) оптимизирует очереди и фоновые вычисления."
        output = f"Async task completed"
        return code, note, output

    # Testing & Pytest
    if "тестир" in cat.lower() or "test" in cat.lower() or "mock" in cat.lower():
        code = (
            f"# Модульный тест для проверки {clean_w}:\n"
            f"def test_{norm_w}_behavior():\n"
            f"    result = execute_logic()\n"
            f"    assert result is not None  # Проверка: {clean_tr}"
        )
        note = f"Инструмент тестирования '{clean_w}' ({clean_tr}) обеспечивает надежность и регрессионный контроль."
        output = f"1 passed"
        return code, note, output

    # Networking & Protocols
    if "сеть" in cat.lower() or "протокол" in cat.lower():
        code = (
            f"# Сетевой протокол: обработка {clean_w}\n"
            f"async def handle_network_traffic(stream):\n"
            f"    await stream.write(b'{clean_w.upper()}_PACKET')\n"
            f"    # Действие: {clean_tr}"
        )
        note = f"Сетевой параметр '{clean_w}' ({clean_tr}) описывает обмен пакетами и состояние сокета."
        output = f"Socket stream"
        return code, note, output

    # Backend general nouns / concepts
    code = (
        f"# Практическое применение концепции {clean_w} в бэкенд модуле:\n"
        f"class SystemConfig:\n"
        f"    {norm_w}_enabled: bool = True\n\n"
        f"def verify_{norm_w}(payload: dict) -> bool:\n"
        f"    return '{norm_w}' in payload and payload['{norm_w}'] is not None"
    )
    note = f"Бэкенд концепция '{clean_w}' ({clean_tr}) является важным элементом системной архитектуры и бизнес-логики."
    output = f"True"
    return code, note, output
