from typing import Callable
from chunk_encrypter import ChunkEncrypter
from rsa_key_manager import RsaKeyManager
from constants import Size
import logging

logging.basicConfig(level=logging.INFO)

class FileManager:
    def __init__(self):       
        """
        Initializes FileManager with a ChunkEncrypter instance for encryption and decryption operations.

        :return: FileManager instance
        """
        self.chunk_encrypter = ChunkEncrypter(RsaKeyManager())
    
    def encrypt_file(self, input_file_path: str, output_file_path: str):
        """
        Encrypts a given file using the ChunkEncrypter instance, writing the encrypted bytes to another file.

        :param input_file_path: The path to the file to be encrypted
        :param output_file_path: The path to the file where the encrypted bytes will be written
        """
        self._process_file(input_file_path, output_file_path, self.chunk_encrypter.encrypt_chunk, Size.ENCRYPTION_CHUNK)

    def decrypt_file(self, input_file_path: str, output_file_path: str):
        """
        Decrypts a given file using the ChunkEncrypter instance, writing the decrypted bytes to another file.

        :param input_file_path: The path to the file to be decrypted
        :param output_file_path: The path to the file where the decrypted bytes will be written
        """
        
        self._process_file(input_file_path, output_file_path, self.chunk_encrypter.decrypt_chunk, Size.DECRYPTION_CHUNK)
    
    
    def _process_file(self, input_file_path: str, output_file_path:str, chunk_handler: Callable[[bytes], bytes], chunk_size: int):
        """
        Reads a given file chunk by chunk, processes each chunk using a given callable, and writes the processed chunks to another file.

        :param input_file_path: The path to the file to be read
        :param output_file_path: The path to the file where the processed chunks will be written
        :param chunk_handler: The callable to be used to process the chunks
        :param chunk_size: The size of the chunks to be read and processed
        """
        try:
            with open(input_file_path, 'rb') as infile, open(output_file_path, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunk_size)
                    if not chunk:  # If end of file
                        break  

                    processed_chunk = chunk_handler(chunk)
                    outfile.write(processed_chunk)
        except Exception as e:
            logging.error(f"Error processing file {input_file_path}: {e}")
    