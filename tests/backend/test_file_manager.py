from unittest.mock import MagicMock, mock_open, patch
from backend.chunk_encrypter import ChunkEncrypter
from backend.file_manager import FileManager
from backend.constants.constants import Size
import pytest


class TestFileManager:

    @pytest.fixture(scope="function", autouse=True)
    def autorun(self):
        """
        Fixture to set up and tear down the FileManager test environment.

        This fixture is automatically used for each test function in the
        TestFileManager class. It initializes the FileManager instance.

        After the test, it ensures the FileManager instance is properly closed and cleaned up.

        :param self: The test class instance.
        :yield: The FileManager instance.
        """
        self.fm = FileManager()
        yield

    def test_stop_process_request(self):
        """
        Tests that the stop_process_request method sets the internal flag.

        :return: None
        """
        self.fm.stop_process_request()
        assert self.fm._stop_flag

    def test_encrypt_file(self):
        """
        Tests that the encrypt_file method correctly initializes a ChunkEncrypter
        instance and calls the _process_file method with the correct arguments.

        :return: None
        """
        with patch(
            "backend.file_manager.ChunkEncrypter",
            autospec=True,
            return_value=MagicMock(ChunkEncrypter),
        ) as MockChunkEncrypter, patch.object(self.fm, "_process_file"):
            chunk_encrypter = MockChunkEncrypter.return_value
            self.fm.encrypt_file("input.file", "output.file", "public.key")

            MockChunkEncrypter.assert_called_once_with(public_key="public.key")
            self.fm._process_file.assert_called_once_with(
                "input.file",
                "output.file",
                chunk_encrypter.encrypt_chunk,
                Size.ENCRYPTION_CHUNK,
            )

    def test_decrypt_file(self):
        """
        Tests that the decrypt_file method correctly initializes a ChunkEncrypter
        instance and calls the _process_file method with the correct arguments.

        :return: None
        """

        with patch(
            "backend.file_manager.ChunkEncrypter",
            autospec=True,
            return_value=MagicMock(ChunkEncrypter),
        ) as MockChunkEncrypter, patch.object(self.fm, "_process_file"):
            chunk_encrypter = MockChunkEncrypter.return_value

            self.fm.decrypt_file("input.file", "output.file", "private.key")

            MockChunkEncrypter.assert_called_once_with(private_key="private.key")
            self.fm._process_file.assert_called_once_with(
                "input.file",
                "output.file",
                chunk_encrypter.decrypt_chunk,
                Size.DECRYPTION_CHUNK,
            )

    def test__process_file(self):
        """
        Tests the _process_file method to ensure that it correctly reads a file in
        chunks, processes each chunk using the provided chunk_handler, and writes the
        processed chunk to the specified output file. The size of the chunks is determined
        by the chunk_size argument.

        The test verifies that the method correctly calls the chunk_handler for each
        chunk, writes the processed chunks to the output file, and updates the
        processed_bytes signal and the chunk_counter_flag attribute.

        The test also verifies that the method correctly handles exceptions, logging
        the error and emitting the critical_error signal with the input file path and
        the error message.

        :return: None
        """
        mock_input_data = b"Chunk1Chunk2Chunk3"

        mock_open_func = mock_open(read_data=mock_input_data)
        chunk_handler = MagicMock(side_effect=lambda chunk: chunk.upper())

        with patch("builtins.open", mock_open_func), patch(
            "backend.file_manager.signal_manager", autospec=True
        ) as mock_signal_manager:

            self.fm._process_file("input.file", "output.file", chunk_handler, 6)

            mock_open_func.assert_any_call("input.file", "rb")
            mock_open_func.assert_any_call("output.file", "wb")

            chunk_handler.assert_any_call(b"Chunk1")
            chunk_handler.assert_any_call(b"Chunk2")
            chunk_handler.assert_any_call(b"Chunk3")

            handle = mock_open_func()
            handle.write.assert_any_call(b"Chunk1".upper())
            handle.write.assert_any_call(b"Chunk2".upper())
            handle.write.assert_any_call(b"Chunk3".upper())

            assert self.fm.chunk_counter_flag == 3
            assert mock_signal_manager.update_processed_bytes.emit.call_count == 3
            mock_signal_manager.operation_completed.emit.assert_called_once()

            exception_message = "Error processing file"
            handle.write.side_effect = Exception(exception_message)
            self.fm._process_file("input.file", "output.file", chunk_handler, 6)
            mock_signal_manager.critical_error.emit.assert_called_once_with(
                "input.file", exception_message
            )
