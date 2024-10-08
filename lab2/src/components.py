from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import typing


class TabulaRecta:
    @staticmethod
    def generate_by_linear(
        a: int, b: int, p: int, *args, **kwargs
    ) -> int:
        return a * p + b


    @staticmethod
    def generate_by_nonlinear(
        a: int, b: int, c: int, p: int, *args, **kwargs
    ) -> int:
        return a * p ** 2 + b * p + c


class CaesarCipher:
    @staticmethod
    def encode_caesar(c: int, l: int, k: int) -> int:
        return (c + k) % l
    

    @staticmethod
    def decode_caesar(c: int, l: int, k: int) -> int:
        return (c + l - k % l) % l


class AlphabetCode:
    def __init__(self, valid_chars: str | list[str] = None, **alphabets):
        self.chars = {}
        self.alphabets = {}
        self.valid_chars = valid_chars or ""

        for name, chars in alphabets.items():
            codes, alphabet, char_list_len = self.form_alphabet(name, chars)

            self.chars |= codes
            self.alphabets |= {name: (alphabet, char_list_len)}


    @staticmethod
    def form_alphabet(
        name: str, chars: str | typing.Iterable[str]
    ) -> dict[str, tuple[int, int, str]]:
        if not chars:
            raise ValueError(f"Алфавіт {name} не заповнений")
        
        small_chars = AlphabetCode.select_chars(chars, "lower")
        big_chars = AlphabetCode.select_chars(chars, "upper")

        small_chars = AlphabetCode.to_codes(small_chars)
        big_chars = AlphabetCode.to_codes(big_chars)
        l1, l2 = len(small_chars), len(big_chars)
        char_list_len, alphabet = (
            (l1, list(small_chars.keys())) if l1 > l2 
            else (l2, list(big_chars.keys()))
        )

        return {
            k: (v, char_list_len, name) 
            for k, v in (small_chars | big_chars).items()
        }, alphabet, char_list_len


    @staticmethod
    def select_chars(
        chars: str | typing.Iterable[str], case: typing.Literal["lower", "upper"]
    ) -> str:
        func = {
            "lower": "islower",
            "upper": "isupper"
        }[case]

        result = ""
        for c in chars:
            if c.__getattribute__(func)():
                result += c

        return result


    @staticmethod
    def to_codes(chars: str | typing.Iterable[str]) -> dict[str, int]:
        return {c: i for i, c in enumerate(chars)}
    

    @staticmethod
    def choose_case(c: str, nc: str) -> str:
        if c.islower():
            return nc.lower()
        else:
            return nc.upper()
    

    def code_by_multiple_key_with_tabula_recta(
        self, 
        text: str, 
        a: int, 
        b: int, 
        action: typing.Literal["decode", "encode"],
        c: int = 0, 
        use_data_validation = False
    ) -> str:
        if a < 1 or b < 1:
            raise ValueError("Ключі не повинні бути меншими за 1")
        
        if c < 0:
            raise ValueError("Ключ c не повинен бути менши за 0")
        elif c == 0:
            gen_func = TabulaRecta.generate_by_linear
        elif c > 0:
            gen_func = TabulaRecta.generate_by_nonlinear

        func = {
            "encode": CaesarCipher.encode_caesar,
            "decode": CaesarCipher.decode_caesar
        }[action]
        
        result = ""
        for i, ch in enumerate(text):
            if v := self.chars.get(ch):
                code, l, name = v
                k = gen_func(a=a, b=b, p=i, c=c)
                ncode = func(code, l, k)
                nc: str = self.alphabets[name][0][ncode]
                result += self.choose_case(ch, nc)
            elif use_data_validation and ch not in self.valid_chars:
                raise ValueError(f"Некоректний символ: {ch}")
            else:
                result += ch

        return result


    def code_by_word_with_tabula_recta(
        self,
        text: str,
        keyword: str, 
        action: typing.Literal["decode", "encode"],
        use_data_validation = False
    ) -> str:
        kwl = len(keyword)
        if kwl < 1:
            raise ValueError(
                "Довжина ключового слова повинна бути більшою за 0"
            )
        
        func = {
            "encode": CaesarCipher.encode_caesar,
            "decode": CaesarCipher.decode_caesar
        }[action]
        
        result = ""
        for i, c in enumerate(text):
            if not (kwv := self.chars.get(keyword[i % kwl])):
                raise ValueError("Нема такого символу в доступному алфавіті")

            if v := self.chars.get(c):
                code, l, name = v
                kcode, _, _ = kwv
                ncode = func(code, l, kcode)
                nc: str = self.alphabets[name][0][ncode]
                result += self.choose_case(c, nc)
            elif use_data_validation and c not in self.valid_chars:
                raise ValueError(f"Некоректний символ: {c}")
            else:
                result += c

        return result


    def code_with_caesar_cypher(
        self, text: str, k: int, func, use_data_validation = False
    ) -> str:
        if k < 1:
            raise ValueError("Ключ повинен бути більшим за 0")

        lens = np.array([l for _, l in self.alphabets.values()])
        if not (lens > k).all():
            raise ValueError(
                "Ключ повинен бути меншим за потужність алфавіту"
            )
        
        result = ""
        for c in text:
            if v := self.chars.get(c):
                code, l, name = v
                ncode = func(code, l, k)
                nc: str = self.alphabets[name][0][ncode]
                result += self.choose_case(c, nc)
            elif use_data_validation and c not in self.valid_chars:
                raise ValueError(f"Некоректний символ: {c}")
            else:
                result += c

        return result
    

class FileCode:
    @staticmethod
    def code(
        file: bytes, 
        k: int, 
        l: int, 
        func, 
        use_index: typing.Literal["encode", "decode"] = None,
    ) -> bytes:
        if k < 1:
            raise ValueError("Ключ повинен бути більшим за 0")
        if l < 1:
            raise ValueError("Потужність набору даних має бути більшою за 0")
        if k >= l:
            raise ValueError(
                "Ключ повинен бути меншим за потужність набору даних"
            )
        
        result = []
        for i, c in enumerate(file):
            n = c
            if use_index == "encode":
                n += i
            elif use_index == "decode":
                n -= i
            result.append(func(n, l, k))
        return bytes(result)
    

class AttackTabulaRectaDetection:
    def __init__(self, tries: int, drop_tries: int) -> None:
        self._blocked = False
        self._tries = tries
        self._drop_tries = drop_tries
        self._history = pd.DataFrame(columns=[
            "text", "key", "action", "timestamp"
        ])


    def check_request(
        self, 
        text: str, 
        key: typing.Any, 
        action: typing.Literal["encode", "decode"],
        dt: datetime
    ):
        req_df = self._history[
            (self._history["action"] == action) &
            (self._history["timestamp"].between(
                dt - timedelta(seconds=self._drop_tries), dt
            )) &
            (self._history["text"] == text) 
        ]
        req_df_len = len(req_df) 
        if req_df_len >= self._tries:
            self._blocked = True
            raise OSError(
                "Досягнуто ліміт на розшифрування. Інтерфейс заблоковано"
            )


    def insert_request(
        self, 
        text: str, 
        key: typing.Any,
        action: typing.Literal["encode", "decode"],
        dt: datetime
    ):
        if self._blocked:
            raise OSError(
                "Досягнуто ліміт на розшифрування. Інтерфейс заблоковано"
            )
        self._history.loc[len(self._history)] = (text, key, action, dt)