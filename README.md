# File Encryption CLI Tool

Encrypt and decrypt files using AES-256 (CBC/GCM) and PGP.

## Features
- AES-256 encryption (CBC/GCM)
- PGP (RSA/ECC) support
- Secure key vault
- CLI with Click

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python -m cli.main encrypt file.txt --algo aes
```