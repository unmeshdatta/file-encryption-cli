# tests/test_pgp.py

import tempfile
from encryption.pgp import PGPHandler

def test_pgp_key_generation_and_listing():
    pgp = PGPHandler()
    key = pgp.generate_keypair("test@example.com")
    assert key
    keys = pgp.list_keys()
    assert any(k['fingerprint'] == key.fingerprint for k in keys)
