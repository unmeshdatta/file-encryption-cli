
import sqlite3
import base64
import os
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

DB_FILE = os.path.expanduser("~/.keyvault.db")

class KeyVault:
    def __init__(self, master_password):
        self.key = self.derive_key(master_password)
        self.conn = sqlite3.connect(DB_FILE)
        self._init_db()

    def derive_key(self, password):
        salt = b'secure_salt'
        kdf = Argon2id(length=32, salt=salt, time_cost=2, memory_cost=51200, parallelism=2)
        return kdf.derive(password.encode())

    def _init_db(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS keys (
                        name TEXT PRIMARY KEY,
                        type TEXT,
                        key BLOB)''')
        self.conn.commit()

    def encrypt(self, plaintext):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv))
        encryptor = cipher.encryptor()
        return base64.b64encode(iv + encryptor.update(plaintext) + encryptor.finalize())

    def decrypt(self, ciphertext):
        data = base64.b64decode(ciphertext)
        iv = data[:16]
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv))
        decryptor = cipher.decryptor()
        return decryptor.update(data[16:]) + decryptor.finalize()

    def store_key(self, name, key_type, key_data):
        encrypted = self.encrypt(key_data)
        c = self.conn.cursor()
        c.execute("REPLACE INTO keys (name, type, key) VALUES (?, ?, ?)",
                  (name, key_type, encrypted))
        self.conn.commit()

    def retrieve_key(self, name):
        c = self.conn.cursor()
        c.execute("SELECT key FROM keys WHERE name=?", (name,))
        row = c.fetchone()
        return self.decrypt(row[0]) if row else None
