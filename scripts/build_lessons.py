#!/usr/bin/env python3
"""
scripts/build_lessons.py

Generates 12 high-quality micro-lessons conforming to Section 7.3 of GEMINI_TECH_SPEC_ENGLISH_V3.md.
Each lesson includes topic, rules, authentic examples with highlights, and exactly 3 exercises.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LESSONS_DIR = BASE_DIR / "content/lessons"

LESSONS = [
    {
        "lesson_id": "lesson_01_articles_tech",
        "title_ru": "Артикли в техническом контексте (a / an vs the)",
        "topic": "articles",
        "duration_minutes": 3,
        "rule_ru": "Используйте 'a/an' при первом упоминании любого представителя класса (например, 'a server' = какой-то сервер, один из серверов). Используйте 'the', когда речь идет о конкретном объекте, известном собеседникам ('the database' = наша рабочая БД проекта). С неисчисляемыми ('code', 'data') артикль 'a' не используется.",
        "examples": [
            {"en": "We deployed a new server yesterday.", "ru": "Вчера мы развернули новый сервер (один из).", "highlight": "a new server"},
            {"en": "The server stopped responding to requests.", "ru": "Сервер перестал отвечать на запросы (тот самый конкретный).", "highlight": "The server"},
            {"en": "We wrote clean code without any errors.", "ru": "Мы написали чистый код без ошибок (code неисчисляемое, без 'a').", "highlight": "clean code"}
        ],
        "exercises": [
            {
                "exercise_id": "ex_01",
                "type": "choice",
                "prompt": "I noticed ___ memory leak in the worker service.",
                "options": ["a", "the", "an", "— (no article)"],
                "answer": "a",
                "explanation": "'memory leak' — исчисляемое существительное, упоминается впервые, начинается с согласного звука 'm'."
            },
            {
                "exercise_id": "ex_02",
                "type": "choice",
                "prompt": "Please verify ___ production database connection string.",
                "options": ["the", "a", "an", "— (no article)"],
                "answer": "the",
                "explanation": "Речь идет о конкретной базе данных проекта (production database), поэтому нужен определенный артикль 'the'."
            },
            {
                "exercise_id": "ex_03",
                "type": "choice",
                "prompt": "We need to parse all incoming ___ from the sensor.",
                "options": ["data", "a data", "the datas", "an data"],
                "answer": "data",
                "explanation": "'Data' в английском неисчисляемое существительное и не употребляется с артиклем 'a'."
            }
        ]
    },
    {
        "lesson_id": "lesson_02_countability",
        "title_ru": "Исчисляемые и неисчисляемые существительные: Data, Code, Information",
        "topic": "countability",
        "duration_minutes": 3,
        "rule_ru": "Слова 'information', 'code', 'data', 'hardware', 'software' в техническом английском языке являются неисчисляемыми. Они не имеют множественного числа с окончанием -s и не используются с 'a/an'. Чтобы посчитать, говорят: 'a piece of code', 'a snippet', 'an item of data'.",
        "examples": [
            {"en": "This information is very helpful for debugging.", "ru": "Эта информация очень полезна для отладки.", "highlight": "This information is"},
            {"en": "We reviewed multiple lines of code.", "ru": "Мы просмотрели множество строк кода.", "highlight": "lines of code"}
        ],
        "exercises": [
            {
                "exercise_id": "ex_01",
                "type": "choice",
                "prompt": "Could you provide more ___ about this exception?",
                "options": ["information", "informations", "an information", "pieces information"],
                "answer": "information",
                "explanation": "Слово 'information' неисчисляемое, формы 'informations' не существует."
            },
            {
                "exercise_id": "ex_02",
                "type": "choice",
                "prompt": "We discovered several malicious ___ in the legacy repository.",
                "options": ["code snippets", "codes", "a code", "code fragmentses"],
                "answer": "code snippets",
                "explanation": "Для подсчета элементов кода используется составная фраза 'code snippets' или 'lines of code'."
            },
            {
                "exercise_id": "ex_03",
                "type": "choice",
                "prompt": "All telemetry ___ stored in ClickHouse.",
                "options": ["data is", "datas are", "a data is", "data are not"],
                "answer": "data is",
                "explanation": "В стандартном техническом английском 'data' согласуется с глаголом в единственном числе: 'data is'."
            }
        ]
    },
    {
        "lesson_id": "lesson_03_do_vs_make",
        "title_ru": "Глаголы Do vs Make в разработке ПО",
        "topic": "vocabulary_verbs",
        "duration_minutes": 3,
        "rule_ru": "'Do' используется для действий, процессов и рутинной работы: 'do research', 'do testing', 'do refactoring', 'do a task'. 'Make' используется, когда что-то создается или меняется: 'make a commit', 'make changes', 'make a decision', 'make an API call'.",
        "examples": [
            {"en": "We need to make changes to the authentication flow.", "ru": "Нам нужно внести изменения в поток аутентификации.", "highlight": "make changes"},
            {"en": "I will do the code review after the standup.", "ru": "Я проведу код-ревью после стендапа.", "highlight": "do the code review"}
        ],
        "exercises": [
            {
                "exercise_id": "ex_01",
                "type": "choice",
                "prompt": "Please ___ a new branch before modifying the migrations.",
                "options": ["make", "do", "execute to", "perform for"],
                "answer": "make",
                "explanation": "Создание чего-то нового (коммита, ветки, изменений) сочетается с глаголом 'make'."
            },
            {
                "exercise_id": "ex_02",
                "type": "choice",
                "prompt": "Our QA team will ___ performance testing tomorrow.",
                "options": ["do", "make", "create of", "build for"],
                "answer": "do",
                "explanation": "Проведение тестирования или анализа — это процесс/действие, поэтому используется 'do testing'."
            },
            {
                "exercise_id": "ex_03",
                "type": "choice",
                "prompt": "We need to ___ a quick decision on the database schema.",
                "options": ["make", "do", "take over", "put"],
                "answer": "make",
                "explanation": "Устойчивое выражение: 'make a decision' (принять решение)."
            }
        ]
    },
    {
        "lesson_id": "lesson_04_say_vs_tell",
        "title_ru": "Say vs Tell в коммуникации разработчиков",
        "topic": "vocabulary_verbs",
        "duration_minutes": 3,
        "rule_ru": "После глагола 'tell' ВСЕГДА следует адресат (кому говорят) БЕЗ предлога: 'Tell me the endpoint', 'He told the team'. После глагола 'say' адресат либо не указывается ('The logs say timeout'), либо используется с предлогом 'to' ('Say to them').",
        "examples": [
            {"en": "The tech lead told the team about the upcoming release.", "ru": "Техлид рассказал команде о предстоящем релизе.", "highlight": "told the team"},
            {"en": "The error message says that the port is already in use.", "ru": "Сообщение об ошибке говорит, что порт уже занят.", "highlight": "message says that"}
        ],
        "exercises": [
            {
                "exercise_id": "ex_01",
                "type": "choice",
                "prompt": "Could you ___ me where the configuration file is located?",
                "options": ["tell", "say", "say to", "speak"],
                "answer": "tell",
                "explanation": "Перед местоимением 'me' используется глагол 'tell' (tell me)."
            },
            {
                "exercise_id": "ex_02",
                "type": "choice",
                "prompt": "The compiler output ___ that variable 'count' is unused.",
                "options": ["says", "tells", "tells that", "talks"],
                "answer": "says",
                "explanation": "Когда адресат не указан (вывод сообщает, что...), используется 'says that'."
            },
            {
                "exercise_id": "ex_03",
                "type": "choice",
                "prompt": "Did the client ___ what features they need first?",
                "options": ["say", "tell", "spoke", "tell to"],
                "answer": "say",
                "explanation": "Без указания прямого адресата используется 'say'."
            }
        ]
    },
    {
        "lesson_id": "lesson_05_look_at_vs_look_for",
        "title_ru": "Фразовые глаголы с Look: Look at, Look for, Look into",
        "topic": "phrasal_verbs",
        "duration_minutes": 3,
        "rule_ru": "'Look at' = посмотреть/взглянуть на что-то видимое (код, экран, график). 'Look for' = искать что-то отсутствующее (баг, решение, документацию). 'Look into' = исследовать, детально расследовать проблему (инцидент, ошибку).",
        "examples": [
            {"en": "Look at the CPU utilization chart on Grafana.", "ru": "Взгляни на график загрузки процессора в Grafana.", "highlight": "Look at the CPU"},
            {"en": "I am looking for the API key in the .env file.", "ru": "Я ищу ключ API в файле .env.", "highlight": "looking for the API key"},
            {"en": "Our DevOps engineer is looking into the connection drop.", "ru": "Наш DevOps расследует сброс соединения.", "highlight": "looking into the connection"}
        ],
        "exercises": [
            {
                "exercise_id": "ex_01",
                "type": "choice",
                "prompt": "Please ___ this traceback on the terminal.",
                "options": ["look at", "look for", "look into to", "look after"],
                "answer": "look at",
                "explanation": "Взглянуть на видимый трейсбек на экране — 'look at'."
            },
            {
                "exercise_id": "ex_02",
                "type": "choice",
                "prompt": "The developers are ___ the root cause of the outage.",
                "options": ["looking into", "looking at for", "looking up to", "looking on"],
                "answer": "looking into",
                "explanation": "Расследовать первопричину инцидента — 'look into'."
            },
            {
                "exercise_id": "ex_03",
                "type": "choice",
                "prompt": "I spent two hours ___ a working example in the documentation.",
                "options": ["looking for", "looking at", "looking after", "looking on"],
                "answer": "looking for",
                "explanation": "Искать отсутствующий пример — 'look for'."
            }
        ]
    },
    {
        "lesson_id": "lesson_06_depend_on",
        "title_ru": "Управление глаголов: Depend on",
        "topic": "prepositions",
        "duration_minutes": 3,
        "rule_ru": "Глагол 'depend' ВСЕГДА требует предлога 'on' (или 'upon'), в отличие от русского 'зависеть от' (нельзя говорить 'depend of' или 'depend from'). То же самое относится к прилагательному 'dependent on'.",
        "examples": [
            {"en": "Our release date depends on the client's approval.", "ru": "Дата нашего релиза зависит от согласования клиента.", "highlight": "depends on"},
            {"en": "This microservice depends on Redis for caching.", "ru": "Этот микросервис зависит от Redis для кэширования.", "highlight": "depends on Redis"}
        ],
        "exercises": [
            {
                "exercise_id": "ex_01",
                "type": "choice",
                "prompt": "The query performance depends ___ the index configuration.",
                "options": ["on", "from", "of", "with"],
                "answer": "on",
                "explanation": "После depend всегда используется предлог on."
            },
            {
                "exercise_id": "ex_02",
                "type": "choice",
                "prompt": "Our payment module is heavily dependent ___ third-party webhooks.",
                "options": ["on", "of", "from", "at"],
                "answer": "on",
                "explanation": "Прилагательное 'dependent' также управляется предлогом 'on'."
            },
            {
                "exercise_id": "ex_03",
                "type": "choice",
                "prompt": "Whether we use Celery depends ___ the volume of background tasks.",
                "options": ["on", "from", "in", "by"],
                "answer": "on",
                "explanation": "Зависеть от чего-то — всегда 'depend on'."
            }
        ]
    },
    {
        "lesson_id": "lesson_07_modals_must_should",
        "title_ru": "Модальные глаголы: Must, Have to, Should",
        "topic": "modal_verbs",
        "duration_minutes": 3,
        "rule_ru": "'Must' выражает строгое требование или внутреннюю уверенность: 'Passwords must contain at least 8 characters'. 'Have to' выражает внешнюю необходимость: 'I have to fix this bug before 5 PM'. 'Should' выражает рекомендацию: 'You should optimize this query' (Вам следует оптимизировать этот запрос).",
        "examples": [
            {"en": "All API endpoints must be covered with tests.", "ru": "Все эндпоинты API обязаны быть покрыты тестами.", "highlight": "must be covered"},
            {"en": "You should use select_related to avoid N+1 queries.", "ru": "Вам следует использовать select_related, чтобы избежать N+1 запросов.", "highlight": "You should use"}
        ],
        "exercises": [
            {
                "exercise_id": "ex_01",
                "type": "choice",
                "prompt": "It's just a best practice recommendation: you ___ add type hints.",
                "options": ["should", "must", "have to", "are forced to"],
                "answer": "should",
                "explanation": "Для мягкой рекомендации лучшей практики используется 'should'."
            },
            {
                "exercise_id": "ex_02",
                "type": "choice",
                "prompt": "According to GDPR regulations, we ___ encrypt all user passwords.",
                "options": ["must", "should", "might", "could"],
                "answer": "must",
                "explanation": "Для строгих юридических и архитектурных требований используется 'must'."
            },
            {
                "exercise_id": "ex_03",
                "type": "choice",
                "prompt": "The server room is locked, so I ___ ask the sysadmin for access.",
                "options": ["have to", "should", "ought", "might"],
                "answer": "have to",
                "explanation": "Вынужденная внешняя необходимость описывается модальной конструкцией 'have to'."
            }
        ]
    },
    {
        "lesson_id": "lesson_08_polite_requests",
        "title_ru": "Вежливые просьбы в деловой переписке (Could you...)",
        "topic": "communication",
        "duration_minutes": 3,
        "rule_ru": "Вместо резкого повелительного наклонения ('Fix this bug!') в англоязычных командах принято использовать вежливые обороты: 'Could you please check this endpoint?' или 'Would you mind reviewing my pull request?'. Обратите внимание: после 'Would you mind' используется глагол с окончанием -ing ('reviewing').",
        "examples": [
            {"en": "Could you please clarify the acceptance criteria?", "ru": "Не могли бы вы уточнить критерии приемки?", "highlight": "Could you please clarify"},
            {"en": "Would you mind testing this on staging?", "ru": "Не будете ли вы против протестировать это на стейджинге?", "highlight": "Would you mind testing"}
        ],
        "exercises": [
            {
                "exercise_id": "ex_01",
                "type": "choice",
                "prompt": "Would you mind ___ the server logs for yesterday?",
                "options": ["checking", "check", "to check", "checked"],
                "answer": "checking",
                "explanation": "После конструкции 'Would you mind' глагол всегда идет в герундии с -ing."
            },
            {
                "exercise_id": "ex_02",
                "type": "choice",
                "prompt": "Could you please ___ me permissions to the production cluster?",
                "options": ["grant", "granting", "to grant", "granted"],
                "answer": "grant",
                "explanation": "После модального глагола 'Could you please' используется инфинитив без частицы to ('grant')."
            },
            {
                "exercise_id": "ex_03",
                "type": "choice",
                "prompt": "Would you mind ___ this migration during the maintenance window?",
                "options": ["running", "run", "to run", "ran"],
                "answer": "running",
                "explanation": "После 'Would you mind' требуется герундий (-ing)."
            }
        ]
    },
    {
        "lesson_id": "lesson_09_negations_traps",
        "title_ru": "Ловушки отрицания: Neither... Nor и двойное отрицание",
        "topic": "grammar_negations",
        "duration_minutes": 3,
        "rule_ru": "В правильном английском языке не используется двойное отрицание (нельзя сказать 'I don't know nothing'). Используйте 'I don't know anything' или 'I know nothing'. Парный союз 'neither ... nor' означает 'ни ... ни': 'Neither CPU nor memory was overloaded'.",
        "examples": [
            {"en": "The query returned no results.", "ru": "Запрос не вернул результатов (одно отрицание 'no').", "highlight": "returned no results"},
            {"en": "Neither Redis nor PostgreSQL threw an exception.", "ru": "Ни Redis, ни PostgreSQL не выбросили исключение.", "highlight": "Neither Redis nor PostgreSQL"}
        ],
        "exercises": [
            {
                "exercise_id": "ex_01",
                "type": "choice",
                "prompt": "The test didn't find ___ errors in the module.",
                "options": ["any", "no", "none", "nothing"],
                "answer": "any",
                "explanation": "Поскольку уже есть 'didn't', используется 'any', а не 'no'."
            },
            {
                "exercise_id": "ex_02",
                "type": "choice",
                "prompt": "Neither the primary database ___ the replica responded to the ping.",
                "options": ["nor", "or", "and", "neither"],
                "answer": "nor",
                "explanation": "Парный союз отрицания всегда строится как 'neither ... nor'."
            },
            {
                "exercise_id": "ex_03",
                "type": "choice",
                "prompt": "We have ___ received the confirmation email yet.",
                "options": ["not", "no", "never", "nothing"],
                "answer": "not",
                "explanation": "С глаголом Present Perfect используется отрицательная частица 'not': 'have not received'."
            }
        ]
    },
    {
        "lesson_id": "lesson_10_question_inversion",
        "title_ru": "Порядок слов в вопросах (Question Inversion)",
        "topic": "grammar_questions",
        "duration_minutes": 3,
        "rule_ru": "В прямых вопросах вспомогательный глагол выносится перед подлежащим: 'Why did the worker crash?', 'How does this cache work?'. Однако в косвенных вопросах порядок слов становится прямым: 'Do you know why the worker crashed?' (НЕ 'why did the worker crash').",
        "examples": [
            {"en": "When will the deployment finish?", "ru": "Когда завершится развертывание?", "highlight": "When will the deployment"},
            {"en": "Can you explain how this algorithm works?", "ru": "Ты можешь объяснить, как работает этот алгоритм? (прямой порядок в придаточном)", "highlight": "how this algorithm works"}
        ],
        "exercises": [
            {
                "exercise_id": "ex_01",
                "type": "choice",
                "prompt": "Do you know where ___ the configuration file?",
                "options": ["we can find", "can we find", "did we find", "find we"],
                "answer": "we can find",
                "explanation": "В косвенном вопросе (после 'Do you know where...') сохраняется прямой порядок слов подлежащее + сказуемое."
            },
            {
                "exercise_id": "ex_02",
                "type": "choice",
                "prompt": "Why ___ the staging pipeline fail this morning?",
                "options": ["did", "was", "does", "had"],
                "answer": "did",
                "explanation": "В прямом вопросе в Past Simple требуется вспомогательный глагол 'did'."
            },
            {
                "exercise_id": "ex_03",
                "type": "choice",
                "prompt": "Could you tell me what the current CPU load ___?",
                "options": ["is", "is it", "does it", "be"],
                "answer": "is",
                "explanation": "В косвенном вопросе глагол ставится в конец: 'what the current CPU load is'."
            }
        ]
    },
    {
        "lesson_id": "lesson_11_tenses_work",
        "title_ru": "Времена Past Simple vs Present Perfect в баг-репортах",
        "topic": "tenses",
        "duration_minutes": 3,
        "rule_ru": "Используйте Past Simple для действий, завершенных в конкретный момент в прошлом ('We deployed v2.1 yesterday at 14:00'). Используйте Present Perfect, когда важен результат для настоящего момента без указания точного времени ('We have fixed the memory leak' = утечка исправлена и сейчас сервер работает стабильно).",
        "examples": [
            {"en": "I merged the pull request ten minutes ago.", "ru": "Я влил пул-реквест десять минут назад (точное время в прошлом — Past Simple).", "highlight": "merged the pull request"},
            {"en": "The team has released a hotfix for the security vulnerability.", "ru": "Команда выпустила хотфикс (результат налицо — Present Perfect).", "highlight": "has released a hotfix"}
        ],
        "exercises": [
            {
                "exercise_id": "ex_01",
                "type": "choice",
                "prompt": "We ___ our database schema three days ago.",
                "options": ["migrated", "have migrated", "migrate", "were migrated"],
                "answer": "migrated",
                "explanation": "Маркер 'three days ago' указывает на конкретное время в прошлом, требуется Past Simple."
            },
            {
                "exercise_id": "ex_02",
                "type": "choice",
                "prompt": "The developers ___ already resolved the connection issue.",
                "options": ["have", "did", "had been", "were"],
                "answer": "have",
                "explanation": "Маркер 'already' с причастием 'resolved' требует Present Perfect: 'have resolved'."
            },
            {
                "exercise_id": "ex_03",
                "type": "choice",
                "prompt": "The server ___ at midnight yesterday.",
                "options": ["crashed", "has crashed", "is crashing", "crashes"],
                "answer": "crashed",
                "explanation": "Указание конкретного времени 'at midnight yesterday' требует Past Simple ('crashed')."
            }
        ]
    },
    {
        "lesson_id": "lesson_12_connectives",
        "title_ru": "Логические связки в технической документации (However, Therefore)",
        "topic": "connectives",
        "duration_minutes": 3,
        "rule_ru": "'However' (однако, тем не менее) выделяется запятыми и вводит противопоставление: 'The test passed; however, latency increased'. 'Therefore' (следовательно, поэтому) выражает логический вывод: 'Traffic doubled, therefore we scaled the cluster'. 'Although' (хотя) соединяет зависимое предложение без точки с запятой.",
        "examples": [
            {"en": "The query is fast; however, it consumes too much RAM.", "ru": "Запрос быстрый, однако он потребляет слишком много оперативной памяти.", "highlight": "however, it consumes"},
            {"en": "The node failed health checks, therefore traffic was rerouted.", "ru": "Узел не прошел проверку здоровья, поэтому трафик был перенаправлен.", "highlight": "therefore traffic was rerouted"}
        ],
        "exercises": [
            {
                "exercise_id": "ex_01",
                "type": "choice",
                "prompt": "The build succeeded; ___, we cannot deploy without QA approval.",
                "options": ["however", "because", "although", "so that"],
                "answer": "however",
                "explanation": "'However' используется для контраста между независимыми предложениями и выделяется запятой."
            },
            {
                "exercise_id": "ex_02",
                "type": "choice",
                "prompt": "Disk usage reached 95%, ___ the monitoring service triggered a critical alert.",
                "options": ["therefore", "despite", "although", "whereas"],
                "answer": "therefore",
                "explanation": "'Therefore' выражает прямое логическое следствие из предыдущего факта."
            },
            {
                "exercise_id": "ex_03",
                "type": "choice",
                "prompt": "___ the database was under high load, latency remained acceptable.",
                "options": ["Although", "However", "Therefore", "In order to"],
                "answer": "Although",
                "explanation": "'Although' присоединяет придаточное уступки: 'Хотя база данных была под высокой нагрузкой...'."
            }
        ]
    }
]

def build():
    LESSONS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Building {len(LESSONS)} micro-lessons in {LESSONS_DIR}...")
    for lesson in LESSONS:
        fname = f"{lesson['lesson_id']}.json"
        path = LESSONS_DIR / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(lesson, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Written {fname}")
    print("All 12 micro-lessons built successfully!")

if __name__ == "__main__":
    build()
