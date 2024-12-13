from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA1


class AbsRSA:
    @staticmethod
    def gen_keys(key_len: int) -> tuple[bytes, bytes]:
        key = RSA.generate(key_len)
        return key.public_key().export_key(), key.export_key()
    

    @staticmethod
    def encrypt(public_key: bytes, text: bytes):
        cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
        return cipher.encrypt(text)
    

    @staticmethod
    def decrypt(private_key: bytes, text: bytes):
        cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
        return cipher.decrypt(text)
    

class Subscription:
    @staticmethod
    def encrypt(public_key: bytes, text: bytes):
        hash = SHA1.new(text)
        return AbsRSA.encrypt(public_key, hash.digest()), hash.digest()
    

    @staticmethod
    def decrypt(private_key: bytes, text: bytes):
        return AbsRSA.decrypt(private_key, text)
