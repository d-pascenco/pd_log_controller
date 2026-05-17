import streamlit as st
import numpy as np
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
logo_path = BASE_DIR / "assets" / "images" / "logo_large.png"

st.set_page_config(
    page_title="PD Log Controller",
    page_icon=str(logo_path),
    layout="wide"
)

# Ввод имени
name = st.text_input('Введите имя студента:', placeholder="Студент")

# Слайдер для числа
number = st.slider('Введите число:', 0, 10, 5)

# Кнопка для расчета
if st.button('Посчитать квадрат!'):
    result = number ** 2
    st.success(f'Привет, {name}! Квадрат числа {number} = {result}')
    st.balloons()

df = pd.DataFrame(np.random.randn(10, 4), columns=list('ABCD'))
df


import matplotlib.pyplot as plt
import numpy as np

arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

fig