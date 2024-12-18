from .rsa_key_manager import RsaKeyManager

load_public_key_from_file = RsaKeyManager.load_public_key_from_file
load_private_key_from_file = RsaKeyManager.load_private_key_from_file

save_public_key_to_file = RsaKeyManager.save_public_key_to_file
save_private_key_to_file = RsaKeyManager.save_private_key_to_file

generate_private_key = RsaKeyManager.generate_private_key
generate_public_key = RsaKeyManager.generate_public_key

serialize_public_key = RsaKeyManager.serialize_public_key


__all__ = [
    "load_public_key_from_file",
    "load_private_key_from_file",
    "save_public_key_to_file",
    "save_private_key_to_file",
    "generate_private_key",
    "generate_public_key",
    "serialize_public_key",
]
