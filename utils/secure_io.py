
import os
import tempfile
import shutil

def atomic_write(filepath, data):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(data)
        tempname = tmp.name
    shutil.move(tempname, filepath)

def secure_delete(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'ba+', buffering=0) as delfile:
            length = delfile.tell()
            delfile.seek(0)
            delfile.write(os.urandom(length))
        os.remove(filepath)
