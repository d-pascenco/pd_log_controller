### Описание развертывания бэкенда и зависимостей

#### 1. Streamlit 
Основной сайт: https://streamlit.io/

API: https://docs.streamlit.io/develop/api-reference

Playground: https://streamlit.io/components?category=all


В виртуальном окружении
```bash
pip install streamlit
```
Проверка:
```bash
streamlit hello
```
Если всё ок, то ответ будет такой:
```text
 👋 Welcome to Streamlit!

If you'd like to receive helpful onboarding emails, news, offers, promotions,
and the occasional swag, please enter your email address below. Otherwise,
leave this field blank.
```
Плюс предложат указать email для получения рассылок.

Затем будет предоставлен набор ресурсов, среди которых адрес для подключения локально и удаленно:

```text
[browser]
    gatherUsageStats = false

2026-05-17 15:56:22.201 Uvicorn server started on 0.0.0.0:8501
Welcome to Streamlit. Check out our demo in your browser.
Local URL: http://localhost:8501
Network URL: http://111.111.111.111:8501
Ready to create your own Python apps super quickly?
Head over to https://docs.streamlit.io
May you create awesome apps!
```

Проверяем, куда он поставился:
```bash
python -m pip show streamlit
```

Запускать проект будем примерно так:
```bash
python -m streamlit run app/Home.py
```

Лучше сразу записать все зависимости:
```bash
pip freeze > requirements.txt
```