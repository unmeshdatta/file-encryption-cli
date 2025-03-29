
# 🔐 File Encryption CLI Tool

A command-line tool to securely encrypt and decrypt files using **AES-256 (CBC/GCM)** and **PGP (RSA/ECC)** algorithms. Includes secure key management, OpenPGP compatibility, and a local encrypted key vault.

---

## ✨ Features

- ✅ AES-256 encryption in **CBC** and **GCM** modes  
- ✅ PGP encryption (Symmetric & Asymmetric) with **RSA**/**ECC**  
- ✅ Secure key generation and local vault (SQLite + AES + Argon2id)  
- ✅ OpenPGP support (.pgp/.gpg files, ASCII-armored output)  
- ✅ CLI powered by `Click` with helpful prompts and options  
- ✅ Cross-platform: Linux, macOS, Windows  

---

## 🧰 Requirements

- Python 3.9+
- GnuPG (for PGP support)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Quick Start

### 🔐 Encrypt a file using AES

```bash
python -m cli.main encrypt myfile.txt --algo aes
```

### 🔐 Encrypt using PGP

```bash
python -m cli.main encrypt secret.docx --algo pgp --recipient-key someone@example.com
```

### 🔓 Decrypt AES-encrypted file

```bash
python -m cli.main decrypt myfile.txt.enc
```

---

## 🔑 Key Management

### Generate AES Key

```bash
python -m cli.main generate-key --type aes --name myaeskey
```

### Generate PGP Key Pair

```bash
python -m cli.main generate-key --type pgp --name user@example.com
```

Keys are stored in a secure local vault (`~/.keyvault.db`), protected by a master password using **Argon2id**.

---

## 🧪 Testing

Run unit tests:

```bash
pytest tests/
```

---

## 📂 Project Structure

```
file-encryption-cli/
│
├── cli/              # CLI commands (encrypt, decrypt, etc.)
├── encryption/       # Core logic (AES, PGP, KeyVault)
├── utils/            # Logging, validation, secure file IO
├── tests/            # Unit tests
├── README.md
├── requirements.txt
├── setup.py
├── pyproject.toml
```

---

## 📸 Screenshots

> Add screenshots here of encryption/decryption in action

---

## 📦 Packaging

Create executable (optional):

```bash
pip install pyinstaller
pyinstaller --onefile cli/main.py
```

---

## ✅ Security Notes

- Keys never stored in plaintext  
- Encrypted vault secured with AES-256 and Argon2id  
- AES-CBC with HMAC-SHA256 for integrity  
- AES-GCM with built-in authentication  
- Input sanitization and memory handling considered  

---
