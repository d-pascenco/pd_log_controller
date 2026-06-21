import streamlit as st
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
logo_path = BASE_DIR / "assets" / "images" / "logo_large.png"

st.set_page_config(
    page_title="PD Log Controller",
    page_icon=str(logo_path),
    layout="wide"
)

API_URL = "http://localhost:8000"

st.title("PD Log Controller")

st.header("Отправить лог")

message = st.text_input("Сообщение лога:")
level = st.selectbox("Уровень:", ["INFO", "WARNING", "ERROR", "CRITICAL"])
source = st.text_input("Источник:", placeholder="...")

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
