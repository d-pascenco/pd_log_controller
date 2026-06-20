## Описание скриптов проекта

Все скрипты лежат в `scripts/`.

### 1. start.sh

Скрипт запуска всех сервисов внутри Docker-контейнера.
Запускает бэкенд (FastAPI) и фронтенд (Streamlit) в одном контейнере.

```bash
#!/bin/bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &
streamlit run app/Home.py --server.address=0.0.0.0 --server.port=8501
```

`&` после uvicorn — запускает его в фоне.
Streamlit запускается на переднем плане — контейнер живёт, пока жив этот процесс.

Используется в Dockerfile:
```dockerfile
CMD ["bash", "scripts/start.sh"]
```
