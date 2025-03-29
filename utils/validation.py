
import os

def validate_file_path(path):
    if ".." in path or not os.path.exists(path):
        raise ValueError("Invalid or unsafe file path.")
