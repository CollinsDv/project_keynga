import unittest
import os
import json
from models.store.vault import Vault
import bcrypt

class TestVault(unittest.TestCase):

    def setUp(self):
        self.user_id = 'test_user'
        self.master_pass = 'test_pass'
        self.salt = str(bcrypt.gensalt())
        self.vault = Vault(self.user_id, self.master_pass, self.salt)
        self.platform_name = 'test_platform'
        self.password = 'test_password'

    def tearDown(self):
        # Remove the test file if it exists
        if os.path.exists(f'{self.user_id}.json'):
            os.remove(f'{self.user_id}.json')

    def test_initialization(self):
        self.assertEqual(self.vault.user_id, self.user_id)
        self.assertEqual(self.vault.aes.key, Vault(self.user_id, self.master_pass, self.salt).aes.key)
        self.assertEqual(self.vault.get_vault(), {})

    def test_add_platform(self):
        self.vault.add_platform(self.platform_name, self.password)
        encrypted_password = self.vault.get_vault().get(self.platform_name)
        self.assertIsNotNone(encrypted_password)
        self.assertNotEqual(encrypted_password, self.password)

    def test_generate_password(self):
        """testing password_generator"""
        self.vault.generate_password(self.platform_name)
        self.vault.save_platforms()

        with open(self.vault.file, 'r') as file:
            platforms = json.load(file)

        self.assertTrue(len(self.vault.aes.decrypt(platforms[self.platform_name])) == 10)

    def test_load_vault(self):
        self.vault.add_platform(self.platform_name, self.password)
        self.vault.save_platforms()
        new_vault = Vault(self.user_id, self.master_pass, self.salt)
        new_vault.load_vault()
        self.assertEqual(new_vault.get_vault(), self.vault.get_vault())

    def test_get_vault(self):
        self.vault.add_platform(self.platform_name, self.password)
        vault_contents = self.vault.get_vault()
        self.assertIn(self.platform_name, vault_contents)

    def test_decrypt(self):
        self.vault.add_platform(self.platform_name, self.password)
        decrypted_vault = self.vault.decrypt()
        self.assertEqual(decrypted_vault.get(self.platform_name), self.password)

    def test_save_platforms(self):
        self.vault.add_platform(self.platform_name, self.password)
        self.vault.save_platforms()
        self.assertTrue(os.path.exists(f'{self.user_id}.json'))
        with open(f'{self.user_id}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        self.assertIn(self.platform_name, data)

    def test_delete_platform(self):
        self.vault.add_platform(self.platform_name, self.password)
        self.vault.delete_platform(self.platform_name)
        self.assertNotIn(self.platform_name, self.vault.get_vault())

if __name__ == '__main__':
    unittest.main()
