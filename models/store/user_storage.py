"""module: models/store/user_store
will use the file to store user instances
"""
import json
import os


class UserStore(object):
    """Instantiate a file storage unit"""
    file_store = 'users.json'
    __users = {}

    def add(self, user):
        """Add a new user to the store"""
        key = user.name + ':' + user.user_id
        self.__users[key] = user

    def user_exists(self, key):
        """Check if a user exists in the store."""
        return key in self.__users

    def get_user_count(self):
        """Returns the number of users in the store."""
        return len(self.__users)

    def get_users(self):
        """Used to get the list of objects"""
        return self.__users

    def save(self):
        store_dict = {}
        try:
            with open(self.file_store, 'w', encoding='utf-8') as file:
                for key, obj in self.__users.items():
                    store_dict[key] = obj.obj_dict()
                json.dump(store_dict, file)
        except Exception as e:
            print(f"Error saving users: {e}")

    def load(self):
        from models.user import User
        try:
            if os.path.exists(self.file_store) and\
                    os.path.getsize(self.file_store) > 0:
                # file is not not empty
                with open(self.file_store, 'r', encoding='utf-8') as file:
                    loaded_dict = json.load(file)
                    for key, obj in loaded_dict.items():
                        obj['hash_pw'] = obj['hash_pw'].encode() \
                            if obj['hash_pw'] else None
                        self.__users[key] = User(**obj)
            else:
                print("users.json is empty or does not exist. Skipping load.")
        except Exception as e:
            print(f"Error loading users: {e}")

    def clear(self):
        """Clear the store"""
        self.__users = {}
        if os.path.exists(self.file_store):
            os.remove(self.file_store)
