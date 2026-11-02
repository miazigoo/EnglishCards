# scripts/data_secondary_examples.py
"""Secondary contextual examples for 50 core vocabulary cards (Section 7.2, A07)."""

SECONDARY_EXAMPLES = {
    "reliable": {
        "example_id": "secondary_reliable_info",
        "en": "Always verify that you are receiving reliable information from the source.",
        "ru": "Всегда проверяйте, что получаете надежную информацию из источника."
    },
    "available": {
        "example_id": "secondary_available_slots",
        "en": "Are there any available time slots for the deployment review?",
        "ru": "Есть ли свободные слоты времени для ревью деплоя?"
    },
    "recent": {
        "example_id": "secondary_recent_graduates",
        "en": "We hired three recent graduates for our backend team.",
        "ru": "Мы наняли трех недавних выпускников в нашу бэкенд команду."
    },
    "similar": {
        "example_id": "secondary_similar_experience",
        "en": "Have you had similar experience with PostgreSQL replication?",
        "ru": "Был ли у вас похожий опыт с репликацией PostgreSQL?"
    },
    "efficient": {
        "example_id": "secondary_efficient_communication",
        "en": "Asynchronous standups enable efficient communication across timezones.",
        "ru": "Асинхронные стендапы обеспечивают эффективную коммуникацию между часовыми поясами."
    },
    "redundant": {
        "example_id": "secondary_redundant_hardware",
        "en": "We installed redundant power supplies in our server rack.",
        "ru": "Мы установили резервные (дублирующие) блоки питания в нашу серверную стойку."
    },
    "flexible": {
        "example_id": "secondary_flexible_schedule",
        "en": "Our engineering department offers a flexible working schedule.",
        "ru": "Наш инженерный отдел предлагает гибкий график работы."
    },
    "secure": {
        "example_id": "secondary_secure_connection",
        "en": "Always use TLS to maintain a secure connection to the database.",
        "ru": "Всегда используйте TLS для поддержания защищенного подключения к базе данных."
    },
    "scalable": {
        "example_id": "secondary_scalable_team",
        "en": "Clear processes build a scalable engineering organization.",
        "ru": "Понятные процессы создают масштабируемую инженерную организацию."
    },
    "robust": {
        "example_id": "secondary_robust_design",
        "en": "A robust system design prevents cascading failures across services.",
        "ru": "Надежный дизайн системы предотвращает каскадные сбои между сервисами."
    },
    "maintainable": {
        "example_id": "secondary_maintainable_tests",
        "en": "Keep test cases small and maintainable over the project lifecycle.",
        "ru": "Делайте тест-кейсы небольшими и поддерживаемыми на протяжении жизненного цикла проекта."
    },
    "consistent": {
        "example_id": "secondary_consistent_feedback",
        "en": "Consistent feedback during code reviews helps junior developers grow.",
        "ru": "Регулярная и последовательная обратная связь на код-ревью помогает расти джуниор разработчикам."
    },
    "accurate": {
        "example_id": "secondary_accurate_estimate",
        "en": "Can you provide an accurate estimate for completing the database schema?",
        "ru": "Можете ли вы предоставить точную оценку завершения схемы базы данных?"
    },
    "compatible": {
        "example_id": "secondary_compatible_browsers",
        "en": "The modern web client is compatible with all evergreen browsers.",
        "ru": "Современный веб-клиент совместим со всеми актуальными браузерами."
    },
    "critical": {
        "example_id": "secondary_critical_thinking",
        "en": "Critical thinking is necessary when evaluating architectural trade-offs.",
        "ru": "Критическое мышление необходимо при оценке архитектурных компромиссов."
    },
    "essential": {
        "example_id": "secondary_essential_tools",
        "en": "Git and Docker are essential tools for every modern programmer.",
        "ru": "Git и Docker — неотъемлемые инструменты каждого современного программиста."
    },
    "temporary": {
        "example_id": "secondary_temporary_fix",
        "en": "This workaround is a temporary fix until the upstream bug is resolved.",
        "ru": "Этот обходной путь — временное решение, пока баг в библиотеке не исправлен."
    },
    "permanent": {
        "example_id": "secondary_permanent_redirect",
        "en": "Use HTTP status 301 for a permanent redirect to the new domain.",
        "ru": "Используйте HTTP статус 301 для постоянного перенаправления на новый домен."
    },
    "urgent": {
        "example_id": "secondary_urgent_meeting",
        "en": "The team lead called an urgent meeting regarding the production outage.",
        "ru": "Тимлид созвал срочное совещание по поводу аварии в продакшене."
    },
    "resilient": {
        "example_id": "secondary_resilient_network",
        "en": "Deploying across multiple cloud zones creates a resilient infrastructure.",
        "ru": "Развертывание в нескольких облачных зонах создает устойчивую к сбоям инфраструктуру."
    },
    "transparent": {
        "example_id": "secondary_transparent_pricing",
        "en": "Our cloud provider offers transparent pricing without hidden fees.",
        "ru": "Наш облачный провайдер предлагает прозрачное ценообразование без скрытых комиссий."
    },
    "unless": {
        "example_id": "secondary_unless_instructed",
        "en": "Do not delete records from the audit table unless instructed by compliance.",
        "ru": "Не удаляйте записи из таблицы аудита, если только нет указания от комплаенса."
    },
    "otherwise": {
        "example_id": "secondary_otherwise_abort",
        "en": "All checks must pass; otherwise, abort the continuous deployment pipeline.",
        "ru": "Все проверки должны пройти успешно; в противном случае прервите пайплайн непрерывного деплоя."
    },
    "however": {
        "example_id": "secondary_however_slow",
        "en": "The query executes correctly; however, it remains too slow on large datasets.",
        "ru": "Запрос выполняется корректно; однако он остается слишком медленным на больших объемах данных."
    },
    "instead of": {
        "example_id": "secondary_instead_raw_sql",
        "en": "Use parameterized queries instead of string concatenation.",
        "ru": "Используйте параметризованные запросы вместо конкатенации строк."
    },
    "required": {
        "example_id": "secondary_required_skills",
        "en": "Experience with relational databases is required for this senior vacancy.",
        "ru": "Опыт работы с реляционными базами данных обязателен для этой сеньорной вакансии."
    },
    "optional": {
        "example_id": "secondary_optional_parameters",
        "en": "In Python, default arguments define optional parameters for a function.",
        "ru": "В Python аргументы по умолчанию определяют опциональные параметры функции."
    },
    "enumerate": {
        "example_id": "secondary_enumerate_lines",
        "en": "Enumerate the lines of the config file to print line numbers next to errors.",
        "ru": "Пронумеруйте строки конфигурационного файла, чтобы вывести номера строк рядом с ошибками."
    },
    "zip": {
        "example_id": "secondary_zip_dict",
        "en": "Pass zip output to the dict constructor to combine keys and values into a mapping.",
        "ru": "Передайте результат zip в конструктор dict, чтобы объединить ключи и значения в словарь."
    },
    "rsplit": {
        "example_id": "secondary_rsplit_email",
        "en": "Use rsplit on the email string to separate username from domain.",
        "ru": "Используйте rsplit для строки email, чтобы отделить имя пользователя от домена."
    },
    "issubclass": {
        "example_id": "secondary_issubclass_plugin",
        "en": "Verify with issubclass that dynamic plugins inherit from BasePlugin.",
        "ru": "Проверьте с помощью issubclass, что динамические плагины наследуются от BasePlugin."
    },
    "getattr": {
        "example_id": "secondary_getattr_serializer",
        "en": "Dynamic serializers use getattr to extract fields from model instances.",
        "ru": "Динамические сериализаторы используют getattr для извлечения полей из экземпляров моделей."
    },
    "filter": {
        "example_id": "secondary_filter_logs",
        "en": "Filter incoming log records to display only warnings and fatal errors.",
        "ru": "Отфильтруйте входящие записи логов, чтобы отобразить только предупреждения и фатальные ошибки."
    },
    "commit": {
        "example_id": "secondary_commit_transaction",
        "en": "Ensure you commit the database transaction only after external payment succeeds.",
        "ru": "Убедитесь, что фиксируете (commit) транзакцию в БД только после успеха внешнего платежа."
    },
    "rollback": {
        "example_id": "secondary_rollback_deployment",
        "en": "We can rollback the deployment in one click if health checks fail.",
        "ru": "Мы можем откатить деплой в один клик, если проверки работоспособности упадут."
    },
    "repository": {
        "example_id": "secondary_repository_pattern",
        "en": "The repository pattern abstracts database operations from domain business rules.",
        "ru": "Паттерн репозиторий абстрагирует операции с базой данных от бизнес-правил домена."
    },
    "adapter": {
        "example_id": "secondary_adapter_payment",
        "en": "Write an adapter class to integrate the third-party SMS notification service.",
        "ru": "Напишите класс-адаптер для интеграции стороннего сервиса SMS-уведомлений."
    },
    "middleware": {
        "example_id": "secondary_middleware_timing",
        "en": "Add timing middleware to record execution duration for every HTTP request.",
        "ru": "Добавьте промежуточное ПО (middleware) замера времени, чтобы фиксировать длительность каждого HTTP-запроса."
    },
    "payload": {
        "example_id": "secondary_payload_jwt",
        "en": "Store user identifier and assigned permissions inside the JWT payload.",
        "ru": "Сохраняйте идентификатор пользователя и назначенные права внутри полезной нагрузки (payload) JWT."
    },
    "dependency": {
        "example_id": "secondary_dependency_pinning",
        "en": "Pin exact dependency versions in your lockfile to ensure reproducible builds.",
        "ru": "Фиксируйте точные версии зависимостей в lock-файле для обеспечения воспроизводимости сборок."
    },
    "serialize": {
        "example_id": "secondary_serialize_cache",
        "en": "Serialize complex objects to JSON before saving them in the Redis cache.",
        "ru": "Сериализуйте сложные объекты в JSON перед сохранением их в кэше Redis."
    },
    "dispatch": {
        "example_id": "secondary_dispatch_event",
        "en": "Dispatch an asynchronous domain event whenever a new order is confirmed.",
        "ru": "Отправляйте (dispatch) асинхронное событие домена каждый раз, когда новый заказ подтвержден."
    },
    "authenticate": {
        "example_id": "secondary_authenticate_api_key",
        "en": "Authenticate incoming webhook requests using a cryptographic signature header.",
        "ru": "Аутентифицируйте входящие запросы вебхуков с помощью заголовка криптографической подписи."
    },
    "sanitize": {
        "example_id": "secondary_sanitize_html",
        "en": "Sanitize user-submitted HTML input to eliminate cross-site scripting risks.",
        "ru": "Очищайте (sanitize) введенный пользователем HTML, чтобы исключить риски XSS-атак."
    },
    "truncate": {
        "example_id": "secondary_truncate_table",
        "en": "Execute TRUNCATE TABLE to quickly purge temporary import data in PostgreSQL.",
        "ru": "Выполните TRUNCATE TABLE, чтобы быстро очистить временные данные импорта в PostgreSQL."
    },
    "paginate": {
        "example_id": "secondary_paginate_catalog",
        "en": "Always paginate product catalog endpoints to prevent out-of-memory errors.",
        "ru": "Всегда разбивайте эндпоинты каталога товаров на страницы (paginate), чтобы избежать ошибок нехватки памяти."
    },
    "immutable": {
        "example_id": "secondary_immutable_dataclass",
        "en": "Use frozen dataclasses to create immutable value objects in Python.",
        "ru": "Используйте frozen dataclass для создания неизменяемых (immutable) объектов-значений в Python."
    },
    "deprecated": {
        "example_id": "secondary_deprecated_warning",
        "en": "Issue a DeprecationWarning when callers invoke legacy API version one.",
        "ru": "Выдавайте DeprecationWarning, когда клиенты вызывают устаревшую версию API v1."
    },
    "cache": {
        "example_id": "secondary_cache_invalidation",
        "en": "Cache invalidation is notoriously one of the hardest problems in software engineering.",
        "ru": "Инвалидация кэша общеизвестно является одной из сложнейших задач в программной инженерии."
    },
    "asynchronous": {
        "example_id": "secondary_async_task",
        "en": "Delegate heavy video transcoding to an asynchronous Celery worker queue.",
        "ru": "Делегируйте тяжелое перекодирование видео в очередь асинхронных воркеров Celery."
    }
}
