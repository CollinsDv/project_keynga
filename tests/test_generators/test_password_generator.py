import unittest
from models.generators.password_generator import password_generator,string

class TestPasswordGenerator(unittest.TestCase):
    def test_password_length(self):
        """Test that the generated password meets the expected length"""
        password = password_generator()
        self.assertEqual(len(password), 10, "Generated password should be 12 characters long")

    def test_password_complexity(self):
        """Test that the generated password contains a mix of character types"""
        password = password_generator()
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        self.assertTrue(has_upper and has_lower and has_digit and has_special,
                        "Password must contain upper, lower, digits, and special characters")

    def test_password_uniqueness(self):
        """Test that multiple generated passwords are unique"""
        passwords = {password_generator() for _ in range(100)}
        self.assertEqual(len(passwords), 100, "Generated passwords should be unique")

if __name__ == '__main__':
    unittest.main()