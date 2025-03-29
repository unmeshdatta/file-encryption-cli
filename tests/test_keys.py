# tests/test_keys.py

import os
from encryption.key_vault import KeyVault

def test_key_vault_store_and_retrieve():
    key = os.urandom(32)
    vault = KeyVault("testpass")
    vault.store_key("testkey", "aes", key)
    fetched = vault.retrieve_key("testkey")
    assert key == fetched
