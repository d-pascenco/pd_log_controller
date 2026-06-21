## Описание FastAPI и основных концепций

Основной сайт: https://fastapi.tiangolo.com/

API Reference: https://fastapi.tiangolo.com/reference/

### 1. FastAPI

Это фреймворк для создания бэкенда на Python.
Принимает HTTP-запросы и возвращает ответы в формате JSON.

### 2. Установка

В виртуальном окружении:
```bash
pip install fastapi
```
FastAPI сам по себе — это только фреймворк. Для запуска нужен ASGI-сервер.
Используем uvicorn:
```bash
pip install uvicorn
```

Проверка:
```bash
python -c "import fastapi; print(fastapi.__version__)"
```

### 3. Минимальное приложение

Файл `src/api/main.py`:
```python
from fastapi import FastAPI
app = FastAPI()
@app.get("/health")
def health_check():
    return {"status": "ok"}
```
Разбор по строкам:
- `from fastapi import FastAPI` — импортируем класс FastAPI.
- `app = FastAPI()` — создаём экземпляр приложения. Именно эту переменную ищет uvicorn при запуске.
- `@app.get("/health")` — декоратор. Говорит: "при GET-запросе на /health вызови функцию ниже".
- `def health_check()` — обычная функция Python. Возвращает словарь, FastAPI автоматически превращает его в JSON.

### 4. Запуск

Из корня проекта:
```bash
uvicorn src.api.main:app --reload --port 8000
```

После запуска доступно:
- `http://localhost:8000/health` — ответ `{"status": "ok"}`
- `http://localhost:8000/docs` — Swagger UI (автодокументация, можно тестировать эндпоинты)
- `http://localhost:8000/redoc` — ReDoc (альтернативная документация)

### 5. HTTP-методы (декораторы)

FastAPI поддерживает все основные HTTP-методы:
```python
@app.get("/path")       # получить данные
@app.post("/path")      # отправить / создать данные
@app.put("/path")       # обновить данные целиком
@app.patch("/path")     # обновить данные частично
@app.delete("/path")    # удалить данные
```

Самые частые в проектах:
- `GET` — запросить данные (список логов, статус, статистика).
- `POST` — отправить данные (загрузить лог, запустить анализ).

### 6. Параметры пути (Path Parameters)

Значения, которые передаются прямо в URL:
```python
@app.get("/logs/{log_id}")
def get_log(log_id: int):
    return {"log_id": log_id}
```

Запрос: `GET /logs/42` → ответ: `{"log_id": 42}`

`{log_id}` в пути автоматически становится аргументом функции.
Указание типа `int` — FastAPI сам проверит, что передано число, и вернёт ошибку если нет.

### 7. Параметры запроса

Значения после `?` в URL:
```python
@app.get("/logs")
def get_logs(level: str = "all", limit: int = 10):
    return {"level": level, "limit": limit}
```

Запрос: `GET /logs?level=ERROR&limit=5` → ответ: `{"level": "ERROR", "limit": 5}`

Аргументы функции, которых нет в пути `{}`, автоматически становятся query-параметрами.
Значения по умолчанию (`"all"`, `10`) делают параметры необязательными.

### 8. Тело запроса

Для POST-запросов данные передаются в теле запроса как JSON.
FastAPI использует Pydantic для валидации:
```python
from pydantic import BaseModel
class LogEntry(BaseModel):
    message: str
    level: str
    source: str
@app.post("/logs")
def create_log(entry: LogEntry):
    return {"received": entry.model_dump()}
```

Запрос (JSON в теле):
```json
{
    "message": "Connection timeout",
    "level": "ERROR",
    "source": "nginx"
}
```

Pydantic автоматически:
- проверяет, что все обязательные поля переданы;
- проверяет типы данных;
- возвращает понятную ошибку, если что-то не так.

### 9. Коды ответов (Status Codes)

По умолчанию FastAPI возвращает код `200 OK`.
Можно указать другой:
```python
from fastapi import status

@app.post("/logs", status_code=status.HTTP_201_CREATED)
def create_log(entry: LogEntry):
    return {"id": 1, "received": entry.model_dump()}
```

Основные коды:
- `200` — OK (всё хорошо, данные возвращены).
- `201` — Created (объект успешно создан).
- `404` — Not Found (ресурс не найден).
- `422` — Unprocessable Entity (ошибка валидации, FastAPI возвращает автоматически).
- `500` — Internal Server Error (ошибка на сервере).

### 10. Полезные команды

Запуск в режиме разработки:
```bash
uvicorn src.api.main:app --reload --port 8000
```

Запуск для продакшена:
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

`--host 0.0.0.0` — слушать на всех интерфейсах (нужно для Docker и удалённого доступа).

Проверка через curl:
```bash
curl http://localhost:8000/health
```

Проверка POST через curl:
```bash
curl -X POST http://localhost:8000/logs \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "level": "INFO", "source": "app"}'
```
