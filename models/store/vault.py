from models.generators import generate_login_hash, AESCipher
"""module: models/platforms
will generate user platforms and their crypted passwords
"""
import json


class Vault:
    """generate user's password only from file"""
    # user_id = ''
    # __platforms = {}
    # file = ''

    def __init__(self, user_id, master_pass):
        """initializing a users platform using his user id"""
        self.user_id = user_id
        self.__platforms = {}  # Format: {'platform_name': 'encrypted_password'}
        self.file = f'{user_id}.json'
        self.aes = AESCipher(master_pass)

    def add_platform(self, platform_name, password):
        """Add a platform and password for the user."""
        hashed_password = self.aes.encrypt(password)
        self.__platforms[platform_name] = hashed_password

    def load_vault(self):
        try:
            with open(self.file, 'r', encoding='utf-8') as file:
                self.__platforms = json.load(file)
        except Exception:
            pass
    
    def get_vault(self):
        """get users platforms in dictionary"""
        return self.__platforms

    def decrypt(self):
        """decrypt platforms and send back a decrypted"""
        decrypted = {}
        for platform, password in self.__platforms:
            decrypted[platform] = self.aes.decrypt(password)

        return decrypted

    def save_platform(self):
        """saves the encryped platforms"""
        save_dict = self.__platforms.copy()
        try:
            with open(self.file, 'w', encoding='utf-8') as file:
                json.dump(save_dict, file)
        except Exception:
            pass

    def delete_platform(self, platform_name):
        """deletes a users platform"""
        del self.__platforms[platform_name]
        

    # def verify_access(self, platform_name, password):
    #     """Verify if the user has access to the given platform."""
    #     if platform_name in self.platforms:
    #         hashed_password = generate_login_hash(password)
    #         return self.platforms[platform_name] == hashed_password
    #     return False
