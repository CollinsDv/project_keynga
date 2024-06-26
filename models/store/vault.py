from models.generators import generate_login_hash, AESCipher, password_generator
"""module: models/platforms
will generate user platforms and their crypted passwords
"""
import json


class Vault:
    """generate user's password only from file"""
    # user_id = ''
    # __platforms = {}
    # file = ''

    def __init__(self, user_id, master_pass, salt):
        """initializing a users platform using his user id"""
        self.user_id = user_id
        self.__platforms = {}  # Format: {'platform_name': 'encrypted_password'}
        self.file = f'{user_id}.json'
        self.aes = AESCipher(master_pass, salt)

    def add_platform(self, platform_name, password):
        """Add a platform and password for the user."""
        hashed_password = self.aes.encrypt(password)
        self.__platforms[platform_name] = hashed_password

    def generate_password(self, platform):
        """used to generate a strong 10 char password for a platform"""
        self.__platforms[platform] = self.aes.encrypt(password_generator())

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

    def delete_platform(self, platform_name):
        """deletes a users platform"""
        self.__platforms = {}

    def delete_all_platforms(self):
        """deletes all platforms"""
        self.__platforms = {}
    
    def number_of_platforms(self):
        """gets the number of platforms managed"""
        return len(self.__platforms)
    
    def get_platforms(self):
        """returns the list of platforms"""
        return self.__platforms

    # def verify_access(self, platform_name, password):
    #     """Verify if the user has access to the given platform."""
    #     if platform_name in self.platforms:
    #         hashed_password = generate_login_hash(password)
    #         return self.platforms[platform_name] == hashed_password
    #     return False
