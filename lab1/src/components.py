import numpy as np
import typing


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


    def code(
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

                if c.islower():
                    result += nc.lower()
                else:
                    result += nc.upper()
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