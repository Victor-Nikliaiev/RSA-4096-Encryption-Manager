from file_manager import FileManager
from rsa_key_manager import RsaKeyManager
from constants import Path




def main():
    pass
    ### Generate keys ###
    # key_manager = RsaKeyManager()
    # private_key = key_manager.generate_private_key()
    # public_key = key_manager.generate_public_key(private_key)

    # key_manager.save_private_key_to_file(private_key, Path.PRIVATE_KEY_FILE)
    # key_manager.save_public_key_to_file(public_key, Path.PUBLIC_KEY_FILE)

    # file_manager = FileManager()

    ### Picture ###
    # file_manager.encrypt_file('picture.png', 'encrypted_picture.bin')    
    # file_manager.decrypt_file('encrypted_picture.bin', 'decrypted_picture.png')

    ### Text ###
    # file_manager.encrypt_file('message.txt', 'encrypted_message.bin')
    # file_manager.decrypt_file('encrypted_message.bin', 'decrypted_message.txt')

    ### Zip Archive ###
    # file_manager.encrypt_file('saved_keys.zip', 'encrypted_saved_keys.bin')
    # file_manager.decrypt_file('encrypted_saved_keys.bin', 'decrypted_saved_keys.zip')

    ### Video ###
    # file_manager.encrypt_file('video.mp4', 'encrypted_video.bin')
    # file_manager.decrypt_file('encrypted_video.bin', 'decrypted_video.mp4')
 
if __name__ == "__main__":
    main()




