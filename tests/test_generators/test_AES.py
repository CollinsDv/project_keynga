import unittest
from models.generators.AES_cipher import AESCipher

class TestAESCipher(unittest.TestCase):
    def setUp(self):
        # Initialize AESCipher with a test key
        self.key = "test_key"
        self.cipher = AESCipher(self.key)

    def test_encrypt_decrypt(self):
        # Test that encryption and decryption work as expected
        plain_text = "This is a test."
        encrypted_text = self.cipher.encrypt(plain_text)
        decrypted_text = self.cipher.decrypt(encrypted_text)
        
        self.assertEqual(plain_text, decrypted_text, "Decrypted text should match the original")

    def test_encrypt_output_type(self):
        # Test that the output of encrypt is a string
        plain_text = "Another test."
        encrypted_text = self.cipher.encrypt(plain_text)
        
        self.assertIsInstance(encrypted_text, str, "Encrypted text should be a string")

    def test_decrypt_output_type(self):
        # Test that the output of decrypt is a string
        plain_text = "Yet another test."
        encrypted_text = self.cipher.encrypt(plain_text)
        decrypted_text = self.cipher.decrypt(encrypted_text)
        
        self.assertIsInstance(decrypted_text, str, "Decrypted text should be a string")

if __name__ == '__main__':
    unittest.main()