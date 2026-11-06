#!/usr/bin/env python3
"""Build original, short reading exercises based on official framework guides."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINGS = [
    {
        "id": "django_models", "title": "Django: models and fields",
        "source_url": "https://docs.djangoproject.com/en/5.2/topics/db/models/",
        "passage": "A model describes the structure of data in a Django application. Each field represents one kind of value, such as a title, a date, or a price. When you create a model class, Django can use it to create a database table. A field may also have options. For example, you can provide a default value or require a value from the user. Read the field name and its options together: they tell you what the application stores and which values are allowed.",
        "questions": [
            {"question_ru": "Что описывает модель?", "options_ru": ["Структуру данных", "Цвет кнопки", "Скорость сети"], "correct": 0, "explanation_ru": "Модель описывает структуру данных приложения."},
            {"question_ru": "Что может задавать параметр поля?", "options_ru": ["Значение по умолчанию", "Адрес сервера Git", "Версию Python"], "correct": 0, "explanation_ru": "У поля может быть значение по умолчанию."},
        ],
    },
    {
        "id": "django_queries", "title": "Django: finding records",
        "source_url": "https://docs.djangoproject.com/en/5.2/topics/db/queries/",
        "passage": "A query asks the database for records. In Django, a QuerySet can describe a group of records before the database is accessed. You can filter the group to keep only records that match a condition. You can also order the result or limit the number of records. These operations can be combined. When reading documentation, notice the difference between a query that builds a QuerySet and an action that actually retrieves data. This distinction helps you understand when the application talks to the database.",
        "questions": [
            {"question_ru": "Зачем применяют фильтр?", "options_ru": ["Оставить записи по условию", "Удалить таблицу", "Создать пользователя"], "correct": 0, "explanation_ru": "Фильтр оставляет записи, соответствующие условию."},
            {"question_ru": "Что ещё можно сделать с результатом?", "options_ru": ["Упорядочить его", "Изменить язык Python", "Отключить сервер"], "correct": 0, "explanation_ru": "Результат можно упорядочить или ограничить."},
        ],
    },
    {
        "id": "django_urls", "title": "Django: URL routes",
        "source_url": "https://docs.djangoproject.com/en/5.2/topics/http/urls/",
        "passage": "A URL route connects a web address to a view. Django checks the requested path against the patterns in the URL configuration. When it finds a match, it calls the related view. A pattern may capture a value from the path, such as an article number, and pass it to the view. If no pattern matches, the user receives a not found response. While reading a route definition, identify the path, the captured values, and the view. This makes the request flow easier to follow.",
        "questions": [
            {"question_ru": "Что происходит при совпадении маршрута?", "options_ru": ["Вызывается представление", "Удаляется база", "Создаётся миграция"], "correct": 0, "explanation_ru": "Маршрут направляет запрос в представление."},
            {"question_ru": "Что может извлекаться из пути?", "options_ru": ["Номер статьи", "Пароль сервера", "Размер экрана"], "correct": 0, "explanation_ru": "Шаблон пути может захватить значение, например номер статьи."},
        ],
    },
    {
        "id": "django_forms", "title": "Django: forms and validation",
        "source_url": "https://docs.djangoproject.com/en/5.2/topics/forms/",
        "passage": "A form collects input from a user. Before an application saves that input, it should validate the submitted values. A field can be required, or it can accept an empty value. If validation fails, the form can display errors so the user knows what to correct. The server should not trust a value only because it came from a visible form. When reading form documentation, look for words such as required, valid, error, and cleaned data. They describe the path from input to a usable value.",
        "questions": [
            {"question_ru": "Что нужно сделать до сохранения ввода?", "options_ru": ["Проверить значения", "Закрыть браузер", "Сменить тему"], "correct": 0, "explanation_ru": "Значения формы нужно проверить."},
            {"question_ru": "Зачем показывают ошибки формы?", "options_ru": ["Чтобы пользователь исправил ввод", "Чтобы скрыть данные", "Чтобы ускорить сеть"], "correct": 0, "explanation_ru": "Сообщения об ошибках помогают исправить ввод."},
        ],
    },
    {
        "id": "django_migrations", "title": "Django: changing the schema",
        "source_url": "https://docs.djangoproject.com/en/5.2/topics/migrations/",
        "passage": "An application changes over time. When a model changes, the database schema may need to change as well. A migration records a planned change so it can be applied to a database. Django provides commands to create migrations and to apply them. The migration files should usually be kept with the project source code. Read migration instructions carefully: creating a migration file is a different step from applying it to the database. This difference matters when several people work on the same project.",
        "questions": [
            {"question_ru": "Что записывает миграция?", "options_ru": ["Запланированное изменение схемы", "Историю браузера", "Пароль пользователя"], "correct": 0, "explanation_ru": "Миграция хранит изменение схемы базы данных."},
            {"question_ru": "Чем создание миграции отличается от применения?", "options_ru": ["Сначала создают файл, затем меняют БД", "Это один и тот же шаг", "Миграция не затрагивает БД"], "correct": 0, "explanation_ru": "Создание файла и применение к базе — разные действия."},
        ],
    },
    {
        "id": "django_tests", "title": "Django: testing behavior",
        "source_url": "https://docs.djangoproject.com/en/5.2/topics/testing/overview/",
        "passage": "A test checks whether an application behaves as expected. It can send a request, inspect a response, and compare the result with an expected value. Tests help detect a failure after code changes. In Django, tests can use a separate test database, so normal application data is not used for the test run. A useful test has a clear purpose: it should tell you which behavior failed and why that behavior matters. When reading a test guide, distinguish the setup, the action, and the assertion.",
        "questions": [
            {"question_ru": "Что сравнивает тест?", "options_ru": ["Фактический и ожидаемый результат", "Два названия файла", "Две темы экрана"], "correct": 0, "explanation_ru": "Тест сравнивает результат с ожиданием."},
            {"question_ru": "Зачем отдельная тестовая база?", "options_ru": ["Не использовать обычные данные приложения", "Ускорить звук", "Изменить язык интерфейса"], "correct": 0, "explanation_ru": "Тесты не должны работать с обычными данными приложения."},
        ],
    },
    {
        "id": "django_security", "title": "Django: security checks",
        "source_url": "https://docs.djangoproject.com/en/5.2/topics/security/",
        "passage": "A public web application receives input from people it does not know. Some input may be unsafe. Django offers protections for common risks, but the developer still needs to use them correctly. For example, a page should escape untrusted text before displaying it, and a form that changes data should be protected against forged requests. Security guidance also explains why secrets must stay out of public code. While reading this documentation, pay attention to words that describe a risk, a protection, and the developer's responsibility.",
        "questions": [
            {"question_ru": "Почему пользовательский ввод проверяют?", "options_ru": ["Он может быть небезопасным", "Он всегда пустой", "Он не приходит на сервер"], "correct": 0, "explanation_ru": "Внешний ввод нельзя считать безопасным."},
            {"question_ru": "Где не следует хранить секреты?", "options_ru": ["В общедоступном коде", "В защищённом хранилище", "В настройках доступа"], "correct": 0, "explanation_ru": "Секреты не должны попадать в публичный код."},
        ],
    },
    {
        "id": "fastapi_path", "title": "FastAPI: path parameters",
        "source_url": "https://fastapi.tiangolo.com/tutorial/path-params/",
        "passage": "A path parameter is a value inside a URL path. An endpoint can use that value to identify a resource, such as an item with a particular number. In FastAPI, a parameter can have a Python type annotation. FastAPI uses the annotation to convert the text from the path and validate it. If the value cannot be converted, the client receives a validation error. When you read an endpoint example, compare the path pattern with the function parameter. They refer to the same value.",
        "questions": [
            {"question_ru": "Где находится path parameter?", "options_ru": ["В пути URL", "Только в теле ответа", "В имени приложения"], "correct": 0, "explanation_ru": "Параметр пути — часть URL."},
            {"question_ru": "Что помогает проверить тип значения?", "options_ru": ["Аннотация типа Python", "Цвет кнопки", "Имя репозитория"], "correct": 0, "explanation_ru": "FastAPI использует аннотацию типа для преобразования и проверки."},
        ],
    },
    {
        "id": "fastapi_body", "title": "FastAPI: request body",
        "source_url": "https://fastapi.tiangolo.com/tutorial/body/",
        "passage": "A client can send data in the body of a request. This is useful when an endpoint needs several related values. In FastAPI, a Pydantic model can describe the expected structure. FastAPI reads the incoming data, converts values where appropriate, and reports validation errors when the data does not fit the model. The endpoint receives the validated object rather than raw text. When reading an API description, ask which values come from the path, which come from the query, and which come from the request body.",
        "questions": [
            {"question_ru": "Что описывает модель Pydantic?", "options_ru": ["Ожидаемую структуру данных", "Цвет ответа", "Путь к APK"], "correct": 0, "explanation_ru": "Модель описывает ожидаемые поля и значения."},
            {"question_ru": "Что получит обработчик после проверки?", "options_ru": ["Проверенный объект", "Случайный текст", "Файл миграции"], "correct": 0, "explanation_ru": "FastAPI передаёт обработчику проверенный объект."},
        ],
    },
    {
        "id": "fastapi_dependencies", "title": "FastAPI: dependencies",
        "source_url": "https://fastapi.tiangolo.com/tutorial/dependencies/",
        "passage": "A dependency provides a value or a service that an endpoint needs. The same dependency can be reused by several endpoints. For example, it may read a request header, check the current user, or provide access to a database session. FastAPI resolves dependencies before it calls the endpoint function. A dependency can itself depend on another dependency. When you read a function signature, identify which values come directly from the request and which are provided by dependencies. This helps explain where the function's inputs come from.",
        "questions": [
            {"question_ru": "Зачем используют зависимость?", "options_ru": ["Передать обработчику нужное значение или сервис", "Поменять шрифт", "Записать аудио"], "correct": 0, "explanation_ru": "Зависимость предоставляет то, что нужно обработчику."},
            {"question_ru": "Может ли зависимость использовать другую зависимость?", "options_ru": ["Да", "Нет", "Только при тестировании"], "correct": 0, "explanation_ru": "FastAPI поддерживает вложенные зависимости."},
        ],
    },
]


if __name__ == "__main__":
    assert len(READINGS) == 10
    assert all(len(r["questions"]) == 2 and len(r["passage"].split()) >= 65 for r in READINGS)
    out = ROOT / "content/readings.json"
    out.write_text(json.dumps(READINGS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Created", len(READINGS), "readings in", out)
