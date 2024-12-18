###############################################################
# !Warning!:
# The chunk size for encryption can be changed, but must be no more than 446 bytes
# The chunk size for decryption must be exactly 512 bytes to be compatible with the encryption algorithm.
###############################################################


class Path:
    PUBLIC_KEY_FILE: str = "public_key.pem"
    PRIVATE_KEY_FILE: str = "private_key.pem"


class Size:
    ENCRYPTION_CHUNK: int = 446
    DECRYPTION_CHUNK: int = 512


class Rsa:
    KEY_SIZE: int = 4096
    PUBLIC_EXPONENT: int = 65537
