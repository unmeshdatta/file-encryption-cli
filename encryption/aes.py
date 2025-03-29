
import os
import hmac
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

CHUNK_SIZE = 64 * 1024  # 64KB

class AESCipher:
    def __init__(self, key, iv=None):
        self.key = key
        self.iv = iv

    @staticmethod
    def generate_key():
        return os.urandom(32)  # AES-256

    @staticmethod
    def generate_iv():
        return os.urandom(16)

    def encrypt_cbc(self, infile, outfile):
        iv = self.iv or self.generate_iv()
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        hmac_digest = hmac.new(self.key, digestmod=hashlib.sha256)

        with open(infile, 'rb') as fin, open(outfile, 'wb') as fout:
            fout.write(iv)
            while True:
                chunk = fin.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    break
                if len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)
                encrypted = encryptor.update(chunk)
                fout.write(encrypted)
                hmac_digest.update(encrypted)
            fout.write(encryptor.finalize())
            fout.write(hmac_digest.digest())

    def decrypt_cbc(self, infile, outfile):
        with open(infile, 'rb') as fin:
            iv = fin.read(16)
            content = fin.read()
            data, received_hmac = content[:-32], content[-32:]

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        hmac_digest = hmac.new(self.key, digestmod=hashlib.sha256)
        hmac_digest.update(data)

        if not hmac.compare_digest(hmac_digest.digest(), received_hmac):
            raise ValueError("HMAC integrity check failed.")

        with open(outfile, 'wb') as fout:
            fout.write(decryptor.update(data) + decryptor.finalize())

    def encrypt_gcm(self, infile, outfile):
        iv = os.urandom(12)
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        with open(infile, 'rb') as fin, open(outfile, 'wb') as fout:
            fout.write(iv)
            while chunk := fin.read(CHUNK_SIZE):
                fout.write(encryptor.update(chunk))
            fout.write(encryptor.finalize())
            fout.write(encryptor.tag)

    def decrypt_gcm(self, infile, outfile):
        with open(infile, 'rb') as fin:
            iv = fin.read(12)
            content = fin.read()
            tag = content[-16:]
            data = content[:-16]

        cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()

        with open(outfile, 'wb') as fout:
            fout.write(decryptor.update(data) + decryptor.finalize())
