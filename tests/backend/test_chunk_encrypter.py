from unittest.mock import MagicMock, patch
import pytest

from backend.chunk_encrypter import ChunkEncrypter
from backend.rsa_key_manager import RsaKeyManager
from backend.constants import Path
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


class TestChunkEncrypter:
    public_key = MagicMock()
    private_key = MagicMock()

    @pytest.fixture
    def instance_without_keys(self):
        yield ChunkEncrypter(MagicMock(spec=RsaKeyManager))

    @pytest.fixture
    def instance_with_keys(self):
        yield ChunkEncrypter(
            MagicMock(spec=RsaKeyManager), self.public_key, self.private_key
        )

    def test_property_public_key(self, instance_without_keys, instance_with_keys):
        instance_without_keys.key_manager.load_public_key_from_file.return_value = (
            self.public_key
        )

        instance_without_keys.public_key
        instance_without_keys.key_manager.load_public_key_from_file.assert_called_once_with(
            Path.PUBLIC_KEY_FILE
        )

        instance_with_keys.public_key
        instance_with_keys.key_manager.load_public_key_from_file.assert_not_called()

    def test_property_private_key(self, instance_without_keys, instance_with_keys):

        instance_without_keys.key_manager.load_private_key_from_file.return_value = (
            self.private_key
        )

        instance_without_keys.private_key
        instance_without_keys.key_manager.load_private_key_from_file.assert_called_once_with(
            Path.PRIVATE_KEY_FILE
        )

        instance_with_keys.private_key
        instance_with_keys.key_manager.load_private_key_from_file.assert_not_called()

    def test_encrypt_chunk(self, instance_with_keys):
        with patch.object(instance_with_keys, "get_padding") as mock_get_padding:
            iwk = instance_with_keys
            chunk = b"chunk"
            encrypted_chunk = b"encrypted_chunk"
            padding = "mock_padding"

            mock_get_padding.return_value = padding
            iwk.public_key.encrypt.return_value = encrypted_chunk

            result = iwk.encrypt_chunk(chunk)

            mock_get_padding.assert_called_once()
            iwk.public_key.encrypt.assert_called_once_with(chunk, padding)
            assert result == encrypted_chunk

    def test_decrypt_chunk(self, instance_with_keys):
        with patch.object(instance_with_keys, "get_padding") as mock_get_padding:
            iwk = instance_with_keys
            chunk = b"chunk"
            decrypted_chunk = b"decrypted_chunk"
            padding = "mock_padding"

            mock_get_padding.return_value = padding
            iwk.private_key.decrypt.return_value = decrypted_chunk

            result = iwk.decrypt_chunk(chunk)

            mock_get_padding.assert_called_once()
            iwk.private_key.decrypt.assert_called_once_with(chunk, padding)
            assert result == decrypted_chunk

    def test_get_padding(self, instance_with_keys):
        padding_scheme: padding.OAEP = instance_with_keys.get_padding()

        assert isinstance(padding_scheme, padding.OAEP)
        assert isinstance(padding_scheme.mgf, padding.MGF1)
        assert isinstance(padding_scheme.algorithm, hashes.SHA256)
        assert isinstance(padding_scheme.algorithm, hashes.SHA256)
        assert padding_scheme._label is None
