import time
import os
import psutil

import streamlit as st

from components import AbsRSA


def code():
    gen_or_load = st.radio("Генерація ключа", ["gen", "load"])
    pub = st.session_state.get("pub")
    prv = st.session_state.get("prv")

    if pub and prv:
        c1, c2 = st.columns(2)
        c1.download_button(
            "Публічний", 
            pub, 
            "pub.pem", 
            key="load_pub"
        )
        c2.download_button(
            "Приватний", 
            prv, 
            "prv.pem", 
            key="load_prv"
        )

    if gen_or_load == "gen":
        key_len = st.number_input(
            "Довжина ключа", 
            min_value=1024, 
            value=1024, 
            step=1
        )
        gen_keys_btn = st.button("Генерувати ключ")

        if gen_keys_btn:
            pub, prv = AbsRSA.gen_keys(key_len)

            st.session_state.update({"pub": pub})
            st.session_state.update({"prv": prv})
            st.success("Ключі було сформовано")
            time.sleep(3)
            st.rerun()
    elif gen_or_load == "load":
        c1, c2 = st.columns(2)
        pub_file = c1.file_uploader("Публічний")
        prv_file = c2.file_uploader("Приватний")
        download_btn = st.button("Завантажити")

        if pub_file and prv_file and download_btn:
            pub = pub_file.read()
            prv = prv_file.read()

            st.session_state.update({"pub": pub})
            st.session_state.update({"prv": prv})
            st.success("Ключі було завантажено")
            time.sleep(3)
            st.rerun()

    if pub and prv:
        c1, c2 = st.columns(2)
        
        text = c1.text_area("Текст для шифрування")
        encode_btn = c1.button("Шифрувати")

        if encode_btn:
            result = AbsRSA.encrypt(pub, text.encode())
            c1.download_button("Результат", result, "RSA_cipher.txt")

        file = c2.file_uploader("Завантажити")
        decode_btn = c2.button("Розшифрувати")

        if decode_btn:
            result = AbsRSA.decrypt(prv, file.read())
            c2.text(result.decode())
            c2.download_button("Результат", result.decode(), "result.txt")



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
        code()
    except Exception as ex_:
        st.error(f"{ex_}")


if __name__ == "__main__":
    main()