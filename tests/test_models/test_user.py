import unittest
from models.user import User
from models.generators import generate_login_hash
from models.store.vault import Vault
import datetime
import bcrypt
import base64
import hashlib

class TestUser(unittest.TestCase):
    """test user mode"""
    def setUp(self) -> None:
        self.deets1 = {'name':'Collins', 'master_pass':'password1', 'user_id':'32545-53535-53535'}
        self.deets2 = {'name':'Kush', 'master_pass':'password2'}
        self.User1 = User(**self.deets1)
        self.User2 = User(**self.deets2)

    def test_object_types(self):
        """used to test the users types"""
        self.assertIsInstance(self.User1, User)
        self.assertIsInstance(self.User2, User)
        self.assertIsNot(self.User1, self.User2)

    def test_user1_details(self):
        """observing user1 details"""

        self.assertEqual(self.User1.name, 'Collins')
        self.assertEqual(type(self.User1.user_id), str)
        self.assertIsInstance(self.User1.date_joined, datetime.datetime)
        self.assertIsInstance(self.User1.date_updated, datetime.datetime)
        # testing hash
        passwd = base64.b64encode(hashlib.sha256('password1'.encode('utf-8')).digest())
        self.assertTrue(bcrypt.checkpw(passwd, generate_login_hash('password1')))

    def test_user2_details(self):
        """observing user1 details"""
        self.assertEqual(self.User2.name, 'Kush')
        self.assertEqual(type(self.User1.user_id), str)
        self.assertIsInstance(self.User1.date_joined, datetime.datetime)
        self.assertIsInstance(self.User1.date_updated, datetime.datetime)
        # testing hash
        passwd = base64.b64encode(hashlib.sha256('password2'.encode('utf-8')).digest())
        self.assertTrue(bcrypt.checkpw(passwd, generate_login_hash('password2')))

    def test_null(self):
        """testing null input"""
        null_user = User()
        self.assertEqual(null_user.name, '--NO NAME--')
        self.assertIsInstance(null_user, User)
        self.assertIsInstance(null_user.date_joined, datetime.datetime)
        self.assertIsInstance(null_user.date_updated, datetime.datetime)


    def test_user_password_hash(self):
        """Test if the password hash matches the expected hash"""
        # user1
        raw_password = self.deets1['master_pass'].encode('utf-8')
        sha_pw = hashlib.sha256(raw_password).digest()
        encoded = base64.b64encode(sha_pw)
        self.assertTrue(bcrypt.checkpw(encoded, generate_login_hash(self.deets1['master_pass'])))
        # user2
        raw_password = self.deets2['master_pass'].encode('utf-8')
        sha_pw = hashlib.sha256(raw_password).digest()
        encoded = base64.b64encode(sha_pw)
        self.assertTrue(bcrypt.checkpw(encoded, generate_login_hash(self.deets2['master_pass'])))

    def test_invalid_password(self):
        """Test with an invalid password"""
        self.assertFalse(bcrypt.checkpw(b"wrongpassword", generate_login_hash(self.deets1['master_pass'])))

    def test_vault_exists(self):
        """checking vault existence"""
        self.assertIn('vault', self.User1.__dict__)
        self.assertIsInstance(self.User1.vault, Vault)
