# scripts/data_benchmarks.py
"""Authoritative benchmark cards strictly conforming to Sections 5 and 6 of GEMINI_TECH_SPEC_ENGLISH_V3.md."""

BENCHMARK_CARDS = [
    {
        "schema_version": 3,
        "card_id": "python.str.rsplit.directional",
        "legacy_ids": [45],
        "content_revision": 2,
        "lexeme_id": "en.split.verb",
        "display_term": "rsplit()",
        "namespace": "python.str",
        "entry_type": "api_method",
        "part_of_speech": "verb",
        "language_level": "A2",
        "technical_level": "basic",
        "priority": "core_it",
        "tags": ["python", "strings", "direction", "methods"],
        "meaning_ru_short": "разделяет строку по разделителю, выбирая разделения справа",
        "explanation_ru": "Метод возвращает список частей строки. Если число разделений ограничено параметром maxsplit, выбираются самые правые разделители. Полученные части остаются в обычном порядке слева направо.",
        "name_breakdown": {
            "kind": "pedagogical_breakdown",
            "parts": [
                {"text_en": "right", "meaning_ru": "правый / справа"},
                {"text_en": "split", "meaning_ru": "разделять, разбивать на части"}
            ],
            "explanation_ru": "Для запоминания: right split — «разделить справа», приблизительно «райт сплит»."
        },
        "pronunciation": {
            "spoken_en": "R split",
            "ipa": None,
            "ru_hint": "ар сплит",
            "verification": "human_verified"
        },
        "examples": [
            {
                "example_id": "filename_extension",
                "en": "Split the filename from the right to get the extension.",
                "ru": "Раздели имя файла справа, чтобы получить расширение."
            },
            {
                "example_id": "url_path",
                "en": "Use rsplit with maxsplit 1 to extract the final path segment.",
                "ru": "Используй rsplit с maxsplit 1, чтобы извлечь последний сегмент пути."
            }
        ],
        "practice": {
            "enabled_templates": ["en_to_ru", "ru_to_en", "listening", "cloze", "spelling"],
            "production_prompt_ru": "Метод строки Python str: разделить строку справа с ограничением",
            "accepted_answers": ["rsplit", "rsplit()", "str.rsplit"],
            "cloze": {
                "example_id": "filename_extension",
                "target": "right"
            }
        },
        "technical": {
            "api": "str.rsplit",
            "python_version": "3.12",
            "example_kind": "standalone",
            "code": "filename = 'report.final.csv'\nassert filename.rsplit('.', 1) == ['report.final', 'csv']\nassert filename.split('.', 1) == ['report', 'final.csv']",
            "expected_output": "['report.final', 'csv']",
            "source_url": "https://docs.python.org/3.12/library/stdtypes.html#str.rsplit"
        },
        "qa": {
            "qa_status": "ready",
            "review_level": "automated",
            "reviewed_at": "2026-11-03T00:30:00Z",
            "issues": []
        }
    },
    {
        "schema_version": 3,
        "card_id": "python.builtins.zip",
        "legacy_ids": [2],
        "content_revision": 2,
        "lexeme_id": "en.zip.verb",
        "display_term": "zip()",
        "namespace": "python.builtins",
        "entry_type": "api_method",
        "part_of_speech": "verb",
        "language_level": "A2",
        "technical_level": "basic",
        "priority": "core_it",
        "tags": ["python", "builtins", "iterables", "pairing"],
        "meaning_ru_short": "объединяет элементы нескольких коллекций попарно по позициям",
        "explanation_ru": "Объединяет элементы по позициям: первый с первым, второй со вторым. Например, имена и оценки превращаются в пары 'имя — оценка'. По умолчанию заканчивает работу на самой короткой последовательности.",
        "name_breakdown": {
            "kind": "pedagogical_breakdown",
            "parts": [
                {"text_en": "zipper", "meaning_ru": "застежка-молния"}
            ],
            "explanation_ru": "Подобно молнии на одежде, zip соединяет элементы с двух сторон попарно."
        },
        "pronunciation": {
            "spoken_en": "zip",
            "ipa": "/zɪp/",
            "ru_hint": "зип",
            "verification": "human_verified"
        },
        "examples": [
            {
                "example_id": "pair_names_scores",
                "en": "Use zip to pair names with scores.",
                "ru": "Используй zip, чтобы соединить имена с оценками."
            },
            {
                "example_id": "two_lists_loop",
                "en": "Iterate over two lists in parallel using zip.",
                "ru": "Перебирай два списка параллельно с помощью zip."
            }
        ],
        "practice": {
            "enabled_templates": ["en_to_ru", "ru_to_en", "listening", "cloze", "spelling"],
            "production_prompt_ru": "Встроенная функция Python: попарно объединить элементы итераторов",
            "accepted_answers": ["zip", "zip()"],
            "cloze": {
                "example_id": "pair_names_scores",
                "target": "zip"
            }
        },
        "technical": {
            "api": "zip",
            "python_version": "3.12",
            "example_kind": "standalone",
            "code": "names = ['Anna', 'Max']\nscores = [90, 85, 70]\nresult = list(zip(names, scores))\nassert result == [('Anna', 90), ('Max', 85)]",
            "expected_output": "[('Anna', 90), ('Max', 85)]",
            "source_url": "https://docs.python.org/3.12/library/functions.html#zip"
        },
        "qa": {
            "qa_status": "ready",
            "review_level": "automated",
            "reviewed_at": "2026-11-03T00:30:00Z",
            "issues": []
        }
    },
    {
        "schema_version": 3,
        "card_id": "python.builtins.issubclass",
        "legacy_ids": [4],
        "content_revision": 2,
        "lexeme_id": "en.subclass.noun",
        "display_term": "issubclass()",
        "namespace": "python.builtins",
        "entry_type": "api_method",
        "part_of_speech": "verb",
        "language_level": "B1",
        "technical_level": "basic",
        "priority": "core_it",
        "tags": ["python", "builtins", "oop", "inheritance"],
        "meaning_ru_short": "проверяет отношение наследования между классами",
        "explanation_ru": "Проверяет, является ли первый класс наследником (прямым или косвенным) второго класса. Класс также считается подклассом самого себя. В отличие от isinstance(), проверяются именно классы, а не объекты-экземпляры.",
        "name_breakdown": {
            "kind": "pedagogical_breakdown",
            "parts": [
                {"text_en": "is", "meaning_ru": "является ли"},
                {"text_en": "subclass", "meaning_ru": "подкласс / наследник"}
            ],
            "explanation_ru": "Вопрос для проверки: является ли класс подклассом?"
        },
        "pronunciation": {
            "spoken_en": "is subclass",
            "ipa": None,
            "ru_hint": "из сабкласс",
            "verification": "human_verified"
        },
        "examples": [
            {
                "example_id": "dog_animal",
                "en": "Check whether Dog is a subclass of Animal.",
                "ru": "Проверь, является ли Dog подклассом Animal."
            },
            {
                "example_id": "custom_exception",
                "en": "Verify that our custom error is a subclass of Exception.",
                "ru": "Убедись, что наша собственная ошибка является подклассом Exception."
            }
        ],
        "practice": {
            "enabled_templates": ["en_to_ru", "ru_to_en", "listening", "cloze", "spelling"],
            "production_prompt_ru": "Функция Python: проверить, наследуется ли класс от другого класса",
            "accepted_answers": ["issubclass", "issubclass()"],
            "cloze": {
                "example_id": "dog_animal",
                "target": "subclass"
            }
        },
        "technical": {
            "api": "issubclass",
            "python_version": "3.12",
            "example_kind": "standalone",
            "code": "class Animal:\n    pass\n\nclass Dog(Animal):\n    pass\n\nassert issubclass(Dog, Animal) is True\nassert issubclass(Animal, Dog) is False\nassert issubclass(Dog, Dog) is True",
            "expected_output": "True",
            "source_url": "https://docs.python.org/3.12/library/functions.html#issubclass"
        },
        "qa": {
            "qa_status": "ready",
            "review_level": "automated",
            "reviewed_at": "2026-11-03T00:30:00Z",
            "issues": []
        }
    },
    {
        "schema_version": 3,
        "card_id": "python.builtins.filter",
        "legacy_ids": [17],
        "content_revision": 2,
        "lexeme_id": "en.filter.verb",
        "display_term": "filter()",
        "namespace": "python.builtins",
        "entry_type": "api_method",
        "part_of_speech": "verb",
        "language_level": "A2",
        "technical_level": "basic",
        "priority": "core_it",
        "tags": ["python", "builtins", "iterables", "filtering"],
        "meaning_ru_short": "отбирает элементы последовательности, для которых условие истинно",
        "explanation_ru": "Возвращает итератор по элементам последовательности, для которых функция-предикат возвращает истину. Если функция передана как None, отбираются все элементы, оцениваемые как True в булевом контексте.",
        "name_breakdown": {
            "kind": "pedagogical_breakdown",
            "parts": [
                {"text_en": "filter", "meaning_ru": "фильтровать / отсеивать"}
            ],
            "explanation_ru": "Отсеивание лишних элементов по заданному критерию."
        },
        "pronunciation": {
            "spoken_en": "filter",
            "ipa": "/ˈfɪltər/",
            "ru_hint": "филтэр",
            "verification": "human_verified"
        },
        "examples": [
            {
                "example_id": "filter_negatives",
                "en": "Filter out negative numbers from the list.",
                "ru": "Отфильтруй отрицательные числа из списка, то есть убери их."
            },
            {
                "example_id": "filter_active",
                "en": "We can filter empty strings from the incoming payload.",
                "ru": "Мы можем отфильтровать пустые строки из входящих данных."
            }
        ],
        "practice": {
            "enabled_templates": ["en_to_ru", "ru_to_en", "listening", "cloze", "spelling"],
            "production_prompt_ru": "Встроенная функция Python: отфильтровать элементы итератора по предикату",
            "accepted_answers": ["filter", "filter()"],
            "cloze": {
                "example_id": "filter_negatives",
                "target": "Filter"
            }
        },
        "technical": {
            "api": "filter",
            "python_version": "3.12",
            "example_kind": "standalone",
            "code": "numbers = [-2, 0, 3, 5]\nresult = list(filter(lambda n: n >= 0, numbers))\nassert result == [0, 3, 5]",
            "expected_output": "[0, 3, 5]",
            "source_url": "https://docs.python.org/3.12/library/functions.html#filter"
        },
        "qa": {
            "qa_status": "ready",
            "review_level": "automated",
            "reviewed_at": "2026-11-03T00:30:00Z",
            "issues": []
        }
    },
    {
        "schema_version": 3,
        "card_id": "django.queryset.filter",
        "legacy_ids": [17],
        "content_revision": 2,
        "lexeme_id": "en.filter.verb",
        "display_term": "QuerySet.filter()",
        "namespace": "django.db.models.query.QuerySet",
        "entry_type": "api_method",
        "part_of_speech": "verb",
        "language_level": "B1",
        "technical_level": "intermediate",
        "priority": "core_it",
        "tags": ["django", "orm", "sql", "queryset"],
        "meaning_ru_short": "фильтрует записи таблицы базы данных по условиям WHERE",
        "explanation_ru": "Возвращает новый QuerySet, содержащий объекты, соответствующие заданным параметрам поиска (WHERE в SQL). Поддерживает lookup-фильтры вроде field__gte, field__icontains.",
        "name_breakdown": {
            "kind": "pedagogical_breakdown",
            "parts": [
                {"text_en": "query set", "meaning_ru": "набор строк запроса к БД"},
                {"text_en": "filter", "meaning_ru": "фильтровать по условиям"}
            ],
            "explanation_ru": "Фильтрация набора записей в базе данных."
        },
        "pronunciation": {
            "spoken_en": "QuerySet filter",
            "ipa": None,
            "ru_hint": "квэри сет филтэр",
            "verification": "human_verified"
        },
        "examples": [
            {
                "example_id": "active_users",
                "en": "Filter active users created this month.",
                "ru": "Отфильтруй активных пользователей, созданных в этом месяце."
            },
            {
                "example_id": "device_status",
                "en": "Filter all online devices assigned to production line number one.",
                "ru": "Отфильтруй все онлайн-станки, назначенные на производственную линию номер один."
            }
        ],
        "practice": {
            "enabled_templates": ["en_to_ru", "ru_to_en", "listening", "cloze", "spelling"],
            "production_prompt_ru": "Метод Django QuerySet: фильтрация объектов модели по условиям WHERE",
            "accepted_answers": ["filter", "filter()", "QuerySet.filter"],
            "cloze": {
                "example_id": "active_users",
                "target": "Filter"
            }
        },
        "technical": {
            "api": "QuerySet.filter",
            "python_version": "3.12",
            "example_kind": "framework_fragment",
            "code": "# Django ORM пример:\n# users = User.objects.filter(is_active=True, role='developer')\n# Генерирует SQL: SELECT ... WHERE is_active = TRUE AND role = 'developer'",
            "expected_output": "<QuerySet [User, ...]>",
            "source_url": "https://docs.djangoproject.com/en/5.2/ref/models/querysets/#filter"
        },
        "qa": {
            "qa_status": "ready",
            "review_level": "automated",
            "reviewed_at": "2026-11-03T00:30:00Z",
            "issues": []
        }
    },
    {
        "schema_version": 3,
        "card_id": "python.builtins.getattr",
        "legacy_ids": [6],
        "content_revision": 2,
        "lexeme_id": "en.attribute.noun",
        "display_term": "getattr()",
        "namespace": "python.builtins",
        "entry_type": "api_method",
        "part_of_speech": "verb",
        "language_level": "A2",
        "technical_level": "basic",
        "priority": "core_it",
        "tags": ["python", "builtins", "attributes", "reflection"],
        "meaning_ru_short": "получает значение атрибута объекта по его строковому имени",
        "explanation_ru": "Возвращает значение именованного атрибута объекта. Если атрибут не найден, возвращается переданное третье позиционное значение по умолчанию (default). Если значение по умолчанию не указано и атрибут отсутствует, вызывается AttributeError.",
        "name_breakdown": {
            "kind": "pedagogical_breakdown",
            "parts": [
                {"text_en": "get", "meaning_ru": "получить"},
                {"text_en": "attribute", "meaning_ru": "атрибут / свойство"}
            ],
            "explanation_ru": "Получение атрибута объекта по строковому ключу."
        },
        "pronunciation": {
            "spoken_en": "get attr",
            "ipa": None,
            "ru_hint": "гет аттр",
            "verification": "human_verified"
        },
        "examples": [
            {
                "example_id": "get_attr_name",
                "en": "Get the attribute by its name.",
                "ru": "Получи атрибут по его имени."
            },
            {
                "example_id": "safe_default_attr",
                "en": "Use getattr with a default value to avoid an attribute error.",
                "ru": "Используй getattr со значением по умолчанию, чтобы избежать ошибки атрибута."
            }
        ],
        "practice": {
            "enabled_templates": ["en_to_ru", "ru_to_en", "listening", "cloze", "spelling"],
            "production_prompt_ru": "Встроенная функция Python: безопасно получить атрибут объекта по строковому имени",
            "accepted_answers": ["getattr", "getattr()"],
            "cloze": {
                "example_id": "get_attr_name",
                "target": "attribute"
            }
        },
        "technical": {
            "api": "getattr",
            "python_version": "3.12",
            "example_kind": "standalone",
            "code": "class Order:\n    total_weight = 12.5\n\norder = Order()\nassert getattr(order, 'total_weight', 0.0) == 12.5\nassert getattr(order, 'missing_weight', 0.0) == 0.0",
            "expected_output": "12.5, 0.0",
            "source_url": "https://docs.python.org/3.12/library/functions.html#getattr"
        },
        "qa": {
            "qa_status": "ready",
            "review_level": "automated",
            "reviewed_at": "2026-11-03T00:30:00Z",
            "issues": []
        }
    }
]
