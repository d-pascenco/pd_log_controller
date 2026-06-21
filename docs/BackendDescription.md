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

Логи хранятся в PostgreSQL через SQLAlchemy ORM.
Подключение и модели — в `src/db/` (см. DatabaseDescription.md).

При старте приложения таблицы создаются автоматически:
```python
Base.metadata.create_all(bind=engine)
```

### 3. Как API работает с БД

**Depends(get_db)** — FastAPI автоматически вызывает `get_db()` перед каждым запросом,
передаёт сессию БД в функцию, и закрывает сессию после ответа.

```python
def create_log(entry: LogEntry, db: Session = Depends(get_db)):
```
`db` — это сессия. Через неё делаю все операции с БД.

**POST /logs** — что происходит:
1. `Log(...)` — создаём Python-объект из модели
2. `db.add(log)` — добавляем в сессию (пока не в бд)
3. `db.commit()` — записываем в БД
4. `db.refresh(log)` — обновляем объект (получаем `id` и `timestamp` из БД)

**GET /logs** — `db.query(Log).all()` возвращает все строки таблицы `logs` как список объектов.

### 4. Схемы данных (Pydantic)

```python
class LogEntry(BaseModel):
    message: str
    level: str
    source: str
```

Описывает, что ожидает API на входе. Если отправить не те поля или не тот тип —
FastAPI автоматически вернёт ошибку 422 с описанием что не так.
