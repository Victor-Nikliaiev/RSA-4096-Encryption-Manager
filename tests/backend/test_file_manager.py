import re
from unittest.mock import MagicMock, Mock, call, mock_open, patch
import pytest
import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtUiTools as qtu
from backend import signal_manager
from backend.chunk_encrypter import ChunkEncrypter
from backend.constants.constants import Size
from backend.file_manager import FileManager
from tools.toolkit import Tools as t


class TestFileManager:

    @pytest.fixture(scope="function", autouse=True)
    def autorun(self):
        self.fm = FileManager()
        yield

    def test_stop_process_request(self):
        self.fm.stop_process_request()
        assert self.fm._stop_flag

    def test_encrypt_file(self):
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
