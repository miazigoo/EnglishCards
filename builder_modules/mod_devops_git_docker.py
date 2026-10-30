"""
Модуль 11: Git, Docker, CI/CD и DevOps.
Команды версионирования кода, контейнеризация Docker и стратегии деплоя.
"""

ITEMS = [
    # Git Version Control
    ("commit", "фиксация изменений в истории Git", "git commit -m 'feat: add user auth' — сохраняет снимок проиндексированных изменений в репозиторий", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("branch", "ветка разработки в Git", "git checkout -b feature/orders — изолированная линия разработки для новой фичи или багфикса", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("checkout", "переключение веток или коммитов", "git checkout main (или git switch) — переключает рабочее дерево на указанную ветку", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("merge", "слияние одной ветки в другую", "git merge feature — объединяет историю коммитов фичи в целевую ветку", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("rebase", "перебазирование коммитов на свежую основу", "git rebase main — переносит ваши коммиты поверх свежей верхушки целевой ветки для чистой линейной истории", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("stash", "временное сохранение незакоммиченных правок", "git stash / git stash pop — убирает текущие незавершенные правки в стек и очищает рабочую копию", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("cherry_pick", "выборочный перенос отдельного коммита", "git cherry-pick <commit-hash> — применяет изменения одного точечного коммита в текущую ветку", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("fetch", "скачивание свежих ссылок с удаленного сервера", "git fetch origin — загружает новые коммиты и ветки из remote без автоматического слияния", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("pull", "скачивание и слияние изменений в текущую ветку", "git pull origin main — выполняет git fetch, а затем git merge (или rebase) в текущую ветку", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("push", "отправка локальных коммитов на сервер", "git push origin main — загружает локальные коммиты в удаленный репозиторий (GitHub/GitLab)", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("clone", "полное клонирование репозитория на диск", "git clone <url> — копирует удаленный репозиторий со всей историей на локальную машину", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("fork", "персональная копия чужого репозитория", "fork — создание копии публичного репозитория в свой аккаунт для отправки Pull Request", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("tag", "именованная метка версии/релиза", "git tag -a v1.2.0 -m 'Release 1.2.0' — фиксирует неизменяемую точку в истории для релиза", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("diff", "просмотр различий между файлами/коммитами", "git diff HEAD~1 — показывает построчные добавления (+) и удаления (-) кода", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("blame", "построчный автор изменений файла", "git blame app/views.py — показывает, кто, когда и каким коммитом изменил каждую строку", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("reset", "сброс состояния индекса или коммитов", "git reset --hard HEAD~1 — отменяет коммит и физически стирает незакоммиченные файлы", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("revert", "отмена коммита созданием обратного", "git revert <hash> — создает новый коммит, зеркально отменяющий изменения без переписывания истории", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("squash", "схлопывание нескольких коммитов в один", "squash — объединение десятка промежуточных коммитов в один чистый при слиянии PR", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("amend", "дополнение последнего коммита", "git commit --amend --no-edit — добавляет забытые файлы в самый последний коммит без создания нового", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("conflict", "конфликт слияния веток в коде", "merge conflict — ситуация, когда в двух ветках отредактирована одна и та же строка кода", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("fast_forward", "перемотка ветки без коммита слияния", "Fast-Forward merge — простое перемещение указателя ветки вперед, если не было расхождений", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("origin", "стандартное имя удаленного репозитория", "origin — псевдоним удаленного сервера (URL), откуда был склонирован проект", "Git, Docker, CI/CD и DevOps", "git-core"),
    ("head", "указатель на текущий коммит/ветку", "HEAD — символическая ссылка на коммит, на котором сейчас находится рабочая копия", "Git, Docker, CI/CD и DevOps", "git-core"),

    # Docker & Containers
    ("dockerfile", "сценарий сборки Docker образа", "Dockerfile — файл инструкций (FROM, RUN, COPY, CMD) для сборки легковесного образа", "Git, Docker, CI/CD и DevOps", "docker-core"),
    ("image", "неизменяемый образ контейнера", "Docker Image — скомпилированный шаблон файловой системы с кодом и зависимостями", "Git, Docker, CI/CD и DevOps", "docker-core"),
    ("container", "изолированный работающий инстанс образа", "Docker Container — изолированный процесс в Linux namespaces и cgroups, запущенный из образа", "Git, Docker, CI/CD и DevOps", "docker-core"),
    ("volume", "постоянный том данных контейнера", "docker run -v pg_data:/var/lib/postgresql/data — хранилище на хосте, сохраняющее данные после удаления контейнера", "Git, Docker, CI/CD и DevOps", "docker-core"),
    ("network", "виртуальная сеть между контейнерами", "docker network create app-net — изолированная bridge-сеть для общения контейнеров по DNS именам", "Git, Docker, CI/CD и DevOps", "docker-core"),
    ("docker_compose", "оркестрация многоконтейнерного стека", "docker compose up -d — поднимает весь стек (web + db + redis + celery) из одного yaml файла", "Git, Docker, CI/CD и DevOps", "docker-core"),
    ("multi_stage_build", "многоэтапная сборка Docker образа", "FROM python as builder ... FROM python-slim — минимизирует финальный размер образа, исключая компиляторы", "Git, Docker, CI/CD и DevOps", "docker-core"),
    ("entrypoint", "главная стартовая команда контейнера", "ENTRYPOINT ['python', 'manage.py'] — фиксированный исполняемый файл, принимающий параметры из CMD", "Git, Docker, CI/CD и DevOps", "docker-core"),
    ("cmd", "аргументы команды по умолчанию в контейнере", "CMD ['runserver', '0.0.0.0:8000'] — параметры по умолчанию для ENTRYPOINT, которые можно переопределить", "Git, Docker, CI/CD и DevOps", "docker-core"),
    ("port_mapping", "проброс порта из контейнера на хост", "ports: ['8000:8000'] — связывает внешний порт физического сервера с внутренним портом контейнера", "Git, Docker, CI/CD и DevOps", "docker-core"),
    ("restart_policy", "политика перезапуска при падении", "restart: unless-stopped — указывает демону Docker перезапускать контейнер при непредвиденном падении", "Git, Docker, CI/CD и DevOps", "docker-core"),
    ("healthcheck", "инструкция проверки здоровья контейнера", "HEALTHCHECK --interval=30s CMD curl -f http://localhost:8000/healthz — проверяет готовность сервиса", "Git, Docker, CI/CD и DevOps", "docker-core"),
    ("registry", "реестр хранения Docker образов", "Container Registry (Docker Hub, Harbor, ECR) — удаленный сервер для хранения и скачивания образов", "Git, Docker, CI/CD и DevOps", "docker-core"),

    # CI/CD & Deploy
    ("ci_pipeline", "конвейер непрерывной интеграции (CI)", "CI Pipeline — автоматический запуск линтеров (flake8), проверки типов (mypy) и тестов на каждый коммит", "Git, Docker, CI/CD и DevOps", "cicd-core"),
    ("cd_pipeline", "конвейер непрерывной доставки/деплоя (CD)", "CD Pipeline — автоматическая сборка Docker-образа и выкатка релиза на тестовый или боевой сервер", "Git, Docker, CI/CD и DevOps", "cicd-core"),
    ("runner", "агент выполнения задач CI/CD", "GitLab Runner / GitHub Actions Runner — процесс на сервере, исполняющий шаги скрипта из .gitlab-ci.yml", "Git, Docker, CI/CD и DevOps", "cicd-core"),
    ("blue_green_deployment", "деплой синий/зеленый без даунтайма", "Blue-Green Deploy — параллельно поднимается новая версия (Green), после чего роутер мгновенно переключает трафик со старой (Blue)", "Git, Docker, CI/CD и DevOps", "cicd-core"),
    ("canary_deployment", "канареечный деплой на 5% пользователей", "Canary Deploy — выкатка новой версии на небольшую долю аудитории для проверки стабильности на боевых метриках", "Git, Docker, CI/CD и DevOps", "cicd-core"),
    ("rolling_update", "плавное поэтапное обновление подов", "Rolling Update — обновление контейнеров по одному с ожиданием прохождения Healthcheck без остановки сервиса", "Git, Docker, CI/CD и DevOps", "cicd-core"),
]
