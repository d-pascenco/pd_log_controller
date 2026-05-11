### Стек:

- **Host:** Oracle Free Tier

- **OS:** Linux Oracle

- **Backend:** FastAPI
  - -
- **Frontend:** Streamlit
  - -
- **База данных:** PostgreSQL
  - -
- **Репозиторий:** GitHub

### Полная структура проекта
```
sem_project_d_pascenco/
├─ README.md                # общее описание проекта (стек, идея, запуск)
├─ requirements.txt         # Python-зависимости
├─ .env.example             # шаблон переменных окружения (без секретов)
├─ .env                     # локальные секреты/настройки (не коммитятся)
├─ .gitignore               # исключения для git
├─ LICENSE                  # лицензия проекта (MIT)
│
├─ app/                     # Streamlit-фронтенд (страницы UI, графики, фильтры)
│ ├─ Home.py                # точка входа Streamlit
│ └─ pages/                 # дополнительные страницы интерфейса
│
├─ src/                     # основной код backend/data-логики
│ └─ integrations/
│   └─ bots/
│     └─ telegram/
│       └─ bot.py           # модуль Telegram-бота (алерты/команды)
│
├─ data/                    # данные проекта
│ ├─ raw/                   # сырые данные
│ └─ processed/             # подготовленные/очищенные данные
│ └─ /sample/
├─ notebooks/
│ └─ test.ipynb # ноутбук для тестов/экспериментов
│
├─ docs/                    # документация по частям проекта
│ ├─ start_wiki.md
│ ├─ test_project_plan.md
│ ├─ app_description.md
│ ├─ data_description.md
│ ├─ src_description.md
│ └─ notebooks_description.md
├─ logs/                    # логи всех компонентов
├─ .idea/                   # служебные файлы PyCharm
├─ .venv/                   # локальное виртуальное окружение Python
└─ .git/                    # служебные файлы git-репозитория
```

### Запуск проекта

test