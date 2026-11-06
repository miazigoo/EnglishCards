#!/usr/bin/env python3
"""Choose a sentence pair per Anki word, preserving attribution and manual edits."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "content/cards.json"
CANDIDATES = ROOT / "content/anki_context_candidates.json"
OUT = ROOT / "content/anki_contexts.json"

MANUAL = {
    "attempt": ("We will attempt the task again.", "Мы снова попробуем выполнить задачу."),
    "claim": ("They claim the service is secure.", "Они утверждают, что сервис безопасен."),
    "doubt": ("I doubt this result is correct.", "Я сомневаюсь, что этот результат верен."),
    "discover": ("We discovered an error in the configuration.", "Мы обнаружили ошибку в настройке."),
    "provide": ("The API provides a clear error message.", "API предоставляет понятное сообщение об ошибке."),
    "support": ("We support this decision.", "Мы поддерживаем это решение."),
    "cause": ("A small error can cause a failure.", "Небольшая ошибка может вызвать сбой."),
    "keep": ("Keep a copy of this file.", "Сохраните копию этого файла."),
    "lend": ("Can you lend me your pen?", "Можешь одолжить мне ручку?"),
    "save": ("Save the file before you close it.", "Сохраните файл, прежде чем закрыть его."),
    "suppose": ("I suppose this answer is correct.", "Я предполагаю, что этот ответ верен."),
    "though": ("Though it was late, we continued.", "Хотя было поздно, мы продолжили."),
    "in particular": ("This rule applies to services, in particular to APIs.", "Это правило относится к сервисам, в частности к API."),
    "so far": ("The service has worked so far.", "До сих пор сервис работал."),
    "proper": ("Use the proper method for this task.", "Используйте надлежащий метод для этой задачи."),
    "remote": ("The team works from a remote location.", "Команда работает из удалённого места."),
    "entrance": ("The entrance is on the left.", "Вход находится слева."),
    "critical": ("This is a critical step in the process.", "Это критически важный шаг в процессе."),
    "major": ("The major reason is a missing value.", "Основная причина — отсутствующее значение."),
    "utility bill": ("The utility bill is due next week.", "Счёт за коммунальные услуги нужно оплатить на следующей неделе."),
    "monthly payment": ("The monthly payment is due tomorrow.", "Ежемесячный платёж нужно внести завтра."),
    "proof of address": ("Please provide proof of address.", "Пожалуйста, предоставьте подтверждение адреса."),
    "applicant": ("The applicant has relevant experience.", "У соискателя есть подходящий опыт."),
    "notice period": ("My notice period is two weeks.", "Мой срок предупреждения об увольнении — две недели."),
    "onboarding": ("Onboarding starts on your first day.", "Введение в должность начинается в первый рабочий день."),
    "probation period": ("The probation period lasts three months.", "Испытательный срок длится три месяца."),
    "qualification": ("This role requires a technical qualification.", "Для этой должности требуется техническая квалификация."),
    "recruiter": ("The recruiter will contact you tomorrow.", "Рекрутер свяжется с вами завтра."),
    "relocation": ("The company offers help with relocation.", "Компания помогает с переездом по работе."),
    "annual leave": ("You can request annual leave online.", "Вы можете подать заявку на ежегодный отпуск онлайн."),
    "gross salary": ("The contract states the gross salary.", "В контракте указана зарплата до вычета налогов."),
    "net salary": ("Your net salary arrives after taxes.", "Зарплата после вычета налогов поступает на счёт."),
    "salary range": ("The salary range is shown in the vacancy.", "Диапазон зарплаты указан в вакансии."),
    "authentication": ("Authentication confirms who the user is.", "Аутентификация подтверждает личность пользователя."),
    "authorization": ("Authorization determines what the user can access.", "Авторизация определяет, к чему у пользователя есть доступ."),
    "bandwidth": ("The connection has limited bandwidth.", "У соединения ограниченная пропускная способность."),
    "callback": ("The callback runs when the task finishes.", "Обратный вызов выполняется после завершения задачи."),
    "credentials": ("Never put credentials in public code.", "Не размещайте учётные данные в открытом коде."),
    "downtime": ("The update caused ten minutes of downtime.", "Обновление вызвало десять минут простоя."),
    "endpoint": ("This endpoint returns the current status.", "Эта конечная точка API возвращает текущее состояние."),
    "latency": ("High latency makes each request slower.", "Высокая задержка замедляет каждый запрос."),
    "message queue": ("The worker reads tasks from a message queue.", "Рабочий процесс получает задачи из очереди сообщений."),
    "middleware": ("Middleware checks the request before the view runs.", "Промежуточное ПО проверяет запрос до вызова представления."),
    "payload": ("The payload contains the order number.", "Полезная нагрузка сообщения содержит номер заказа."),
    "rate limit": ("The rate limit protects the API from overload.", "Ограничение частоты запросов защищает API от перегрузки."),
    "repository": ("The repository stores the project code.", "Репозиторий хранит код проекта."),
    "retry": ("A retry may succeed after a temporary failure.", "Повторная попытка может пройти после временного сбоя."),
    "rollback": ("A rollback restored the previous version.", "Откат восстановил предыдущую версию."),
    "runtime": ("The error occurred at runtime.", "Ошибка возникла во время выполнения программы."),
    "scalability": ("Scalability matters when traffic grows.", "Масштабируемость важна, когда растёт трафик."),
    "schema": ("The schema defines the data structure.", "Схема определяет структуру данных."),
    "not yet": ("The update is not ready yet.", "Обновление ещё не готово."),
    "basically": ("Basically, the function returns a list.", "По сути, функция возвращает список."),
    "eventually": ("Eventually, the service recovered.", "В конечном итоге сервис восстановился."),
    "fortunately": ("Fortunately, the backup was available.", "К счастью, резервная копия была доступна."),
    "rather": ("I would rather wait for the result.", "Я бы скорее подождал результата."),
    "suddenly": ("The connection suddenly failed.", "Соединение внезапно оборвалось."),
    "for example": ("For example, a model can have a title field.", "Например, у модели может быть поле названия."),
    "in case": ("Keep a backup in case the update fails.", "Сохраните копию на случай, если обновление завершится с ошибкой."),
    "in fact": ("In fact, the result is different.", "На самом деле результат отличается."),
    "on time": ("The task finished on time.", "Задача завершилась вовремя."),
    "to be honest": ("To be honest, I need more practice.", "Честно говоря, мне нужно больше практики."),
    "confident": ("She is confident about her answer.", "Она уверена в своём ответе."),
    "flexible": ("The system has a flexible configuration.", "У системы гибкая настройка."),
    "frequent": ("Frequent requests can overload the server.", "Частые запросы могут перегрузить сервер."),
    "independent": ("This module is independent of the database.", "Этот модуль независим от базы данных."),
    "likely": ("A delay is likely during the update.", "Во время обновления вероятна задержка."),
    "particular": ("A particular value is required here.", "Здесь требуется конкретное значение."),
    "visa": ("She applied for a work visa.", "Она подала заявление на рабочую визу."),
    "fine": ("You may have to pay a fine for late payment.", "За просроченный платёж, возможно, придётся заплатить штраф."),
    "candidate": ("The candidate has relevant experience.", "У кандидата есть подходящий опыт."),
    "company": ("The company develops web applications.", "Компания разрабатывает веб-приложения."),
    "requirement": ("Experience is a requirement for this role.", "Опыт — обязательное требование для этой должности."),
    "teamwork": ("Good teamwork helps the project succeed.", "Хорошая командная работа помогает проекту добиться успеха."),
    "branch": ("Create a new branch before changing the code.", "Создайте новую ветку перед изменением кода."),
    "dependency": ("The package has a new dependency.", "У пакета появилась новая зависимость."),
    "environment": ("The test environment uses a separate database.", "В тестовом окружении используется отдельная база данных."),
    "exception": ("The function raises an exception for invalid input.", "Функция вызывает исключение при неверном вводе."),
    "outage": ("The service outage lasted ten minutes.", "Сервис был недоступен десять минут."),
    "query": ("The query returns matching records.", "Запрос возвращает подходящие записи."),
    "release": ("The new release fixes the error.", "Новый выпуск версии исправляет ошибку."),
    "service": ("The service handles incoming requests.", "Сервис обрабатывает входящие запросы."),
    "storage": ("The application needs more storage.", "Приложению требуется больше места в хранилище."),
    "overload": ("An overload stopped the motor.", "Перегрузка остановила двигатель."),
    "reset": ("Press reset after fixing the fault.", "Нажмите сброс после устранения неисправности."),
    "timer": ("The timer starts when the sensor detects a box.", "Таймер запускается, когда датчик обнаруживает коробку."),
    "assembly": ("Assembly begins after all parts arrive.", "Сборка начинается после прибытия всех деталей."),
    "consumption": ("The report shows material consumption by shift.", "Отчёт показывает расход материалов по сменам."),
    "defect": ("Quality control found a defect in the part.", "Контроль качества обнаружил дефект в детали."),
    "reject": ("Reject any item with an unreadable code.", "Бракуйте любое изделие с нечитаемым кодом."),
    "serial number": ("Each device has a unique serial number.", "У каждого устройства есть уникальный серийный номер."),
    "warehouse": ("The warehouse stores finished goods.", "Склад хранит готовую продукцию."),
    "benefit": ("This benefit is available to all employees.", "Эта льгота доступна всем сотрудникам."),
    "experience": ("She has five years of experience.", "У неё пять лет опыта."),
    "performance": ("The new version improved performance.", "Новая версия повысила производительность."),
    "position": ("The position is still open.", "Эта должность всё ещё вакантна."),
    "reference": ("The guide includes a reference to this method.", "Руководство содержит ссылку на этот метод."),
    "training": ("The company provides training for new staff.", "Компания проводит обучение новых сотрудников."),
    "backup": ("Make a backup before the update.", "Создайте резервную копию перед обновлением."),
    "constraint": ("This constraint prevents duplicate values.", "Это ограничение не допускает повторяющихся значений."),
    "deployment": ("The deployment finished without errors.", "Развёртывание завершилось без ошибок."),
    "failure": ("The service recovered after the failure.", "Сервис восстановился после сбоя."),
    "gateway": ("The gateway forwards requests to the service.", "Шлюз пересылает запросы сервису."),
    "log": ("Check the log for the error.", "Проверьте журнал на наличие ошибки."),
    "monitoring": ("Monitoring detected a slow response.", "Мониторинг обнаружил медленный ответ."),
    "pipeline": ("The pipeline runs tests after each commit.", "Конвейер обработки запускает тесты после каждого коммита."),
    "socket": ("The socket accepts a new connection.", "Сокет принимает новое соединение."),
    "token": ("The client sends a token with the request.", "Клиент отправляет токен вместе с запросом."),
    "trace": ("The trace shows where the error started.", "Трассировка показывает, где началась ошибка."),
    "trigger": ("A sensor can act as a trigger for the alarm.", "Датчик может служить триггером аварийного сигнала."),
    "workflow": ("The workflow has three review steps.", "Рабочий процесс включает три этапа проверки."),
    "counter": ("The counter increases for each request.", "Счётчик увеличивается после каждого запроса."),
    "relay": ("The relay switches the motor on.", "Реле включает двигатель."),
    "override": ("The override replaces the default value.", "Принудительное переопределение заменяет значение по умолчанию."),
    "inventory": ("The warehouse updates inventory every hour.", "Склад обновляет данные о запасах каждый час."),
    "scrap": ("The defective parts were sent to scrap.", "Бракованные детали отправили в отходы."),
    "yield": ("The generator uses yield to return values one at a time.", "Генератор использует yield, чтобы выдавать значения по одному."),
    "root cause": ("The root cause was a missing configuration value.", "Первопричиной стало отсутствующее значение настройки."),
    "bring up": ("I want to bring up a problem.", "Я хочу поднять вопрос о проблеме."),
    "carry out": ("Carry out the safety check before starting.", "Выполните проверку безопасности перед запуском."),
    "drop off": ("Please drop off the package at reception.", "Пожалуйста, оставьте посылку на стойке регистрации."),
    "go over": ("Let's go over the report together.", "Давайте вместе просмотрим отчёт."),
    "look for": ("Look for the error in the log.", "Поищите ошибку в журнале."),
    "pick up": ("I will pick up the package tomorrow.", "Я заберу посылку завтра."),
    "set up": ("Set up the server before testing.", "Настройте сервер перед тестированием."),
    "turn down": ("They turned down the job offer.", "Они отклонили предложение о работе."),
    "work out": ("We need to work out a solution.", "Нам нужно найти решение."),
    "follow up": ("I will follow up with the client tomorrow.", "Завтра я уточню вопрос у клиента."),
    "check out": ("We will check out of the hotel at eight.", "Мы выпишемся из отеля в восемь."),
    "get back to": ("I'll get back to you after the meeting.", "Я вернусь к вам с ответом после совещания."),
    "get rid of": ("Get rid of old backup files.", "Избавьтесь от старых резервных копий."),
    "throughput": ("We measured the throughput of the service.", "Мы измерили пропускную способность сервиса."),
    "timeout": ("The request failed after a timeout.", "Запрос завершился ошибкой после тайм-аута."),
    "validation": ("Validation rejects an invalid value.", "Проверка корректности отклоняет неверное значение."),
    "version control": ("Version control records every code change.", "Контроль версий сохраняет каждое изменение кода."),
    "actuator": ("The actuator opens the valve.", "Исполнительный механизм открывает клапан."),
    "analog input": ("The analog input reads the sensor voltage.", "Аналоговый вход считывает напряжение датчика."),
    "analog output": ("The analog output controls motor speed.", "Аналоговый выход управляет скоростью двигателя."),
    "calibration": ("The sensor needs calibration before use.", "Перед использованием датчик нужно откалибровать."),
    "commissioning": ("Commissioning starts after the equipment is installed.", "Пусконаладка начинается после установки оборудования."),
    "conveyor": ("The conveyor moves boxes to the scanner.", "Конвейер перемещает коробки к сканеру."),
    "cycle time": ("The cycle time is three seconds.", "Время цикла составляет три секунды."),
    "digital input": ("A digital input detects the switch state.", "Дискретный вход определяет состояние переключателя."),
    "digital output": ("The digital output turns on the lamp.", "Дискретный выход включает лампу."),
    "emergency stop": ("Press the emergency stop if the line becomes unsafe.", "Нажмите аварийную остановку, если линия стала небезопасной."),
    "encoder": ("The encoder reports the shaft position.", "Энкодер сообщает положение вала."),
    "fieldbus": ("The fieldbus connects the controller to sensors.", "Полевая шина соединяет контроллер с датчиками."),
    "flow rate": ("The flow rate dropped below the limit.", "Расход потока упал ниже предела."),
    "frequency inverter": ("The frequency inverter adjusts motor speed.", "Частотный преобразователь регулирует скорость двигателя."),
    "human-machine interface": ("The operator checks alarms on the human-machine interface.", "Оператор проверяет аварийные сигналы на человеко-машинном интерфейсе."),
    "interlock": ("The interlock prevents the door from opening.", "Блокировка не даёт открыть дверь."),
    "ladder logic": ("The controller runs a ladder logic program.", "Контроллер выполняет программу на языке релейно-контактной логики."),
    "limit switch": ("The limit switch detects the end position.", "Концевой выключатель определяет крайнее положение."),
    "motor starter": ("The motor starter turns the motor on safely.", "Пускатель двигателя безопасно включает двигатель."),
    "normally closed": ("The normally closed contact opens when pressed.", "Нормально замкнутый контакт размыкается при нажатии."),
    "normally open": ("The normally open contact closes when pressed.", "Нормально разомкнутый контакт замыкается при нажатии."),
    "output coil": ("The output coil controls the relay.", "Выходная катушка управляет реле."),
    "proximity sensor": ("The proximity sensor detects a nearby object.", "Датчик приближения обнаруживает объект рядом."),
    "scan cycle": ("One scan cycle reads inputs and updates outputs.", "Один цикл сканирования считывает входы и обновляет выходы."),
    "setpoint": ("Set the temperature setpoint to 80 degrees.", "Установите уставку температуры на 80 градусов."),
    "solenoid valve": ("The solenoid valve controls the air flow.", "Электромагнитный клапан управляет потоком воздуха."),
    "state machine": ("The state machine tracks the current process step.", "Конечный автомат отслеживает текущий этап процесса."),
    "structured text": ("The PLC program uses structured text.", "Программа ПЛК написана на языке структурированного текста."),
    "torque": ("The motor produces enough torque to move the load.", "Двигатель создаёт достаточный крутящий момент для перемещения груза."),
    "variable frequency drive": ("A variable frequency drive controls the pump motor.", "Частотно-регулируемый привод управляет двигателем насоса."),
    "wiring diagram": ("Check the wiring diagram before connecting the sensor.", "Проверьте электрическую схему перед подключением датчика."),
    "pressure sensor": ("The pressure sensor reports a low value.", "Датчик давления сообщает о низком значении."),
    "temperature sensor": ("The temperature sensor needs calibration.", "Датчик температуры нуждается в калибровке."),
    "level sensor": ("The level sensor detects an empty tank.", "Датчик уровня обнаруживает пустой бак."),
    "fault detection": ("Fault detection stops the line after an error.", "Обнаружение неисправностей останавливает линию после ошибки."),
    "manual mode": ("Use manual mode during maintenance.", "Во время обслуживания используйте ручной режим."),
    "automatic mode": ("The line runs in automatic mode.", "Линия работает в автоматическом режиме."),
    "bill of materials": ("The bill of materials lists every required component.", "Спецификация материалов перечисляет все необходимые компоненты."),
    "downtime reason": ("Record the downtime reason in the report.", "Запишите причину простоя в отчёт."),
    "finished goods": ("Finished goods are ready for shipment.", "Готовая продукция готова к отгрузке."),
    "lot number": ("The lot number identifies this batch.", "Номер партии идентифицирует эту партию."),
    "material tracking": ("Material tracking shows where each component went.", "Отслеживание материалов показывает, куда попал каждый компонент."),
    "order fulfillment": ("Order fulfillment begins after payment.", "Выполнение заказа начинается после оплаты."),
    "overall equipment effectiveness": ("Overall equipment effectiveness dropped this month.", "Общая эффективность оборудования снизилась в этом месяце."),
    "production line": ("The production line stops when an alarm appears.", "Производственная линия останавливается при появлении аварийного сигнала."),
    "production order": ("The production order specifies the required quantity.", "Производственный заказ указывает необходимое количество."),
    "quality assurance": ("Quality assurance defines checks for the process.", "Обеспечение качества определяет проверки для процесса."),
    "quality control": ("Quality control found a defective item.", "Контроль качества обнаружил дефектное изделие."),
    "shop floor": ("The operator works on the shop floor.", "Оператор работает в производственном цехе."),
    "stock level": ("The stock level fell below the minimum.", "Уровень запасов упал ниже минимума."),
    "work order": ("The technician received a new work order.", "Техник получил новое производственное задание."),
    "workstation": ("The workstation displays the current task.", "Рабочая станция показывает текущую задачу."),
    "work in progress": ("Work in progress is tracked separately from finished goods.", "Незавершённое производство учитывается отдельно от готовой продукции."),
    "production schedule": ("The production schedule changed this morning.", "Производственный график изменился сегодня утром."),
    "shift report": ("The shift report lists every alarm.", "Сменный отчёт перечисляет все аварийные сигналы."),
    "quality inspection": ("The batch passed the quality inspection.", "Партия прошла проверку качества."),
    "batch record": ("The batch record contains the test results.", "Запись о партии содержит результаты испытаний."),
    "equipment utilization": ("Equipment utilization increased after the update.", "Загрузка оборудования выросла после обновления."),
    "unplanned downtime": ("A sensor failure caused unplanned downtime.", "Сбой датчика вызвал незапланированный простой."),
    "preventive maintenance": ("Preventive maintenance reduces unexpected failures.", "Профилактическое обслуживание уменьшает число неожиданных сбоев."),
    "point out": ("Please point out the error in this line.", "Пожалуйста, укажите ошибку в этой строке."),
    "roll out": ("We will roll out the update tomorrow.", "Завтра мы развернём обновление."),
}


def main():
    cards = json.loads(CARDS.read_text(encoding="utf-8"))
    candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    contexts = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    existing = {c["display_term"].lower(): c for c in cards if not c["card_id"].startswith("anki.vocab.")}
    anki = [c for c in cards if c["card_id"].startswith("anki.vocab.")]
    missing = []
    for card in anki:
        cid, word = card["card_id"], card["display_term"]
        if cid in contexts and contexts[cid].get("editorial"):
            continue
        if word in MANUAL:
            en, ru = MANUAL[word]
            contexts[cid] = {"en": en, "ru": ru, "source": "original editorial example", "editorial": True}
            continue
        candidate = candidates.get(cid)
        if candidate and candidate.get("en") and candidate.get("ru"):
            contexts[cid] = candidate
            continue
        prior = existing.get(word.lower())
        if prior:
            pair = prior.get("examples", [{}])[0]
            if re.search(r"(?<![A-Za-z])" + re.escape(word) + r"(?![A-Za-z])", pair.get("en", ""), re.I) and pair.get("ru"):
                contexts[cid] = {"en": pair["en"], "ru": pair["ru"],
                                 "source": "existing English Cards content", "editorial": False}
                continue
        missing.append((cid, word, card["meaning_ru_short"], card["tags"][1]))
    OUT.write_text(json.dumps(contexts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("contexts", len(contexts), "missing", len(missing))
    for entry in missing:
        print(" | ".join(entry))


if __name__ == "__main__":
    main()
