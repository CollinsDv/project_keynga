from models import user_store
from models.user import User
from models.generators import AESCipher, generate_login_hash, password_generator
from models.store.vault import Vault
import unittest
import os
import json


class TesTCompleteSystem(unittest.TestCase):
    """overall integration testing"""
    def setUp(self) -> None:
        self.user1_dict = {'name': 'Collins', 'master_pass': 'password'}
        self.user1 = User(**self.user1_dict)
        self.user2_dict = {'name': 'Henry', 'master_pass': '12345678'}
        self.user2 = User(**self.user2_dict)

    def tearDown(self) -> None:
        files = [self.user1.vault.file, self.user2.vault.file]
        for file in files:
            if os.path.exists(file):
                os.remove(file)
        
        # delete each users platforms
        self.user1.vault.delete_all_platforms()
        self.user2.vault.delete_all_platforms()

    def test_vault_existence(self):
        """testing a user's vault"""
        self.assertIsInstance(self.user1.vault, Vault)
        self.assertIsInstance(self.user2.vault, Vault)
        
    def test_vault_attributes(self):
        """testing vault instance attributes"""
        attribute = ['user_id', '_Vault__platforms', 'file', 'aes'] 
        for att in attribute:
            self.assertIn(att, self.user1.vault.__dict__)
            self.assertIn(att, self.user2.vault.__dict__)

    def test_add_save_platform(self):
        user_platforms = [('Gmail', 'collins', 'google1'), ('Netflix', 'collins', '324-342')]
        for platform in user_platforms:
            self.user1.vault.add_platform(platform[0], platform[1], platform[2])

        self.assertTrue(self.user1.vault.number_of_platforms() == 2)
        self.user1.vault.save_platforms()
        self.assertTrue(os.path.exists(self.user1.vault.file))

        with open(self.user1.vault.file, 'r') as file:
             new_user1_dict = json.load(file)
        
        self.assertDictEqual(new_user1_dict, self.user1.vault.get_platforms())
        for platform in ['Gmail-collins', 'Netflix-collins']:
            self.assertIn(platform, self.user1.vault.get_platforms())

if __name__ == '__main__':
    unittest.main()