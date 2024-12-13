import numpy as np
import typing

from Crypto.Cipher import AES, DES, DES3


class AbsCipher:
    def des_pad(self, text, key_len):
        text_len = len(text)
        n = int(np.ceil(text_len ** (1/key_len)))
        return text + b" " * (key_len ** n - text_len)
    
    def des3_pad(self, text):
        n = 8 - len(text) % 8
        return text + b" " * n
    

    def encrypt(
        self, 
        text: bytes, 
        key: bytes,
        cipher_name: typing.Literal["AES", "DES", "DES3"],
        *args, **kwargs
    ) -> bytes | None:
        if cipher_name == "DES":
            padded_text = self.des_pad(text, len(key))
            cipher = DES.new(key, DES.MODE_ECB)
            result = cipher.encrypt(padded_text)
            return {
                "result": result
            }
        elif cipher_name == "DES3":
            padded_text = self.des3_pad(text)
            cipher = DES3.new(key, DES3.MODE_ECB)
            result = cipher.encrypt(padded_text)
            return {
                "result": result
            }
        elif cipher_name == "AES":
            cipher = AES.new(key, AES.MODE_EAX)
            nonce = cipher.nonce
            result, tag = cipher.encrypt_and_digest(text)
            return {
                "nonce": nonce,
                "result": result,
                "tag": tag
            }
        
        return None


    def decrypt(
        self, 
        text: bytes, 
        key: bytes,
        cipher_name: typing.Literal["AES", "DES", "DES3"],
        nonce: str = None,
        tag: str = None,
        *args, **kwargs
    ):
        if cipher_name == "DES":
            cipher = DES.new(key, DES.MODE_ECB)
            return cipher.decrypt(text)
        elif cipher_name == "DES3":
            cipher = DES3.new(key, DES.MODE_ECB)
            return cipher.decrypt(text)
        elif cipher_name == "AES":
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            return cipher.decrypt(text)
        
        return None