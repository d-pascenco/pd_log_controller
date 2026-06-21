import os
import streamlit as st
import requests
from pathlib import Path
import pandas as pd
from io import StringIO

BASE_DIR = Path(__file__).resolve().parent
logo_path = BASE_DIR / "assets" / "images" / "logo_large.png"

st.set_page_config(
    page_title="PD Log Controller",
    page_icon=str(logo_path),
    layout="wide"
)

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("Log Controller")

with st.expander("Ввести вручную", expanded=False):               # блок ввода логов вручную
#    st.header("Отправить лог")

    source = st.text_input("Источник:", placeholder="...")
    level = st.selectbox("Уровень:", ["INFO", "WARNING", "ERROR", "CRITICAL"])
    message = st.text_input("Сообщение лога:")

    if st.button("Отправить"):
        if message and source:
            response = requests.post(f"{API_URL}/logs", json={
                "message": message,
                "level": level,
                "source": source
            })
            if response.status_code == 200:
                st.success("Лог отправлен")
            else:
                st.error(f"Ошибка: {response.status_code}")
        else:
            st.warning("Заполни сообщение и источник")


with st.expander("Импорт из файла", expanded=False):
    uploaded_file = st.file_uploader("Выберите файл", type=["csv", "xlsx"])

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.dataframe(df, height=200, use_container_width=True)
        st.button("Upload (не работает еще, я эндпоинт не подключил)")                   # заглушка

st.header("Все логи")

if st.button("Обновить"):
    pass

response = requests.get(f"{API_URL}/logs")
if response.status_code == 200:
    data = response.json()
    st.write(f"Всего логов: {data['count']}")
    if data["logs"]:
        st.table(data["logs"])
    else:
        st.info("Логов пока нет")
else:
    st.error("Не удалось получить логи. Бэкенд недоступен?")
