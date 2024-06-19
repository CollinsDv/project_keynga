"""module: filestore
will use the file to store object instances
"""
import os
import json
from models.user import User

class_models = {'User': User}


class FileUnit:
    """Instanciate a file storage unit"""
    store = 'store.json'
    __users = {}

    def add(self, object):
        """will add a new object to the store"""
        key = object.name + ':' + object.user_id
        self.__users[key] = object

    def save(self):
        store_dict = {}
        try:
            with open(self.store, 'w', encoding='utf-8') as file:
                for key, obj in self.__users.items():
                    store_dict[key] = obj.object_dict()
                json.dump(store_dict, file)
        except Exception as e:
            print(e)

    def load(self):
        try:
            loaded_dict = {}
            with open(self.__users, 'r', encoding='utf-8') as file:
                loaded_dict = json.load(file)
            
            for key, object in loaded_dict.items():
                loaded_dict[key] = class_models[object.__class__](**object)
            
            self.__users = loaded_dict
        except Exception as e:
            # print(e)
            pass    