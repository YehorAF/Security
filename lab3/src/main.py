import os
import psutil

import streamlit as st

import components


def code_with_book_cipher():
    cipher: components.BookCipher = st.session_state.get("cipher")

    if not cipher:
        text = st.text_area("Веддіть кодовий текст")
        seed = st.number_input("Seed", min_value=0, step=1, value=5)
        with_clean = st.checkbox("Очищувати?")
        set_text_btn = st.button("Внести текст")
        if set_text_btn:
            cipher = components.BookCipher(
                text, seed=seed, with_clean=with_clean
            )
            st.session_state.update({"cipher": cipher})
            st.rerun()
    else:
        code = st.session_state.get("code") or ""
        result = st.session_state.get("result") or ""

        text = st.text_area("Введіть шифруємий текст або код")
        c1, c2 = st.columns(2)

        encode_dtn = c1.button("Шифрувати")
        c1.text_area("Результат", code, key="key_code")

        decode_dtn = c2.button("Дешифрувати")
        c2.text_area("Результат", result, key="key_result")

        if encode_dtn:
            st.session_state.update({"code": cipher.encode(text)})
            st.rerun()
        if decode_dtn:
            st.session_state.update({"result": cipher.decode(text)})
            st.rerun()


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
        code_with_book_cipher()
    except Exception as ex_:
        st.error(f"{ex_}")


if __name__ == "__main__":
    main()