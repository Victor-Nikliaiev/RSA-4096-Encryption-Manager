from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from unittest.mock import MagicMock, mock_open, patch
from backend.rsa_key_manager import RsaKeyManager
from backend.constants.constants import Rsa
import tempfile
import zipfile
import pytest
import os


class TestRsaKeyManager:
    @pytest.fixture(scope="function", autouse=True)
    def autorun(self):
        """
        Fixture to set up and tear down the RsaKeyManager test environment.

        This fixture is automatically used for each test function in the
        TestRsaKeyManager class. It initializes the RsaKeyManager instance.

        After the test, it ensures the RsaKeyManager instance is properly closed and cleaned up.

        :param self: The test class instance.
        :yield: The RsaKeyManager instance.
        """

        self.km = RsaKeyManager()
        yield

    def test_generate_private_key(self):
        """
        Tests the generate_private_key method of the RsaKeyManager class.

        This test verifies that the generate_private_key method correctly calls the
        rsa.generate_private_key function with the expected parameters and returns
        the generated private key. The test uses a mock to replace the
        generate_private_key function and checks that it is called with the correct
        public exponent, key size, and backend. It asserts that the returned value
        matches the mocked private key.
        """

        with patch(
            "cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key"
        ) as mock_generate_private_key:
            mock_private_key = MagicMock()
            mock_generate_private_key.return_value = mock_private_key

            result = self.km.generate_private_key()
            mock_generate_private_key.assert_called_once_with(
                public_exponent=Rsa.PUBLIC_EXPONENT,
                key_size=Rsa.KEY_SIZE,
                backend=default_backend(),
            )
            assert result == mock_private_key

    def test_generate_public_key(self):
        """
        Tests the generate_public_key method of the RsaKeyManager class.

        This test verifies that the generate_public_key method correctly calls the
        public_key method of the given private key and returns the generated public
        key. The test uses a mock to replace the private key and checks that the
        public_key method is called once. It asserts that the returned value matches
        the mocked public key.

        The test also verifies that the method raises a TypeError when the private_key
        parameter is not an instance of RSAPrivateKey.
        """

        private_key = MagicMock(spec=rsa.RSAPrivateKey)
        public_key = MagicMock()
        private_key.public_key.return_value = public_key

        result = self.km.generate_public_key(private_key)
        private_key.public_key.assert_called_once()
        assert result == public_key

        with pytest.raises(
            TypeError, match="Private_key must be an instance of RSAPrivateKey"
        ):
            private_key = MagicMock()
            self.km.generate_public_key(private_key)

    def test_encrypt_private_key(self):
        """
        Tests the encrypt_private_key method of the RsaKeyManager class.

        This test verifies that the method correctly encrypts the given private key
        using the given password. It also verifies that the method correctly handles
        the case where the password is not provided and encrypts the private key
        without encryption.

        The test uses mock objects to replace the private key, the password encryption
        algorithm, and the private key bytes. It checks that the method calls the
        private_bytes method of the given private key with the correct arguments
        and that the method returns the encrypted private key.

        The test also verifies that the method raises a TypeError when the private_key
        parameter is not an instance of RSAPrivateKey.
        """

        private_key = MagicMock()
        password = "my_password"
        encrypted_private_key = MagicMock()
        private_key.private_bytes.return_value = encrypted_private_key
        with patch(
            "cryptography.hazmat.primitives.serialization.BestAvailableEncryption"
        ) as mock_pass_encryption, patch(
            "cryptography.hazmat.primitives.serialization.NoEncryption"
        ) as mock_encryption:
            mock_encryption_instance = MagicMock()
            mock_pass_encryption.return_value = mock_encryption_instance

            result = self.km.encrypt_private_key(private_key, password)

            private_key.private_bytes.assert_called_once_with(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=mock_encryption_instance,
            )
            assert result is encrypted_private_key

            mock_encryption.return_value = mock_encryption_instance
            result = self.km.encrypt_private_key(private_key)
            private_key.private_bytes.assert_any_call(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=mock_encryption_instance,
            )

            assert result is encrypted_private_key

    def test_encrypt_public_key(self):
        """
        Tests the encrypt_public_key method of the RsaKeyManager class.

        This test verifies that the method correctly encrypts the given public key
        into PEM format. It uses a mock object to replace the public key and checks
        that the method calls the public_bytes method of the given public key with
        the correct arguments and that the method returns the encrypted public key.

        Scenarios tested:
        1. A valid public key is correctly encrypted into PEM format.
        """

        public_key = MagicMock()
        encrypted_public_key = MagicMock()
        public_key.public_bytes.return_value = encrypted_public_key

        result = self.km.encrypt_public_key(public_key)

        public_key.public_bytes.assert_called_once_with(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        assert result is encrypted_public_key

    def test_save_private_key_to_file(self):
        """
        Tests the save_private_key_to_file method of the RsaKeyManager class.

        This test verifies that the method correctly saves the given private key
        to a file with the given path. It uses a mock object to replace the open
        function and checks that the method calls the open function with the
        correct arguments and that the method calls the encrypt_private_key
        method with the correct arguments.

        Scenarios tested:
        1. A valid private key is correctly saved to a file with the given path.

        :return: None
        """

        mock_open_func = mock_open()
        with patch("builtins.open", mock_open_func), patch.object(
            self.km, "encrypt_private_key"
        ) as mock_encrypt_private_key:
            private_key = MagicMock()
            private_pem = MagicMock()
            password = None
            mock_encrypt_private_key.return_value = private_pem

            self.km.save_private_key_to_file("output_file.pem", private_key=private_key)

            mock_open_func.assert_called_once_with("output_file.pem", "wb")
            mock_encrypt_private_key.assert_called_once_with(private_key, password)
            handle = mock_open_func()
            handle.write.assert_called_once_with(private_pem)

    def test_save_public_key_to_file(self):
        """
        Tests the save_public_key_to_file method of the RsaKeyManager class.

        This test verifies that the method correctly saves the given public key
        to a file at the specified path. It uses mock objects to replace the
        open function and the encrypt_public_key method. It checks that the
        open function is called with the correct arguments and that the
        encrypt_public_key method is called with the correct public key.

        Scenarios tested:
        1. A valid public key is correctly saved to a file with the specified path.

        :return: None
        """

        mock_open_func = mock_open()
        with patch("builtins.open", mock_open_func), patch.object(
            self.km, "encrypt_public_key"
        ) as mock_encrypt_public_key:
            public_key = MagicMock()
            public_pem = MagicMock()
            mock_encrypt_public_key.return_value = public_pem

            self.km.save_public_key_to_file(public_key, "file_path.pem")

            mock_open_func.assert_called_once_with("file_path.pem", "wb")
            mock_encrypt_public_key.assert_called_once_with(public_key)
            handle = mock_open_func()
            handle.write.assert_called_once_with(public_pem)

    def test_load_private_key_from_file(self):
        """
        Tests the load_private_key_from_file method of the RsaKeyManager class.

        This test verifies that the method correctly loads a private key from a file
        with the given path and password. It checks that the method calls the open
        function and the serialize_private_key method with the correct arguments
        and that it correctly handles exceptions that may occur during the loading
        process.

        Scenarios tested:
        1. A valid private key is correctly loaded from a file with the given path
           and password.
        2. The method raises a FileNotFoundError if the private key file is not found.
        3. The method raises an Exception if the private key file is not in the
           correct format or has an invalid password.

        :return: None
        """

        loaded_private_key = b"loaded_private_key"
        serialized_private_key = MagicMock()
        mock_open_func = mock_open(read_data=loaded_private_key)
        file_path = "file.path"
        password = "password"

        with patch("builtins.open", mock_open_func), patch.object(
            self.km, "serialize_private_key"
        ) as mocked_serialize_private_key:
            mocked_serialize_private_key.return_value = serialized_private_key
            result = self.km.load_private_key_from_file(file_path, password)
            mock_open_func.assert_called_once_with(file_path, "rb")
            mocked_serialize_private_key.assert_called_once_with(
                loaded_private_key, password
            )
            assert result is serialized_private_key

            handle = mock_open_func()

            exception_message = f"Private key file not found: {file_path}"
            handle.read.side_effect = FileNotFoundError(exception_message)
            with pytest.raises(FileNotFoundError, match=exception_message):
                self.km.load_private_key_from_file(file_path, password)

            exception_message = "Something wrong with the key"
            handle.read.side_effect = Exception(exception_message)
            with pytest.raises(
                Exception,
                match=f"Failed to process private key. Please check file format and try again.\n\nAdditional Info:\n {exception_message}",
            ):
                self.km.load_private_key_from_file(file_path, password)

    def test_load_public_key_from_file(self):
        """
        Tests the load_public_key_from_file method of the RsaKeyManager class.

        This test verifies that the method correctly loads a public key from a file
        with the given path. It checks that the method calls the open function and
        the serialize_public_key method with the correct arguments and that it
        correctly handles exceptions that may occur during the loading process.

        Scenarios tested:
        1. A valid public key is correctly loaded from a file with the given path.
        2. The method raises a FileNotFoundError if the public key file is not found.
        3. The method raises an Exception if the public key file is not in the
           correct format or has an invalid password.

        :return: None
        """

        loaded_public_key = b"loaded_public_key"
        serialized_public_key = MagicMock()
        file_path = "file.path"
        mock_open_func = mock_open(read_data=loaded_public_key)

        with patch("builtins.open", mock_open_func), patch.object(
            self.km, "serialize_public_key"
        ) as mocked_serialize_public_key:
            mocked_serialize_public_key.return_value = serialized_public_key
            result = self.km.load_public_key_from_file(file_path)

            mock_open_func.assert_called_once_with(file_path, "rb")
            mocked_serialize_public_key.assert_called_once_with(loaded_public_key)
            assert result is serialized_public_key

            handle = mock_open_func()

            exception_message = f"Public key file not found: {file_path}"
            handle.read.side_effect = FileNotFoundError(exception_message)
            with pytest.raises(FileNotFoundError, match=exception_message):
                self.km.load_public_key_from_file(file_path)

            exception_message = "Key Reading Error"
            handle.read.side_effect = Exception(exception_message)
            with pytest.raises(
                Exception,
                match=f"Failed to process public key. Please check file format and try again.\n\nAdditional Info:\n {exception_message}",
            ):
                self.km.load_public_key_from_file(file_path)

    def test_serialize_public_key(self):
        """
        Tests the serialize_public_key method of the RsaKeyManager class.

        This test verifies that the method correctly serializes the given public
        key into PEM format. It uses mock objects to replace the
        load_pem_public_key function and checks that the method calls the
        function with the correct arguments and that the method returns the
        serialized public key.

        Scenarios tested:
        1. A valid public key is correctly serialized into PEM format.
        2. The method raises an exception if the serialization fails.

        :return: None
        """

        with patch(
            "cryptography.hazmat.primitives.serialization.load_pem_public_key"
        ) as mock_load_pem_public_key:
            public_key = MagicMock()
            serialized_public_key = MagicMock()
            mock_load_pem_public_key.return_value = serialized_public_key

            result = self.km.serialize_public_key(public_key)
            mock_load_pem_public_key.assert_called_once()
            assert result is serialized_public_key

            exception_message = "Serialization Error"
            mock_load_pem_public_key.side_effect = Exception(exception_message)
            with pytest.raises(
                Exception,
                match=f"Failed to serialize public key, most likely key was corrupted, or you made a mistake, when provided the key.\nPlease check your input, and try again.\n\nAdditional Info:\n {exception_message}",
            ):
                self.km.serialize_public_key(public_key)

    def test_serialize_private_key(self):
        """
        Tests the serialize_private_key method of the RsaKeyManager class.

        This test verifies that the method correctly serializes the given private
        key into PEM format. It uses mock objects to replace the
        load_pem_private_key function and checks that the method calls the
        function with the correct arguments and that the method returns the
        serialized private key.

        Scenarios tested:
        1. A valid private key is correctly serialized into PEM format.

        :return: None
        """

        with patch(
            "cryptography.hazmat.primitives.serialization.load_pem_private_key"
        ) as mock_load_pem_private_key:
            private_key = MagicMock()
            serialized_private_key = MagicMock()
            mock_load_pem_private_key.return_value = serialized_private_key
            password = "my_password"

            result = self.km.serialize_private_key(private_key, password)
            mock_load_pem_private_key.assert_called_once_with(
                private_key,
                password=password.encode("utf-8"),
                backend=default_backend(),
            )
            assert result is serialized_private_key

    def test_export_keys_to_zip(self):
        """
        Tests the export_keys_to_zip method of the RsaKeyManager class.

        This test verifies that the method correctly exports the given private and
        public key data to a ZIP file at the given path.

        Scenarios tested:
        1. The ZIP file is correctly created and contains the private and public
           key data.

        :return: None
        """

        private_key_data = b"PRIVATE KEY DATA"

        public_key_data = b"PUBLIC KEY DATA"

        with tempfile.TemporaryDirectory() as temp_dir:
            zip_filename = os.path.join(temp_dir, "keys.zip")

            self.km.export_keys_to_zip(private_key_data, public_key_data, zip_filename)

            assert os.path.exists(zip_filename)

            with zipfile.ZipFile(zip_filename, "r") as archive:
                expected_files = ["private_key.pem", "public_key.pem"]
                assert set(archive.namelist()) == set(expected_files)

                assert archive.read("private_key.pem") == private_key_data
                assert archive.read("public_key.pem") == public_key_data
