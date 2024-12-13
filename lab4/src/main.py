import os
import psutil
import pickle

import streamlit as st

import components


def code(code: str):
    key = st.text_input("Ключ")

    c1, c2 = st.columns(2)

    text = c1.text_area("Контент")
    encrypt_btn = c1.button("Шифрувати")

    if encrypt_btn and key and text:
        cipher = components.AbsCipher()
        res = cipher.encrypt(text.encode(), key.encode(), code)

        download_btn = c1.download_button(
            "Завантажити", pickle.dumps(res), f"{code}_cipher.json"
        )

    file = c2.file_uploader("Файл")
    decrypt_btn = c2.button("Розшифрувати")

    if decrypt_btn and file:
        res = pickle.loads(file.read())

        cipher = components.AbsCipher()
        res = cipher.decrypt(res["result"], key.encode(), code, **res)

        c2.text(res.decode())


def main():
    with st.sidebar:
        st.title("Інформація")
        st.write("Дисципліна \"Безпека ПЗ\"")
        st.write("Виконав: Нестеренко Єгор")
        st.write("Група: ТВ-13")
        exit_btn = st.button("Завершити роботу")

        if exit_btn:
            pid = os.getpid()
            p = psutil.Process(pid)
            p.terminate()

    try:
        t = st.radio("Тип шифрування", ["DES", "DES3", "AES"])
        code(t)
    except Exception as ex_:
        st.error(f"{ex_}")


if __name__ == "__main__":
    main()