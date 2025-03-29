
import gnupg
import os

class PGPHandler:
    def __init__(self, gnupg_home=None):
        self.gpg = gnupg.GPG(gnupghome=gnupg_home or os.path.expanduser("~/.gnupg"))

    def generate_keypair(self, name_email):
        input_data = self.gpg.gen_key_input(
            name_email=name_email,
            key_type="RSA",
            key_length=4096,
            passphrase=None
        )
        return self.gpg.gen_key(input_data)

    def encrypt_file(self, infile, outfile, recipients, armor=False):
        with open(infile, 'rb') as f:
            status = self.gpg.encrypt_file(
                f, recipients=recipients, output=outfile, always_trust=True, armor=armor
            )
        return status.ok

    def decrypt_file(self, infile, outfile, passphrase=None):
        with open(infile, 'rb') as f:
            status = self.gpg.decrypt_file(f, output=outfile, passphrase=passphrase)
        return status.ok

    def list_keys(self):
        return self.gpg.list_keys()

    def import_key(self, key_data):
        return self.gpg.import_keys(key_data)

    def export_key(self, fingerprint):
        return self.gpg.export_keys(fingerprint)

    def delete_key(self, fingerprint, secret=True):
        if secret:
            self.gpg.delete_keys(fingerprint, True)
        self.gpg.delete_keys(fingerprint)
