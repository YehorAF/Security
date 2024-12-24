import os
import psutil
import json

import streamlit as st

import components


def set_keys():
    c1, c2 = st.columns(2)

    key_size = st.number_input("Довжина ключа", min_value=8, value=8)
    gen_btn = st.button("Згенерувати", key="gen")

    if gen_btn:
        pub, prv = components.KnapsackCipher.generate_keys(key_size)
        st.session_state.update({"pub": pub, "prv": prv})

    pub = st.session_state.get("pub")
    prv = st.session_state.get("prv")

    if pub and prv:
        pub_dict = {
            "key": pub
        }
        prv_dict = {
            "seq": prv[0],
            "m": prv[1],
            "w": prv[2]
        }

        c1.download_button(
            label="Публічний ключ", 
            data=json.dumps(pub_dict), 
            file_name="pub.json",
            key="down_pub_key"
        )
        c2.download_button(
            label="Приватний ключ", 
            data=json.dumps(prv_dict), 
            file_name="prv.json",
            key="down_prv_key"
        )

    c1, c2 = st.columns(2)
    pub_key = c1.file_uploader("Публічний ключ", key="upl_pub_key")
    prv_key = c2.file_uploader("Приватний ключ", key="upl_prv_key")
    upl_key_btn = st.button("Завантажити", key="upl_key_btn")

    if upl_key_btn and pub_key and prv_key:
        pub_key_res = json.loads(pub_key.read())
        prv_key_res = json.loads(prv_key.read())
        pub = pub_key_res["key"]
        prv = (prv_key_res["seq"], prv_key_res["m"], prv_key_res["w"])

        st.session_state.update({"pub": pub, "prv": prv})

    set_code_btn = st.button(
        "Перейти до кодування", key="set_code_state"
    )

    if set_code_btn and pub and prv:
        st.session_state.update({"state": "code"})
        st.rerun()


def code():
    pub = st.session_state["pub"]
    prv = st.session_state["prv"]

    c1, c2 = st.columns(2)

    text = c1.text_area("Повідомлення")
    encode_btn = c1.button("Зашифрувати", key="encode_btn")

    if encode_btn:
        res = components.KnapsackCipher.encode(text, pub)
        c1.download_button(
            label="Результат", 
            data=json.dumps({"text": res}),
            file_name="res.json",
            key="down_res_btn"
        )

    file = c2.file_uploader("Зашифроване")
    decode_btn = c2.button("Розшифрувати", key="decode_btn")

    if decode_btn and file:
        res = json.loads(file.read())
        text = components.KnapsackCipher.decode(res["text"], prv)
        c2.empty().write(text)


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
        if st.session_state.get("state") == "code":
            code()
        else:
            set_keys()
    except Exception as ex_:
        st.error(f"{ex_}")


if __name__ == "__main__":
    main()