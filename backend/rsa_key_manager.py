##########################################################################
#### This key manager is used for generating RSA-4096 security level keys
##########################################################################

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from tools.toolkit import Tools as t
from backend.constants import Rsa
import zipfile
import io
import os

logging = t.all.logging_config_screen()
logging = logging.getLogger(__name__)


class RsaKeyManager:

    def generate_private_key(self):
        """
        Generates a private RSA key for use with this key manager.

        :return: The generated private key
        """

        private_key = rsa.generate_private_key(
            public_exponent=Rsa.PUBLIC_EXPONENT,
            key_size=Rsa.KEY_SIZE,
            backend=default_backend(),
        )

        return private_key

    def generate_public_key(self, private_key: rsa.RSAPrivateKey) -> rsa.RSAPublicKey:
        """
        Generates a public RSA key from the given private key.

        :param private_key: An instance of RSAPrivateKey from which to derive the public key.
        :return: The corresponding RSAPublicKey.
        :raises TypeError: If the private_key is not an instance of RSAPrivateKey.
        """

        if not isinstance(private_key, rsa.RSAPrivateKey):
            raise TypeError("Private_key must be an instance of RSAPrivateKey")

        return private_key.public_key()

    def encrypt_private_key(self, private_key, password=None):
        """
        Encrypts a given private key using the given password.

        :param private_key: An instance of RSAPrivateKey to be encrypted.
        :param password: An optional password to encrypt the private key. If None, the key is encrypted without encryption.
        :return: The encrypted private key as a PEM-encoded bytes object.
        """
        encryption = (
            serialization.BestAvailableEncryption(password.encode("utf-8"))
            if password
            else serialization.NoEncryption()
        )

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption,
        )

        return private_pem

    def encrypt_public_key(self, public_key):
        """
        Encrypts the given public RSA key into PEM format.

        :param public_key: An instance of RSAPublicKey to be encrypted.
        :return: The PEM-encoded public key as bytes.
        """

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        return public_pem

    def save_private_key_to_file(
        self, output_pem_file_path, password: str = None, private_key=None
    ):
        """
        Saves the given private RSA key to a specified PEM file path, optionally encrypting it with a password.

        :param private_key: The private RSA key to be saved.
        :param pem_file_path: The file path where the PEM-formatted private key will be saved.
        :param password: An optional password to encrypt the private key. If None, the key is saved without encryption.
        """
        if not private_key:
            private_key = self.generate_private_key()

        with open(output_pem_file_path, "wb") as private_file:
            private_pem = self.encrypt_private_key(private_key, password)
            private_file.write(private_pem)
        logging.info(f"Private key saved to {output_pem_file_path}")

    def save_public_key_to_file(self, public_key, pem_file_path):
        """
        Saves the given public RSA key to a specified PEM file path.

        :param public_key: The public RSA key to be saved.
        :param pem_file_path: The file path where the PEM-formatted public key will be saved.
        """

        with open(pem_file_path, "wb") as public_file:
            public_pem = self.encrypt_public_key(public_key)
            public_file.write(public_pem)
        logging.info(f"Public key saved to {pem_file_path}")

    def load_private_key_from_file(self, pem_file_path, password: str = None):
        """
        Loads a private RSA key from a specified PEM file path, optionally decrypting it with a password.

        :param pem_file_path: The file path where the PEM-formatted private key is saved.
        :param password: An optional password to decrypt the private key. If None, the key is loaded without decryption.
        :return: The loaded private RSA key.
        :raises FileNotFoundError: If the private key file is not found.
        :raises Exception: If the private key file is not in the correct format or has an invalid password.
        """

        try:
            with open(pem_file_path, "rb") as private_file:
                private_key = self.serialize_private_key(private_file.read(), password)
                logging.info(f"Private key loaded from {pem_file_path}")
                return private_key
        except FileNotFoundError:
            raise FileNotFoundError(f"Private key file not found: {pem_file_path}")
        except Exception as e:
            logging.error(e)
            raise Exception(
                f"Failed to process private key. Please check file format and try again.\n\nAdditional Info:\n {e}"
            )

    def load_public_key_from_file(self, pem_file_path):
        """
        Loads a public RSA key from a specified PEM file path.

        :param pem_file_path: The file path where the PEM-formatted public key is saved.
        :return: The loaded public RSA key.
        """

        try:
            with open(pem_file_path, "rb") as public_file:

                public_key = self.serialize_public_key(public_file.read())
                logging.info(f"Public key loaded from {pem_file_path}")
                return public_key
        except FileNotFoundError:
            raise FileNotFoundError(f"Public key file not found: {pem_file_path}")
        except Exception as e:
            raise Exception(
                f"Failed to process public key. Please check file format and try again.\n\nAdditional Info:\n {e}"
            )

    def serialize_public_key(self, public_key):
        """
        Deserializes a given public key string into a cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey object.

        :param public_key: The public key string to be deserialized.
        :return: The deserialized RSAPublicKey object.
        """

        data = public_key.encode("utf-8") if type(public_key) is str else public_key

        try:
            serialized_public_key = serialization.load_pem_public_key(
                data, backend=default_backend()
            )
            return serialized_public_key
        except Exception as e:
            raise Exception(
                f"Failed to serialize public key, most likely key was corrupted, or you made a mistake, when provided the key.\nPlease check your input, and try again.\n\nAdditional Info:\n {e}"
            )

    def serialize_private_key(self, private_key, password: str):
        """
        Deserializes a given private key string into a cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey object.

        :param private_key: The private key string to be deserialized.
        :param password: An optional password to decrypt the private key. If None, the key is loaded without decryption.
        :return: The deserialized RSAPrivateKey object.
        """
        data = private_key.encode("utf-8") if type(private_key) is str else private_key

        if password is not None:
            password = password.encode("utf-8")

        serialized_private_key = serialization.load_pem_private_key(
            data, password=password, backend=default_backend()
        )
        return serialized_private_key

    def export_keys_to_zip(self, private_key_data, public_key_data, zip_filename):
        """
        Exports the given private and public key data to a ZIP file.

        This function creates a ZIP archive containing the provided private and
        public key data as separate files named 'private_key.pem' and 'public_key.pem',
        respectively. If the directory for the ZIP file does not exist, it will be created.

        :param private_key_data: The private key data to be added to the ZIP file.
        :param public_key_data: The public key data to be added to the ZIP file.
        :param zip_filename: The path where the ZIP file will be saved.
        """

        zip_dir = os.path.dirname(zip_filename)
        if zip_dir and not os.path.exists(zip_dir):
            os.makedirs(zip_dir)

        # Create a BytesIO buffer to hold both key data in memory
        private_key_buffer = io.BytesIO(
            private_key_data
        )  # assuming private_key_data is a string
        public_key_buffer = io.BytesIO(
            public_key_data
        )  # assuming public_key_data is a string

        # Create a ZIP file in write mode
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as archive:
            # Write the private key to the ZIP file
            archive.writestr("private_key.pem", private_key_buffer.getvalue())
            logging.info(f"Private key added to {zip_filename}")

            # Write the public key to the ZIP file
            archive.writestr("public_key.pem", public_key_buffer.getvalue())
            logging.info(f"Public key added to {zip_filename}")
