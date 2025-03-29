# tests/test_aes.py

import os
import tempfile
from encryption.aes import AESCipher

def test_aes_encryption_decryption():
    key = AESCipher.generate_key()
    iv = AESCipher.generate_iv()
    cipher = AESCipher(key, iv)

    data = b"Test data for AES encryption"
    with tempfile.NamedTemporaryFile(delete=False) as f_in:
        f_in.write(data)
        input_path = f_in.name

    encrypted_path = input_path + ".enc"
    decrypted_path = input_path + ".dec"

    cipher.encrypt_cbc(input_path, encrypted_path)
    cipher.decrypt_cbc(encrypted_path, decrypted_path)

    with open(decrypted_path, 'rb') as f:
        assert f.read() == data

    os.remove(input_path)
    os.remove(encrypted_path)
    os.remove(decrypted_path)
