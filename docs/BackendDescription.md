## Описание бэкенда проекта

Бэкенд написан на FastAPI. Точка входа: `src/api/main.py`.

### 1. Эндпоинты

**GET /health** — проверка, что API работает.
Ответ: `{"status": "ok"}`

**POST /logs** — принять лог-запись.
Тело запроса (JSON):
```json
{
    "message": "Connection timeout",
    "level": "ERROR",
    "source": "nginx"
}
```
Сервер добавляет `timestamp` автоматически.
Ответ: `{"status": "created", "log": {...}}`

**GET /logs** — получить все принятые логи.
Ответ: `{"count": 3, "logs": [...]}`

### 2. Хранение данных

Пока логи хранятся в списке в памяти (`logs_storage = []`).
При перезапуске контейнера всё теряется.
Потом заменим на PostgreSQL.

### 3. Схемы данных (Pydantic)

```python
class LogEntry(BaseModel):
    message: str
    level: str
    source: str
```

Описывает, что ожидает API на входе. Если отправить не те поля или не тот тип —
FastAPI автоматически вернёт ошибку 422 с описанием что не так.
