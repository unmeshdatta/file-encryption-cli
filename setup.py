from setuptools import setup, find_packages

setup(
    name="file-encryption-cli",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "cryptography",
        "python-gnupg",
        "click",
        "argon2-cffi",
        "keyring"
    ],
    entry_points={
        'console_scripts': ['encrypt-cli=cli.main:cli']
    },
)
