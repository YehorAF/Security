import os
import pickle
import psutil
import uuid

import streamlit as st

from components import AbsRSA, Subscription


def code():
    action = st.radio("Підпис", ["шифрувати", "перевірити"])

    if action == "шифрувати":
        text = st.text_input("Повідомлення")
        code_btn = st.button("Шифрувати")

        if code_btn and text:
            pub, prv = AbsRSA.gen_keys(1024)
            res, hash = Subscription.encrypt(pub, text.encode())
            action_id = uuid.uuid4().hex

            st.session_state.update({
                action_id: {
                    "pub":pub,
                    "action_id": action_id,
                    "prv": prv,
                    "hash": hash
                }
            })

            st.download_button(
                "Результат", 
                pickle.dumps({"pub": pub, "res": res, "action_id": action_id}),
                f"{action_id}_sub.json"
            )
    elif action == "перевірити":
        file = st.file_uploader("Підпис")
        check_btn = st.button("Перевірити")

        if check_btn and file:
            data = pickle.load(file)
            action_id = data["action_id"]
            pub = data["pub"]
            res = data["res"]

            local_data = st.session_state.get(action_id)
            if not local_data or local_data["pub"] != pub:
                raise ValueError("Підпис не дійсний. Не знайдено ключа")
            
            prv = local_data["prv"]
            hash = AbsRSA.decrypt(prv, res)

            if hash != local_data["hash"]:
                raise ValueError("Підпис не дійсний. Не відповідає геш")
            
            st.success("Підпис дійсний")



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