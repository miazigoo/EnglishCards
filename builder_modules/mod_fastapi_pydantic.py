"""
Модуль 3: FastAPI, Pydantic v2, схемы валидации и внедрение зависимостей.
Каждый термин снабжен конкретным объяснением работы в коде API.
"""

ITEMS = [
    # FastAPI Core & Routing
    ("FastAPI", "главный экземпляр приложения API", "FastAPI(title='App', docs_url='/docs') — корневой экземпляр веб-приложения ASGI", "FastAPI, Pydantic и валидация", "fastapi-core"),
    ("APIRouter", "модульный маршрутизатор эндпоинтов", "APIRouter(prefix='/api/v1', tags=['users']) — группирует маршруты модуля для include_router()", "FastAPI, Pydantic и валидация", "fastapi-core"),
    ("include_router()", "подключение дочернего роутера", "app.include_router(router) — регистрирует группу маршрутов в основном приложении", "FastAPI, Pydantic и валидация", "fastapi-core"),
    ("lifespan", "менеджер жизненного цикла приложения", "@asynccontextmanager async def lifespan(app) — управляет запуском и остановкой (startup/shutdown)", "FastAPI, Pydantic и валидация", "fastapi-core"),
    ("add_middleware()", "регистрация промежуточного слоя", "app.add_middleware(CORSMiddleware, ...) — добавляет слой обработки входящих и исходящих запросов", "FastAPI, Pydantic и валидация", "fastapi-core"),
    ("CORSMiddleware", "настройка политики CORS", "CORSMiddleware(allow_origins=['*']) — разрешает кросс-доменные запросы из браузера", "FastAPI, Pydantic и валидация", "fastapi-middleware"),
    ("exception_handler", "пользовательский обработчик ошибок", "@app.exception_handler(CustomError) — перехватывает исключение и возвращает красивый JSONResponse", "FastAPI, Pydantic и валидация", "fastapi-core"),

    # FastAPI Request Parameters (DI & Specs)
    ("Depends()", "внедрение зависимости (DI)", "Depends(get_db) — механизм Dependency Injection: выполняет функцию/класс и передает результат в эндпоинт", "FastAPI, Pydantic и валидация", "fastapi-di"),
    ("Security()", "внедрение зависимости с правами (Scopes)", "Security(get_current_user, scopes=['admin']) — внедряет зависимость авторизации с проверкой прав", "FastAPI, Pydantic и валидация", "fastapi-security"),
    ("Query()", "параметр строки запроса URL", "Query(default=1, ge=1, le=100) — объявляет и валидирует query-параметр из URL (?page=1)", "FastAPI, Pydantic и валидация", "fastapi-params"),
    ("Path()", "параметр пути в маршруте URL", "Path(..., description='ID объекта') — объявляет и валидирует параметр внутри пути (/items/{item_id})", "FastAPI, Pydantic и валидация", "fastapi-params"),
    ("Body()", "тело JSON запроса", "Body(..., embed=True) — указывает, что параметр должен быть извлечен из тела входящего JSON-запроса", "FastAPI, Pydantic и валидация", "fastapi-params"),
    ("Header()", "заголовок HTTP запроса", "Header(default=None, alias='X-Token') — автоматически извлекает значение из заголовков HTTP", "FastAPI, Pydantic и валидация", "fastapi-params"),
    ("Cookie()", "куки HTTP запроса", "Cookie(default=None) — автоматически извлекает значение куки из входящего запроса", "FastAPI, Pydantic и валидация", "fastapi-params"),
    ("Form()", "поле данных HTML формы", "Form(...) — принимает данные из формы 'application/x-www-form-urlencoded'", "FastAPI, Pydantic и валидация", "fastapi-params"),
    ("File()", "загрузка сырого бинарного файла", "File(...) — принимает загружаемый файл в виде байтов (bytes)", "FastAPI, Pydantic и валидация", "fastapi-params"),
    ("UploadFile", "потоковый объект загружаемого файла", "UploadFile — файловый дескриптор со сполнером памяти на диск, методами read(), write(), seek()", "FastAPI, Pydantic и валидация", "fastapi-params"),

    # FastAPI Responses & Background
    ("HTTPException", "выброс HTTP ошибки клиенту", "raise HTTPException(status_code=404, detail='Not found') — немедленно прерывает запрос с кодом и текстом", "FastAPI, Pydantic и валидация", "fastapi-response"),
    ("status", "константы кодов состояния HTTP", "status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST — читаемые константы статус-кодов", "FastAPI, Pydantic и валидация", "fastapi-response"),
    ("BackgroundTasks", "фоновые задачи после ответа", "background_tasks.add_task(send_email, to) — запускает выполнение функции сразу после отправки ответа клиенту", "FastAPI, Pydantic и валидация", "fastapi-background"),
    ("JSONResponse", "стандартный JSON ответ", "JSONResponse(status_code=200, content={'ok': True}) — возвращает прямой ответ в формате application/json", "FastAPI, Pydantic и валидация", "fastapi-response"),
    ("StreamingResponse", "потоковая отдача ответа клиенту", "StreamingResponse(generator(), media_type='text/event-stream') — отдает данные чанками без загрузки в память", "FastAPI, Pydantic и валидация", "fastapi-response"),
    ("FileResponse", "отдача локального файла на скачивание", "FileResponse(path, filename='report.pdf') — эффективно отдает файл с диска клиенту", "FastAPI, Pydantic и валидация", "fastapi-response"),
    ("RedirectResponse", "HTTP редирект на другой URL", "RedirectResponse(url='/login', status_code=303) — возвращает ответ с перенаправлением браузера", "FastAPI, Pydantic и валидация", "fastapi-response"),
    ("WebSocket", "двустороннее соединение реального времени", "async def ws_endpoint(ws: WebSocket) — объект постоянного полнодуплексного соединения", "FastAPI, Pydantic и валидация", "fastapi-ws"),
    ("WebSocketDisconnect", "разрыв WebSocket соединения", "except WebSocketDisconnect: — исключение, сигнализирующее о закрытии соединения клиентом", "FastAPI, Pydantic и валидация", "fastapi-ws"),

    # FastAPI Security
    ("OAuth2PasswordBearer", "извлечение Bearer токена из заголовка", "OAuth2PasswordBearer(tokenUrl='token') — схема авторизации: ищет токен в Authorization: Bearer <token>", "FastAPI, Pydantic и валидация", "fastapi-security"),
    ("OAuth2PasswordRequestForm", "стандартная форма логина и пароля", "OAuth2PasswordRequestForm = Depends() — принимает username, password и grant_type из формы", "FastAPI, Pydantic и валидация", "fastapi-security"),
    ("HTTPBearer", "проверка заголовка Bearer токена", "HTTPBearer() — простая схема авторизации по заголовку Authorization", "FastAPI, Pydantic и валидация", "fastapi-security"),

    # Pydantic Core & Schemas
    ("BaseModel", "базовый класс схем данных Pydantic", "class UserSchema(BaseModel): — основа для всех моделей валидации, сериализации и OpenAPI-схем", "FastAPI, Pydantic и валидация", "pydantic-core"),
    ("Field()", "настройка валидации и метаданных поля", "Field(..., gt=0, max_length=50, description='Описание') — задает правила валидации и документацию поля", "FastAPI, Pydantic и валидация", "pydantic-core"),
    ("field_validator", "валидатор конкретного поля (v2)", "@field_validator('email') — метод проверки и трансформации значения отдельного поля модели", "FastAPI, Pydantic и валидация", "pydantic-validator"),
    ("model_validator", "валидатор всей модели целиком (v2)", "@model_validator(mode='after') — проверяет взаимосвязи между несколькими полями модели", "FastAPI, Pydantic и валидация", "pydantic-validator"),
    ("root_validator", "корневой валидатор (v1 синтаксис)", "@root_validator(pre=True) — валидатор всего словаря данных перед созданием модели (устаревает в v2)", "FastAPI, Pydantic и валидация", "pydantic-validator"),
    ("computed_field", "вычисляемое динамическое поле (v2)", "@computed_field @property def full_name(self) -> str: — добавляет геттер в сериализацию модели", "FastAPI, Pydantic и валидация", "pydantic-core"),
    ("ConfigDict", "словарь конфигурации модели (v2)", "model_config = ConfigDict(from_attributes=True, populate_by_name=True) — задает настройки поведения схемы", "FastAPI, Pydantic и валидация", "pydantic-core"),
    ("model_dump()", "преобразование модели в Python словарь (v2)", "user.model_dump(exclude_unset=True) — сериализует экземпляр модели в стандартный Python dict", "FastAPI, Pydantic и валидация", "pydantic-methods"),
    ("model_dump_json()", "сериализация модели в JSON строку (v2)", "user.model_dump_json(indent=2) — сериализует модель напрямую в JSON строку", "FastAPI, Pydantic и валидация", "pydantic-methods"),
    ("model_validate()", "создание модели из словаря/объекта (v2)", "User.model_validate(data_dict) — парсит и валидирует словарь или ORM-объект в экземпляр модели", "FastAPI, Pydantic и валидация", "pydantic-methods"),
    ("model_validate_json()", "создание модели из JSON строки (v2)", "User.model_validate_json(json_str) — парсит сырую JSON строку и валидирует модель", "FastAPI, Pydantic и валидация", "pydantic-methods"),
    ("model_construct()", "создание модели без валидации (v2)", "User.model_construct(**kwargs) — быстро создает инстанс без проверок валидатора (для скорости)", "FastAPI, Pydantic и валидация", "pydantic-methods"),
    ("model_copy()", "копирование модели с изменениями (v2)", "user.model_copy(update={'name': 'New'}) — создает копию экземпляра модели с заменой полей", "FastAPI, Pydantic и валидация", "pydantic-methods"),
    ("model_json_schema()", "генерация схемы OpenAPI в JSON (v2)", "User.model_json_schema() — возвращает спецификацию JSON Schema для модели", "FastAPI, Pydantic и валидация", "pydantic-methods"),
    ("PrivateAttr", "приватный атрибут вне схемы", "_cache = PrivateAttr(default=None) — поле для внутренних нужд модели, не попадающее в схему экспорта", "FastAPI, Pydantic и валидация", "pydantic-core"),
    ("AliasChoices", "альтернативные имена поля (алиасы)", "Field(validation_alias=AliasChoices('user_name', 'username')) — принимает поле под разными именами", "FastAPI, Pydantic и валидация", "pydantic-core"),

    # Pydantic Special Field Types
    ("EmailStr", "валидный email адрес", "EmailStr — тип поля, проверяющий корректность структуры адреса электронной почты", "FastAPI, Pydantic и валидация", "pydantic-types"),
    ("HttpUrl", "валидный HTTP/HTTPS URL адрес", "HttpUrl — проверяет протокол http/https и валидность структуры веб-адреса", "FastAPI, Pydantic и валидация", "pydantic-types"),
    ("SecretStr", "скрытая строка для паролей и ключей", "SecretStr — скрывает строковое значение от отображения в логах и сериализации (str(val) -> '**********')", "FastAPI, Pydantic и валидация", "pydantic-types"),
    ("PositiveInt", "строго положительное целое число", "PositiveInt — ограничивает значение целым числом больше нуля (x > 0)", "FastAPI, Pydantic и валидация", "pydantic-types"),
    ("NonNegativeInt", "неотрицательное целое число", "NonNegativeInt — допускает целые числа от нуля и выше (x >= 0)", "FastAPI, Pydantic и валидация", "pydantic-types"),
    ("UUID4", "идентификатор формата UUIDv4", "UUID4 — валидирует 128-битный UUID четвертой версии", "FastAPI, Pydantic и валидация", "pydantic-types"),
    ("AwareDatetime", "дата и время строго с таймзоной", "AwareDatetime — требует обязательного указания временной зоны (tzinfo)", "FastAPI, Pydantic и валидация", "pydantic-types"),
    ("StrictBool", "строгий булевый тип без приведения", "StrictBool — принимает строго True или False (запрещает 1, 0, 'true')", "FastAPI, Pydantic и валидация", "pydantic-types"),
    ("StrictStr", "строгий строковый тип", "StrictStr — принимает только тип str без автоматического каста чисел", "FastAPI, Pydantic и валидация", "pydantic-types"),
    ("StrictInt", "строгий целочисленный тип", "StrictInt — принимает только int без округления float значений", "FastAPI, Pydantic и валидация", "pydantic-types"),
]
