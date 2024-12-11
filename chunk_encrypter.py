from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from rsa_key_manager import RsaKeyManager
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey
from constants import Path
import logging

logging.basicConfig(level=logging.INFO)

class ChunkEncrypter: 
    """
    Class responsible for encrypting and decrypting chunks of data using RSA
    """
    def __init__(self, key_manager: RsaKeyManager):
        """
        Initializes a ChunkEncrypter instance with a specified key manager.

        :param key_manager: An instance of RsaKeyManager used for key management operations.
        """
        self.key_manager = key_manager
        self._public_key = None
        self._private_key = None
     
    @property
    def public_key(self) -> RSAPublicKey:
        """
        Public key used for encryption. Loaded from PUBLIC_KEY_FILE on first call.

        :return: An instance of RSAPublicKey.
        """
        if not self._public_key:
            self._public_key = self.key_manager.load_public_key_from_file(Path.PUBLIC_KEY_FILE)
        return self._public_key
    
    @property
    def private_key(self) -> RSAPrivateKey:
        """
        Private key used for decryption. Loaded from PRIVATE_KEY_FILE on first call.

        :return: An instance of RSAPrivateKey.
        """
        if not self._private_key:
            self._private_key = self.key_manager.load_private_key_from_file(Path.PRIVATE_KEY_FILE)
        return self._private_key
    def encrypt_chunk(self, chunk: bytes)-> bytes:     
        """
        Encrypts a given chunk of data using public key
        
        :param chunk: The bytes chunk to be encrypted
        :return: The encrypted chunk
        """
        logging.info(f"Encrypting chunk of size: {len(chunk)}")

        return self.public_key.encrypt(
            chunk,
            self.get_padding()
        )
    
    def decrypt_chunk(self, chunk: bytes) -> bytes:       
        """
        Decrypts a given chunk of data using private key

        :param chunk: Bytes object to be decrypted
        :return: Decrypted bytes object
        """
        logging.info(f"Decrypting chunk of size: {len(chunk)}")
        return self.private_key.decrypt(
            chunk,
            self.get_padding()
        )
    
    def get_padding(self) -> padding.OAEP:
        """
        Returns the padding scheme used for encryption and decryption.
        In this case, it is OAEP with SHA-256 hash and MGF1 padding.
        """
        return padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
        )