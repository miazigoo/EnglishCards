"""
Модуль 10: Тестирование, Mocking и Pytest.
Концепции фикстур, моков, ассертов и стратегий тестирования бэкенда.
"""

ITEMS = [
    ("assert", "инструкция проверки условия в тестах", "assert actual == expected — ключевое слово Python для проверки истинности утверждения в тестах", "Тестирование, Mocking и Pytest", "pytest-core"),
    ("fixture", "фикстура подготовки данных/окружения", "@pytest.fixture — функция, подготавливающая состояние базы или объекты перед тестом", "Тестирование, Mocking и Pytest", "pytest-core"),
    ("parametrize", "параметризация теста набором данных", "@pytest.mark.parametrize('inp, out', [(1, 2), (3, 4)]) — запуск одного теста с разными входными аргументами", "Тестирование, Mocking и Pytest", "pytest-core"),
    ("conftest", "корневой файл общих фикстур pytest", "conftest.py — специальный файл в корне или подпапке для автоматического расшаривания фикстур", "Тестирование, Mocking и Pytest", "pytest-core"),
    ("autouse", "автоматическое применение фикстуры", "@pytest.fixture(autouse=True) — фикстура запускается для каждого теста без явного указания в аргументах", "Тестирование, Mocking и Pytest", "pytest-core"),
    ("scope_function", "область действия на один тест", "scope='function' — фикстура пересоздается с нуля для каждого отдельного тестового метода (по умолчанию)", "Тестирование, Mocking и Pytest", "pytest-core"),
    ("scope_module", "область действия на весь модуль", "scope='module' — фикстура создается один раз для всего тестового файла и переиспользуется", "Тестирование, Mocking и Pytest", "pytest-core"),
    ("scope_session", "область действия на весь прогон тестов", "scope='session' — фикстура инициализируется один раз в самом начале (например, тестовая база данных)", "Тестирование, Mocking и Pytest", "pytest-core"),
    ("yield_fixture", "фикстура с teardown логикой очистки", "yield data; cleanup() — код до yield подготавливает данные, код после — очищает ресурсы после теста", "Тестирование, Mocking и Pytest", "pytest-core"),
    ("monkeypatch", "фикстура временной подмены атрибутов/ENV", "monkeypatch.setenv('KEY', 'val') / monkeypatch.setattr(...) — безопасная подмена на время теста", "Тестирование, Mocking и Pytest", "pytest-core"),
    ("tmp_path", "фикстура временной директории на диске", "def test_file(tmp_path: Path): — предоставляет чистую изолированную временную папку для теста", "Тестирование, Mocking и Pytest", "pytest-core"),
    ("capsys", "перехват вывода stdout и stderr", "out, err = capsys.readouterr() — перехватывает вывод print() для проверки текстовых логов консоли", "Тестирование, Mocking и Pytest", "pytest-core"),
    ("caplog", "перехват сообщений логирования logging", "assert 'Error' in caplog.text — проверяет записи, отправленные в стандартный модуль logging", "Тестирование, Mocking и Pytest", "pytest-core"),
    ("pytest_raises", "проверка выброса ожидаемого исключения", "with pytest.raises(ValueError): — проверяет, что блок кода выбрасывает указанную ошибку", "Тестирование, Mocking и Pytest", "pytest-core"),
    ("approx", "сравнение чисел с плавающей точкой", "assert 0.1 + 0.2 == pytest.approx(0.3) — сравнивает float числа с учетом допустимой погрешности", "Тестирование, Mocking и Pytest", "pytest-core"),
    ("pytest_mark_asyncio", "маркер асинхронного теста", "@pytest.mark.asyncio — позволяет объявлять тест как async def и использовать await внутри", "Тестирование, Mocking и Pytest", "pytest-mark"),
    ("pytest_mark_django_db", "разрешение доступа к БД Django", "@pytest.mark.django_db(transaction=True) — поднимает чистую тестовую транзакцию БД для теста", "Тестирование, Mocking и Pytest", "pytest-mark"),
    ("pytest_mark_skip", "пропуск выполнения теста", "@pytest.mark.skip(reason='...') — безусловно исключает тест из текущего прогона", "Тестирование, Mocking и Pytest", "pytest-mark"),
    ("pytest_mark_skipif", "пропуск теста по условию", "@pytest.mark.skipif(sys.platform == 'win32') — пропускает тест при выполнении булевого условия", "Тестирование, Mocking и Pytest", "pytest-mark"),
    ("pytest_mark_xfail", "ожидаемое падение теста", "@pytest.mark.xfail(reason='Bug #123') — помечает тест как падающий без срыва всего прогона в CI", "Тестирование, Mocking и Pytest", "pytest-mark"),

    # Mocking & unittest.mock
    ("mock", "имитация объекта / метода", "mock — объект, симулирующий поведение реального сервиса для изоляции тестируемого юнита", "Тестирование, Mocking и Pytest", "mock-core"),
    ("magic_mock", "мок с поддержкой магических методов", "MagicMock() — мок-класс с готовыми реализациями __len__, __iter__, __getitem__, __call__", "Тестирование, Mocking и Pytest", "mock-core"),
    ("patch", "декоратор подмены объекта в модуле", "@patch('app.services.send_email') — временно подменяет функцию или класс моком на время вызова", "Тестирование, Mocking и Pytest", "mock-core"),
    ("patch_object", "подмена атрибута конкретного экземпляра", "@patch.object(service, 'method') — подменяет метод у конкретного уже созданного объекта", "Тестирование, Mocking и Pytest", "mock-core"),
    ("return_value", "фиксированное возвращаемое значение мока", "mock_func.return_value = {'status': 'ok'} — указывает, что должен вернуть мок при вызове", "Тестирование, Mocking и Pytest", "mock-core"),
    ("side_effect", "динамический сайд-эффект или выброс ошибки", "mock_func.side_effect = TimeoutError() (или список/функция) — гибкое поведение при вызове", "Тестирование, Mocking и Pytest", "mock-core"),
    ("assert_called", "проверка факта вызова мока", "mock_func.assert_called() — падает с ошибкой, если мок не был вызван хотя бы один раз", "Тестирование, Mocking и Pytest", "mock-core"),
    ("assert_called_once", "проверка ровно одного вызова", "mock_func.assert_called_once() — проверяет, что вызов мока произошел строго один раз", "Тестирование, Mocking и Pytest", "mock-core"),
    ("assert_called_with", "проверка точных переданных аргументов", "mock_func.assert_called_with(user_id=42) — проверяет аргументы последнего вызова мока", "Тестирование, Mocking и Pytest", "mock-core"),
    ("assert_not_called", "проверка отсутствия вызовов", "mock_func.assert_not_called() — гарантирует, что мок ни разу не вызывался в ходе сценария", "Тестирование, Mocking и Pytest", "mock-core"),
    ("call_count", "счетчик совершенных вызовов мока", "assert mock_func.call_count == 3 — целочисленное количество раз, которое был вызван данный мок", "Тестирование, Mocking и Pytest", "mock-core"),

    # Testing Types & Strategies
    ("unit_test", "модульный тест отдельной функции", "unit test — тестирование изолированной функции или метода в отрыве от базы данных и сети", "Тестирование, Mocking и Pytest", "test-strategy"),
    ("integration_test", "интеграционный тест взаимодействия", "integration test — проверка совместной работы нескольких модулей (код + база данных + кэш)", "Тестирование, Mocking и Pytest", "test-strategy"),
    ("end_to_end_test", "сквозной E2E тест сценария", "E2E test — симуляция реального пользователя от клика на фронтенде до записи в БД", "Тестирование, Mocking и Pytest", "test-strategy"),
    ("regression_test", "регрессионный тест от поломок", "regression test — тест, написанный под найденный баг, предотвращающий его повторное появление", "Тестирование, Mocking и Pytest", "test-strategy"),
    ("smoke_test", "дымовой тест базовой работоспособности", "smoke test — быстрая проверка запуска сервиса и ответа эндпоинта /healthz перед релизом", "Тестирование, Mocking и Pytest", "test-strategy"),
    ("load_test", "нагрузочное тестирование производительности", "load test — симуляция сотен параллельных пользователей (Locust/k6) для замера предельного RPS", "Тестирование, Mocking и Pytest", "test-strategy"),
    ("dry_run", "тестовый прогон без реальных изменений", "dry_run=True — режим симуляции: скрипт логирует все планируемые действия, не меняя данные в БД", "Тестирование, Mocking и Pytest", "test-strategy"),
    ("code_coverage", "покрытие исходного кода тестами", "coverage run -m pytest — процент строк исходного кода программы, затронутых выполнением тестов", "Тестирование, Mocking и Pytest", "test-strategy"),
    ("branch_coverage", "покрытие ветвлений логики if/else", "branch coverage — метрика проверки того, что тесты прошли и по ветке if, и по ветке else", "Тестирование, Mocking и Pytest", "test-strategy"),
    ("factory_boy", "генератор тестовых моделей ORM", "UserFactory.create() — библиотека создания реалистичных моделей базы со случайными полями", "Тестирование, Mocking и Pytest", "test-strategy"),
    ("faker", "генератор реалистичных фейковых данных", "fake.name(), fake.email() — генерация правдоподобных адресов, имен и телефонов для тестов", "Тестирование, Mocking и Pytest", "test-strategy"),
]
