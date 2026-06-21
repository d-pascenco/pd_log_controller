## Описание базы данных

### 1. PostgreSQL

Основной сайт: https://www.postgresql.org/

PostgreSQL — реляционная БД. Данные хранятся в таблицах со строками и столбцами.
В проекте используется как основное хранилище логов.

Поднимается через docker-compose как отдельный контейнер из готового образа `postgres:16`.

Настройки подключения задаются через переменные окружения:
```yaml
environment:
  POSTGRES_USER: pd_user       # имя пользователя БД
  POSTGRES_PASSWORD: pd_pass   # пароль
  POSTGRES_DB: pd_logs         # имя базы данных
```
При первом запуске контейнер сам создаёт пользователя и базу с этими данными.

### 2. Строка подключения

Формат: `postgresql://пользователь:пароль@хост:порт/имя_базы`

В docker-compose хост — это имя сервиса (например `db`), а не IP.
```
postgresql://pd_user:pd_pass@db:5432/pd_logs
```
Порт 5432 — стандартный порт PostgreSQL.

### 3. SQLAlchemy

Docs: https://docs.sqlalchemy.org/

Библиотека для работы с БД из Python. Позволяет не писать SQL вручную,
а работать с таблицами как с Python-объектами (ORM).

Зачем: можно потом поменять PostgreSQL на другую БД (MySQL, SQLite),
изменив только строку подключения — код остаётся тот же.

Установка:
```bash
pip install sqlalchemy psycopg2-binary
```
`sqlalchemy` — сама ORM.
`psycopg2-binary` — драйвер для подключения к PostgreSQL. Без него SQLAlchemy не знает как общаться с PostgreSQL.

### 4. Подключение

Файл `src/db/database.py`:
- `engine` — объект подключения к БД. Создаётся один раз при старте.
- `SessionLocal` — фабрика сессий. Сессия — это одна "транзакция" с БД.
- `get_db()` — функция, которая выдаёт сессию для запроса и закрывает после.

### 5. Модели

Файл `src/db/models.py`:
Модель — это Python-класс, который описывает таблицу в БД.
Каждый атрибут класса = колонка в таблице.

```python
class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    message = Column(String)
    level = Column(String)
```

`__tablename__` — имя таблицы в БД.
`primary_key=True` — уникальный идентификатор строки.

### 6. Основные операции

Добавить запись:
```python
log = Log(message="test", level="INFO", source="app")
db.add(log)
db.commit()
```

Получить все записи:
```python
logs = db.query(Log).all()
```

С фильтром:
```python
errors = db.query(Log).filter(Log.level == "ERROR").all()
```

### 7. Полезные команды

Зайти в БД внутри контейнера:
```bash
docker exec -it pd_log_db psql -U pd_user -d pd_logs
```

Посмотреть таблицы: `\dt`
Посмотреть содержимое: `SELECT * FROM logs;`
Выйти: `\q`
