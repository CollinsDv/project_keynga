from models import user_store
import unittest
from models.user import User
import os
import json

class TestStore(unittest.TestCase):
    """Test user storage"""
    def setUp(self) -> None:
        self.user1_dict = {'name':'Collins', 'master_pass':'35262@325'}
        self.user2_dict = {'name':'Kush', 'master_pass':'2424#$454'}
        self.user1 = User(**self.user1_dict)
        self.user2 = User(**self.user2_dict)

    def tearDown(self) -> None:
        if os.path.exists(user_store.file_store):
            os.remove(user_store.file_store)
        user_store.clear()

    def test_add(self):
        """Add a user to storage"""
        self.user1.add()
        self.user2.add()
        key1 = self.user1.name + ':' + self.user1.user_id
        key2 = self.user2.name + ':' + self.user2.user_id
        self.assertTrue(user_store.user_exists(key1))
        self.assertTrue(user_store.user_exists(key2))
        self.assertEqual(2, user_store.get_user_count())
        print('test_add successful')

    def test_user_details(self):
        """Tests membership"""
        self.user1.add()
        key_contents = ['name', 'master_pass', 'date_joined', 'date_updated', 'hash_pw']
        for elem in key_contents:
            self.assertIn(elem, self.user1.obj_dict())
        print('test_user_details successful')
    
    def test_save(self):
        """Testing save method"""
        self.user1.add()
        self.user2.add()
        users = user_store.get()
        print(users)
        user_store.save()
        self.assertTrue(os.path.exists(user_store.file_store))
        print('path exists')
        users_dict = {}
        try:
            with open(user_store.file_store, 'r', encoding='utf-8') as file:
                obj_dict = json.load(file)
                for key, obj in obj_dict.items():
                    users_dict[key] = User(**obj)
        except Exception as e:
            raise e

        user1_key = self.user1.name + ':' + self.user1.user_id
        user2_key = self.user2.name + ':' + self.user2.user_id

        self.assertIsInstance(users_dict[user1_key], User)
        self.assertIsInstance(users_dict[user2_key], User)
        print('test_save successful')

    def test_load_and_get(self):
        """Testing load and get in store"""
        self.user1.add()
        self.user2.add()
        user_store.save()
        user_store.load()

        users = user_store.get()
        self.assertIsInstance(users, dict)
        self.assertEqual(2, user_store.get_user_count())

        user1_key = self.user1.name + ':' + self.user1.user_id
        user2_key = self.user2.name + ':' + self.user2.user_id
        self.assertTrue(user_store.user_exists(user1_key))
        self.assertTrue(user_store.user_exists(user2_key))

        self.assertIsInstance(self.user1, User)
        self.assertIsInstance(self.user2, User)

        new_user1_dict = self.user1.obj_dict()
        del new_user1_dict['__class__']
        new_user1_dict['master_pass'] = self.user1_dict['master_pass']
        new_user1_dict.pop('hash_pw')  # Remove the hash_pw for comparison

        self.assertIsNot(self.user1, User(**new_user1_dict))
        self.assertDictEqual({k: v for k, v in self.user1.obj_dict().items() if k != 'hash_pw'},
                             {k: v for k, v in User(**new_user1_dict).obj_dict().items() if k != 'hash_pw'},
                             "user1_dict should be equal to a new User object created from it.")

        new_user2_dict = self.user2.obj_dict()
        del new_user2_dict['__class__']
        new_user2_dict['master_pass'] = self.user2_dict['master_pass']
        new_user2_dict.pop('hash_pw')  # Remove the hash_pw for comparison

        self.assertIsNot(self.user2, User(**new_user2_dict))
        self.assertDictEqual({k: v for k, v in self.user2.obj_dict().items() if k != 'hash_pw'},
                             {k: v for k, v in User(**new_user2_dict).obj_dict().items() if k != 'hash_pw'},
                             "user2_dict should be equal to a new User object created from it.")
        print('test_load_and_get successful')

    def test_file_not_exist(self):
        """Used to test non-existence of file on creation"""
        self.assertFalse(os.path.exists(user_store.file_store))
        print('test_file_not_exist successful')

if __name__ == '__main__':
    unittest.main()
