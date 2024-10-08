from datetime import datetime
import dotenv
import json
import os
import psutil

import streamlit as st

import components


def load_env():
    try:
        if not dotenv.load_dotenv():
            raise FileNotFoundError("./.env")
        
        path = os.getenv("SETTINGS_PATH")
        if not path:
            raise ValueError(path)

        with open(path) as file:
            data = json.load(file)

        alphabets = data["alphabets"]
        valid_chars = data["valid_chars"]
        alphabet = components.AlphabetCode(
            valid_chars=valid_chars, **alphabets
        )
        detection = components.AttackTabulaRectaDetection(
            tries=data["tries"],
            drop_tries=data["drop_tries"]
        )
    except ValueError as ex_:
        raise Exception(
            "Необхідно внести шлях файлу налаштувань в SETTINGS_PATH"
        )
    except FileNotFoundError as ex_:
        raise Exception(
            f"Неможливо знайти файл налаштувань за посиланням: {ex_}"
        )
    except KeyError as ex_:
        raise Exception(
            f"Необхідно внести дані в змінну: {ex_}"
        )
    except TypeError as ex_:
        raise Exception(
            f"Значення alphabets повинно бути словником"
        )
    else:
        st.session_state.update({
            "alphabet": alphabet,
            "loaded": True,
            "attack_tabula_recta_detection": detection
        })


def show_tabula_recta_text_coder():
    alphabet: components.AlphabetCode = st.session_state["alphabet"]
    text: str = st.session_state.get("text") or ""
    use_validation = st.checkbox("Використовувати валідацію даних")
    selected = st.radio(
        "Тип ключа",
        options=["2-keys", "3-keys", "keyword"],
        captions=[
            "ключ-вектор з 2 значень", 
            "ключ-вектор з 3 значень",
            "ключове слово"
        ]
    )

    if selected == "2-keys":
        a = st.number_input("A", min_value=1, step=1)
        b = st.number_input("B", min_value=1, step=1)
        keys = {"a": a, "b": b}
        skeys = (a, b)
        func = alphabet.code_by_multiple_key_with_tabula_recta
    elif selected == "3-keys":
        a = st.number_input("A", min_value=1, step=1)
        b = st.number_input("B", min_value=1, step=1)
        c = st.number_input("C", min_value=1, step=1)
        keys = {"a": a, "b": b, "c": c}
        skeys = (a, b, c)
        func = alphabet.code_by_multiple_key_with_tabula_recta
    elif selected == "keyword":
        keyword = st.text_input("Ключове слово")
        keys = {"keyword": keyword}
        skeys = keyword
        func = alphabet.code_by_word_with_tabula_recta

    text = st.text_area("Текст", text)
    file = st.file_uploader("Завантажити файл", type=["txt"])
    use_file_btn = st.button("Використовувати файл")

    c1, c2 = st.columns(2)
    encode_btn = c1.button("Шифрувати")
    decode_btn = c2.button("Розшифрувати")

    try:
        if use_file_btn and file is not None:
            st.session_state.update({"text": file.read().decode("utf-8")})

        detection: components.AttackTabulaRectaDetection = st\
            .session_state["attack_tabula_recta_detection"]
        dt = datetime.now()

        if encode_btn:
            action = "encode"
        elif decode_btn:
            action = "decode"
            detection.check_request(text, skeys, action, dt)

        if encode_btn or decode_btn:
            detection.insert_request(text, skeys, action, dt)
            result = func(
                text=text,
                action=action,
                use_data_validation=use_validation,
                **keys
            )
            st.title("Результат")
            st.write(result)
            st.download_button(
                "Завантажити", result, f"{action}_data.txt"
            )
    except Exception as ex_:
        st.error(f"Помилка: {ex_}")


def show_caesar_cypher_text_coder():
    alphabet: components.AlphabetCode = st.session_state["alphabet"]
    text: str = st.session_state.get("text") or ""
    use_validation = st.checkbox("Використовувати валідацію даних")
    key = st.number_input("Ключ", step=1, min_value=1)
    text = st.text_area("Текст", text)
    file = st.file_uploader("Завантажити файл", type=["txt"])
    use_file_btn = st.button("Використовувати файл")
    c1, c2 = st.columns(2)
    encode_btn = c1.button("Шифрувати")
    decode_btn = c2.button("Розшифрувати")

    try:
        if use_file_btn and file is not None:
            st.session_state.update({"text": file.read().decode("utf-8")})

        if encode_btn:
            func = components.CaesarCipher.encode_caesar
            action = "encode"
        elif decode_btn:
            func = components.CaesarCipher.decode_caesar
            action = "decode"

        if encode_btn or decode_btn:
            result = alphabet.code_with_caesar_cypher(
                text=text, 
                k=key, 
                func=func, 
                use_data_validation=use_validation
            )
            st.title("Результат")
            st.write(result)
            st.download_button(
                "Завантажити", result, f"{action}_data.txt"
            )
    except Exception as ex_:
        st.error(f"Помилка: {ex_}")


def show_caesar_cypher_file_coder():
    key = st.number_input("Ключ", step=1, min_value=1)
    use_index = st.checkbox("Використовувати індекс для шифрування")
    file = st.file_uploader("Завантажити файл")
    c1, c2 = st.columns(2)
    encode_btn = c1.button("Шифрувати")
    decode_btn = c2.button("Розшифрувати")

    try:
        if encode_btn:
            func = components.CaesarCipher.encode_caesar
            action = "encode"
        elif decode_btn:
            func = components.CaesarCipher.decode_caesar
            action = "decode"

        if (decode_btn or encode_btn) and file is not None:
            result = components.FileCode.code(
                file=file.read(),
                k=key,
                l=256,
                func=func,
                use_index= action if use_index else None
            )
            st.download_button(
                "Завантажити", result, f"{action}_{file.name}"
            )
    except Exception as ex_:
        st.error(f"Помилка: {ex_}")


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
        if not st.session_state.get("loaded"):
            load_env()

        selected = st.radio(
            "Що необіхдно зашифрувати?", 
            options=[
                "caesar_cypher_text", 
                "caesar_cypher_file",
                "tabula_recta"
            ], 
            captions=[
                "Текст через шифр Цезаря", 
                "Файл через шифр Цезаря",
                "Текст через шифр Тритеміуса"
            ]
        )
        {
            "caesar_cypher_text": show_caesar_cypher_text_coder,
            "caesar_cypher_file": show_caesar_cypher_file_coder,
            "tabula_recta": show_tabula_recta_text_coder
        }[selected]()
    except Exception as ex_:
        st.error(f"{ex_}")


if __name__ == "__main__":
    main()