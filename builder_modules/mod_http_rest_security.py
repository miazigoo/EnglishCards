"""
Модуль 9: HTTP, REST API, WebSockets и безопасность.
Статусы HTTP, методы, токены JWT, безопасность сессий и протокол WebSocket.
"""

ITEMS = [
    # HTTP Methods
    ("GET", "запрос на получение ресурса", "GET /api/users — безопасный и идемпотентный метод для чтения данных без изменения состояния на сервере", "HTTP, REST API и безопасность", "http-method"),
    ("POST", "создание нового ресурса", "POST /api/users — неидемпотентный метод отправки тела данных для создания новой записи", "HTTP, REST API и безопасность", "http-method"),
    ("PUT", "полная замена ресурса целиком", "PUT /api/users/1 — идемпотентный метод полной перезаписи всех полей ресурса", "HTTP, REST API и безопасность", "http-method"),
    ("PATCH", "частичное обновление полей ресурса", "PATCH /api/users/1 — обновление только тех полей, которые переданы в теле запроса", "HTTP, REST API и безопасность", "http-method"),
    ("DELETE", "удаление ресурса", "DELETE /api/users/1 — идемпотентный метод удаления указанного объекта с сервера", "HTTP, REST API и безопасность", "http-method"),
    ("OPTIONS", "запрос поддерживаемых методов (CORS preflight)", "OPTIONS /api — служебный запрос браузера для выяснения разрешенных сервером методов и заголовков", "HTTP, REST API и безопасность", "http-method"),
    ("HEAD", "чтение только заголовков ответа", "HEAD /file.zip — возвращает только метаданные и размер файла (Content-Length) без тела ответа", "HTTP, REST API и безопасность", "http-method"),

    # HTTP Status Codes
    ("ok_200", "200 OK — успешный запрос", "200 OK — стандартный ответ об успешном выполнении GET/PUT/PATCH запроса", "HTTP, REST API и безопасность", "http-status"),
    ("created_201", "201 Created — ресурс успешно создан", "201 Created — успешный ответ на POST запрос; часто возвращает созданный объект в теле", "HTTP, REST API и безопасность", "http-status"),
    ("accepted_202", "202 Accepted — принят в фоновую обработку", "202 Accepted — запрос принят, но будет выполнен асинхронно в очереди воркеров", "HTTP, REST API и безопасность", "http-status"),
    ("no_content_204", "204 No Content — успешное действие без тела", "204 No Content — ответ на успешный DELETE или обновление, когда тело ответа не требуется", "HTTP, REST API и безопасность", "http-status"),
    ("bad_request_400", "400 Bad Request — ошибка в запросе клиента", "400 Bad Request — некорректный синтаксис JSON, недопустимые параметры или ошибка формы", "HTTP, REST API и безопасность", "http-status"),
    ("unauthorized_401", "401 Unauthorized — требуется аутентификация", "401 Unauthorized — пользователь не представился (отсутствует или невалиден Bearer токен)", "HTTP, REST API и безопасность", "http-status"),
    ("forbidden_403", "403 Forbidden — доступ запрещен правами", "403 Forbidden — пользователь авторизован, но у него нет прав на этот объект (нет роли)", "HTTP, REST API и безопасность", "http-status"),
    ("not_found_404", "404 Not Found — ресурс не найден", "404 Not Found — запрашиваемый URL или объект с указанным ID отсутствует на сервере", "HTTP, REST API и безопасность", "http-status"),
    ("method_not_allowed_405", "405 Method Not Allowed — метод не поддерживается", "405 Method Not Allowed — отправка POST на эндпоинт, который принимает только GET", "HTTP, REST API и безопасность", "http-status"),
    ("conflict_409", "409 Conflict — конфликт состояния ресурса", "409 Conflict — попытка создать пользователя с уже занятым email или конфликт версий", "HTTP, REST API и безопасность", "http-status"),
    ("unprocessable_entity_422", "422 Unprocessable Entity — ошибка валидации данных", "422 Unprocessable Entity — стандартный код ошибки валидации схем FastAPI/Pydantic", "HTTP, REST API и безопасность", "http-status"),
    ("too_many_requests_429", "429 Too Many Requests — превышен лимит запросов", "429 Too Many Requests — сработал Rate Limiter; клиенту нужно подождать (Retry-After)", "HTTP, REST API и безопасность", "http-status"),
    ("internal_server_error_500", "500 Internal Server Error — непредвиденная ошибка бэкенда", "500 Internal Server Error — необработанное исключение (Unhandled Exception) в коде сервера", "HTTP, REST API и безопасность", "http-status"),
    ("bad_gateway_502", "502 Bad Gateway — сбой апстрима за прокси", "502 Bad Gateway — Nginx не смог достучаться до упавшего бэкенда (Gunicorn/Uvicorn)", "HTTP, REST API и безопасность", "http-status"),
    ("service_unavailable_503", "503 Service Unavailable — сервер перегружен/на техобслуживании", "503 Service Unavailable — сервис временно не способен отвечать из-за пика нагрузки", "HTTP, REST API и безопасность", "http-status"),
    ("gateway_timeout_504", "504 Gateway Timeout — таймаут ожидания апстрима", "504 Gateway Timeout — Nginx ждал ответа от бэкенда дольше установленного лимита времени", "HTTP, REST API и безопасность", "http-status"),

    # REST & Headers
    ("bearer_token", "токен предъявителя в заголовке", "Authorization: Bearer <token> — стандарт передачи токена доступа для защищенных API эндпоинтов", "HTTP, REST API и безопасность", "http-auth"),
    ("jwt", "JSON Web Token (компактный подписанный токен)", "JWT — токен из трех частей (Header.Payload.Signature), закодированных в base64url", "HTTP, REST API и безопасность", "http-auth"),
    ("access_token", "короткоживущий токен доступа к API", "access_token — токен с коротким TTL (5-15 минут), предъявляемый для авторизации запросов", "HTTP, REST API и безопасность", "http-auth"),
    ("refresh_token", "долгоживущий токен для обновления пары", "refresh_token — токен с долгим TTL (30-60 дней), хранящийся в HttpOnly куке для перевыпуска access_token", "HTTP, REST API и безопасность", "http-auth"),
    ("cors", "Cross-Origin Resource Sharing (кросс-доменные запросы)", "CORS — механизм безопасности браузера, блокирующий запросы с другого домена без разрешения", "HTTP, REST API и безопасность", "http-security"),
    ("csrf_token", "токен защиты от межсайтовой подделки запроса", "CSRF Token — уникальный одноразовый секрет в формах, блокирующий атаки со сторонних вкладок", "HTTP, REST API и безопасность", "http-security"),
    ("http_only", "флаг недоступности куки для JavaScript", "Set-Cookie: ...; HttpOnly — защищает сессионную куку от кражи вредоносными скриптами через XSS", "HTTP, REST API и безопасность", "http-security"),
    ("secure_flag", "флаг передачи куки только по HTTPS", "Set-Cookie: ...; Secure — гарантирует передачу куки строго по зашифрованному SSL/TLS протоколу", "HTTP, REST API и безопасность", "http-security"),
    ("samesite_strict", "запрет отправки куки со сторонних сайтов", "SameSite=Strict — кука отправляется только при прямых переходах внутри исходного домена", "HTTP, REST API и безопасность", "http-security"),
    ("api_key", "секретный статический ключ приложения", "X-API-Key: <key> — фиксированный ключ для межсервисной аутентификации Machine-to-Machine", "HTTP, REST API и безопасность", "http-auth"),

    # WebSockets
    ("websocket_connect", "инициация WebSocket соединения", "ws://host/path — клиент отправляет HTTP GET с заголовком Upgrade: websocket", "HTTP, REST API и безопасность", "websocket"),
    ("websocket_accept", "прием и подтверждение сокета сервером", "await websocket.accept() — сервер завершает рукопожатие и переходит в дуплексный режим", "HTTP, REST API и безопасность", "websocket"),
    ("websocket_send", "отправка фрейма по сокету", "await websocket.send_text(json_data) — отправка текстового или бинарного пакета клиенту", "HTTP, REST API и безопасность", "websocket"),
    ("websocket_receive", "ожидание входящего фрейма", "data = await websocket.receive_text() — асинхронное чтение следующего сообщения от клиента", "HTTP, REST API и безопасность", "websocket"),
    ("websocket_close", "корректное закрытие сокета", "await websocket.close(code=1000) — отправка контрольного фрейма закрытия с кодом статуса", "HTTP, REST API и безопасность", "websocket"),
    ("heartbeat_ping", "контрольный пинг поддержания сокета", "PING фрейм — периодический опрос для предотвращения закрытия соединения NAT-роутерами", "HTTP, REST API и безопасность", "websocket"),
    ("heartbeat_pong", "ответ на контрольный пинг", "PONG фрейм — автоматический встречный ответ на PING для подтверждения связи", "HTTP, REST API и безопасность", "websocket"),

    # Security Standards
    ("rbac", "ролевая модель доступа (Role-Based Access Control)", "RBAC — разграничение прав пользователей на основе присвоенных ролей (Admin, Manager, User)", "HTTP, REST API и безопасность", "security-auth"),
    ("abac", "атрибутивная модель доступа (Attribute-Based)", "ABAC — гибкое управление доступом на основе контекста (время, IP, отдел, статус заказа)", "HTTP, REST API и безопасность", "security-auth"),
    ("oauth2", "протокол делегированной авторизации", "OAuth 2.0 — стандарт предоставления сервису ограниченного доступа к ресурсам пользователя (Google Login)", "HTTP, REST API и безопасность", "security-auth"),
    ("openid_connect", "слой идентификации поверх OAuth2 (OIDC)", "OpenID Connect — стандарт аутентификации с получением id_token с профилем пользователя", "HTTP, REST API и безопасность", "security-auth"),
    ("etag", "хэш-валидатор версии кэша страницы", "ETag: \"hash\" / If-None-Match — сервер возвращает 304 Not Modified, если контент не изменился", "HTTP, REST API и безопасность", "http-cache"),
    ("cache_control", "директива управления браузерным кэшем", "Cache-Control: no-cache, max-age=3600 — указывает браузеру и CDN правила сохранения ответа", "HTTP, REST API и безопасность", "http-cache"),
]
