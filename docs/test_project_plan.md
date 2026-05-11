### Тестовый план проекта
```
log-anomaly/
├─ README.md
├─ pyproject.toml
├─ .env.example
├─ docker-compose.yml
├─ Makefile
├─ configs/
│ ├─ app.yaml
│ ├─ model.yaml
│ └─ alerts.yaml
├─ data/
│ ├─ raw/ # необработанные логи (локально, в git не коммитить)
│ ├─ bronze/
│ ├─ silver/
│ └─ gold/
├─ notebooks/
│ ├─ 01_eda.ipynb
│ ├─ 02_feature_eng.ipynb
│ └─ 03_modeling.ipynb
├─ src/
│ ├─ ingestion/ # сбор логов (filebeat/fluent-bit/mock generator)
│ ├─ parsing/ # regex/grok/drain парсинг
│ ├─ features/ # агрегаты, TF-IDF/embeddings, временные фичи
│ ├─ models/ # train/infer (IsolationForest/LSTM/Autoencoder)
│ ├─ pipeline/ # orchestration шагов
│ ├─ serving/ # API/worker для inference
│ └─ utils/
├─ tests/
│ ├─ unit/
│ └─ integration/
├─ dashboards/
│ ├─ grafana/
│ └─ superset/
├─ sql/
│ ├─ marts/
│ └─ quality_checks/
├─ docs/
│ ├─ architecture.md
│ ├─ experiments.md
│ └─ thesis_notes.md
└─ ci/
└─ github-actions.yml
```