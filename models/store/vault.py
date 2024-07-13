"""module: models/platforms
will generate user platforms and their crypted passwords
"""
from models.generators import AESCipher, password_generator
import json


class Vault:
    """generate user's password only from file"""
    def __init__(self, user_id, master_pass, salt):
        """initializing a users platform using his user id"""
        self.user_id = user_id
        self.__platforms = {}  # Format:{'platform_name': 'encrypted_password'}
        self.file = f'{user_id}.json'
        self.aes = AESCipher(master_pass, salt)

    def add_platform(self, platform_name, username, password):
        """Add a platform and password for the user."""
        hashed_password = self.aes.encrypt(password)
        key = platform_name + '-' + username
        if self.__platforms.get(key, None):
            del self.__platforms[key]
        self.__platforms[key] = hashed_password

    def generate_password(self, platform_name, username):
        """used to generate a strong 10 char password for a platform"""
        key = platform_name + '-' + username
        self.__platforms[key] = self.aes.encrypt(password_generator())

    def load_vault(self):
        """load a user's vault"""
        try:
            with open(self.file, 'r', encoding='utf-8') as file:
                self.__platforms = json.load(file)
        except Exception:
            pass  # vault doesn't exist

    def get_vault(self):
        """get users platforms in dictionary"""
        return self.__platforms

    def decrypt(self):
        """decrypt platforms and send back a decrypted"""
        decrypted = {}
        for platform, password in self.__platforms.items():
            decrypted[platform] = self.aes.decrypt(password)

        return decrypted

    def save_platforms(self):
        """saves the encryped platforms"""
        save_dict = self.__platforms.copy()
        try:
            with open(self.file, 'w', encoding='utf-8') as file:
                json.dump(save_dict, file)
        except Exception:
            pass

    def delete_platform(self, platform_name, username):
        """Delete a user's platform"""
        key = platform_name + '-' + username
        if key in self.__platforms:
            del self.__platforms[key]

    def delete_all_platforms(self):
        """deletes all platforms"""
        self.__platforms = {}

    def number_of_platforms(self):
        """gets the number of platforms managed"""
        return len(self.__platforms)

    def get_platforms(self):
        """returns the list of platforms"""
        return self.__platforms
