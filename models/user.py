import datetime
import uuid
from models.generators import generate_login_hash, AESCipher
from models import store
from models.store import Vault

"""module: user
Used to initiate a user and his profile details
"""
d_time = "%m/%d/%y %H:%M:%S"


class User:
    """generate a user"""
    def __init__(self, *args, **kwargs):
        """initialization of the user object
        Args:
            args (tuple): sigle indexed elements
            kwargs (dict): keyword elements

        Return:
            user object
        """
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

            if kwargs.get('date_joined') and type(self.date_joined) is str:
                self.date_joined = datetime.strptime(self.date_joined, d_time)
            else:
                self.date_joined = datetime.datetime.utcnow()

            if kwargs.get('date_updated') and type(self.date_updated) is str:
                self.date_updated = datetime.strptime(
                    self.date_updated, d_time)
            else:
                self.date_updated = datetime.datetime.utcnow()

            if kwargs.get('master_pass'):
                self.hash_pw = generate_login_hash(kwargs.get('master_pass'))

            if not kwargs.get['user_id']:
                self.user_id = str(uuid.uuid4())
            # activate personal vault
            self.vault = Vault(self.user_id, kwargs.get('master_pass'))
            self.vault.load_vault()
        else:
            self.name = '--NO NAME--'
            self.user_id = str(uuid.uuid4())
            self.date_joined = datetime.datetime.utcnow()
            self.date_updated = self.date_joined
            import random
            self.hash_pw = generate_login_hash(str(random.randint(0, 10)))
            self.vault = Vault(self.user_id)
            self.vault.load_vault()

    def add(self):
        self.date_updated = datetime.datetime.utcnow()
        store.add(self)

    def __str__(self):
        return f"[{self.name}] : [{self.user_id}] || [{self.obj_dict()}]"

    def obj_dict(self):
        dictionary = self.__dict__.copy()
        dictionary['date_joined'] = self.date_joined.strftime(d_time)
        dictionary['date_updated'] = self.date_updated.strftime(d_time)
        dictionary['__class__'] = self.__class__.__name__
        del dictionary['vault']
        return dictionary
