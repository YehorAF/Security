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
            "loaded": True
        })



def show_text_coder():
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
            result = alphabet.code(
                text=text, 
                k=key, 
                func=components.CaesarCipher.encode_caesar, 
                use_data_validation=use_validation
            )
            st.title("Результат")
            st.write(result)
            st.download_button(
                "Завантажити", result, f"encoded_data.txt"
            )

        if decode_btn:
            result = alphabet.code(
                text=text, 
                k=key, 
                func=components.CaesarCipher.decode_caesar,
                use_data_validation=use_validation
            )
            st.title("Результат")
            st.write(result)
            st.download_button(
                "Завантажити", result, f"decoded_data.txt"
            )
    except Exception as ex_:
        st.error(f"Помилка: {ex_}")


def show_file_coder():
    key = st.number_input("Ключ", step=1, min_value=1)
    use_index = st.checkbox("Використовувати індекс для шифрування")
    file = st.file_uploader("Завантажити файл")
    c1, c2 = st.columns(2)
    encode_btn = c1.button("Шифрувати")
    decode_btn = c2.button("Розшифрувати")

    try:
        if encode_btn and file is not None:
            result = components.FileCode.code(
                file=file.read(),
                k=key,
                l=256,
                func=components.CaesarCipher.encode_caesar,
                use_index= "encode" if use_index else None
            )
            st.download_button(
                "Завантажити", result, f"encoded_{file.name}"
            )

        if decode_btn and file is not None:
            result = components.FileCode.code(
                file=file.read(),
                k=key,
                l=256,
                func=components.CaesarCipher.decode_caesar,
                use_index= "decode" if use_index else None
            )
            st.download_button(
                "Завантажити", result, f"decoded_{file.name}"
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
            options=["text", "file"], 
            captions=["Текст", "Файл"]
        )

        {
            "text": show_text_coder,
            "file": show_file_coder
        }[selected]()
    except Exception as ex_:
        st.error(f"{ex_}")


if __name__ == "__main__":
    main()