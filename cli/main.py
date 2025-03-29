
import click
from encryption.aes import AESCipher
from encryption.pgp import PGPHandler
from encryption.key_vault import KeyVault

@click.group()
def cli():
    pass

@cli.command()
@click.argument("file")
@click.option("--algo", type=click.Choice(["aes", "pgp"]), required=True)
@click.option("--output", type=str)
@click.option("--recipient-key", type=str)
def encrypt(file, algo, output, recipient_key):
    if algo == "aes":
        key = AESCipher.generate_key()
        iv = AESCipher.generate_iv()
        cipher = AESCipher(key, iv)
        output = output or file + ".enc"
        cipher.encrypt_cbc(file, output)
        click.echo(f"Encrypted with AES to {output}")
    elif algo == "pgp":
        pgp = PGPHandler()
        output = output or file + ".pgp"
        success = pgp.encrypt_file(file, output, recipients=[recipient_key])
        click.echo("PGP encryption success" if success else "PGP encryption failed")

@cli.command()
@click.argument("file")
@click.option("--output", type=str)
@click.option("--private-key", type=str)
def decrypt(file, output, private_key):
    if file.endswith(".enc"):
        key = click.prompt("Enter AES key (hex)", hide_input=True)
        iv = click.prompt("Enter AES IV (hex)", hide_input=True)
        cipher = AESCipher(bytes.fromhex(key), bytes.fromhex(iv))
        output = output or file.replace(".enc", ".dec")
        cipher.decrypt_cbc(file, output)
        click.echo(f"Decrypted to {output}")
    elif file.endswith(".pgp"):
        pgp = PGPHandler()
        output = output or file.replace(".pgp", ".dec")
        pgp.decrypt_file(file, output)
        click.echo(f"Decrypted PGP to {output}")

@cli.command()
@click.option("--type", "key_type", type=click.Choice(["aes", "pgp"]))
@click.option("--name", prompt=True)
def generate_key(key_type, name):
    if key_type == "aes":
        key = AESCipher.generate_key()
        vault = KeyVault(click.prompt("Master password", hide_input=True))
        vault.store_key(name, "aes", key)
        click.echo("AES key stored securely")
    elif key_type == "pgp":
        pgp = PGPHandler()
        pgp.generate_keypair(name)
        click.echo("PGP key generated")

if __name__ == "__main__":
    cli()
