import os
import hashlib
import binascii
import hmac


class Hasher:
    @staticmethod
    def get_hash_password(password: str) -> str:
        """
        Gera um hash usando PBKDF2-HMAC-SHA256.
        Retorna uma string no formato: salt_hex:hash_hex
        """
        salt = os.urandom(16)
        dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
        return binascii.hexlify(salt).decode() + ':' + binascii.hexlify(dk).decode()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        try:
            salt_hex, dk_hex = hashed_password.split(':')
        except ValueError:
            return False
        salt = binascii.unhexlify(salt_hex)
        expected = binascii.unhexlify(dk_hex)
        new_dk = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100_000)
        return hmac.compare_digest(new_dk, expected)