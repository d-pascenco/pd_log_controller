# Проект по предмету «Семинар наставника»
Здесь буду описывать весь процесс создания.

## Стек

- **Backend:** FastAPI
  - -
- **Frontend:** Streamlit
  - -
- **База данных:** PostgreSQL
  - -
- **Репозиторий:** GitHub
```
        sem_project_d_pascenco/   # корень
        ├── README.md             # О проекте
        ├── wiki.md               # Описываю подробно весь воркфлоу
        ├── .gitignore            # Файл игнорирования некоторых сущностей при push
        ├── requirements.txt      # Зависимости
        ├── .env.example          # Переменные окружения
        ├── backend/              # Директория бэкенда
        │   ├── app/              #
        │   │   ├── -.py       #
        │   │   ├── -.py         #
        │   │   ├── -.py     #
        │   │   └── -.py    #
        │   └── __init__.py       #
        ├── frontend/             #
        │   └── streamlit_app.py  #
        └── .venv/                #
```
### 1. Подготовка окружения
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
а. Проверка интерпретатора:
```
which python
which pip
```
Выход из окружения:
```
deactivate
```
### 2. Переменные окружения
Файл `.env` в корне проекта:
```
DATABASE_URL=postgresql://sem_user:sem_pass@localhost:5432/sem_db
API_URL=http://127.0.0.1:8000
```
Пример без секретов в файле `.env.example`.

### 3. PostgreSQL
Запуск сервиса:
```
sudo systemctl enable --now postgresql
sudo systemctl status postgresql
```
Создание пользователя и базы:
```
sudo -u postgres psql
```
```
CREATE USER sem_user WITH PASSWORD 'sem_pass';
CREATE DATABASE sem_db OWNER sem_user;
GRANT ALL PRIVILEGES ON DATABASE sem_db TO sem_user;
\q
```
Проверка подключения:
```
psql postgresql://sem_user:sem_pass@localhost:5432/sem_db
```
### 4. Backend (FastAPI)
Основные endpoint-ы:
- `GET /health` — проверка, что API работает
- `GET /tasks` — список задач
- `POST /tasks` — добавление задачи
Запуск:
```
uvicorn backend.app.main:app --reload
```
Проверка:
### 5. Frontend (Streamlit)
`frontend/streamlit_app.py`:
- отправка задачи в backend (`POST /tasks`)
- получение списка задач (`GET /tasks`)
- отображение списка в интерфейсе
Запуск:
```
streamlit run frontend/streamlit_app.py
```
Открыть в браузере:
- <http://localhost:8501>

### 6. Локальный запуск
а. Перейти в проект:
```
cd /home/pd/Downloads/sem_project_d_pascenco/
```
б. Активировать окружение:
```
source .venv/bin/activate
```
в. Проверить PostgreSQL:
```
sudo systemctl status postgresql
```
г. Запустить backend:
```
uvicorn backend.app.main:app --reload
```
д. В отдельном терминале запустить frontend:
```
streamlit run frontend/streamlit_app.py
```
### 7. Docker / docker-compose
а. Проверка установки:
```
docker --version
docker compose version
```
б. Запуск сервисов:
```
docker compose up --build
```
в. Запуск в фоне:
```
docker compose up -d --build
```
г. Логи:
```
docker compose logs -f
```
д. Остановка:
```
docker compose down
```
е. Остановка с удалением томов:
```
docker compose down -v
```
------
### Проблемы, с которыми можно встретиться
- `ModuleNotFoundError`
```
source .venv/bin/activate
pip install -r requirements.txt
```
- Ошибка подключения к PostgreSQL `connection refused`
```
sudo systemctl restart postgresql
sudo systemctl status postgresql
```
- Порт 8000 занят
```
uvicorn backend.app.main:app --reload --port 8001
```
- Не читаются переменные из `.env`
Проверить, что `.env` лежит в корне проекта и имена переменных совпадают с тем, что в коде.
