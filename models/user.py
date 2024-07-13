"""module: user
Used to initiate a user and his profile details
"""
import datetime
import uuid
from models.generators import generate_login_hash, password_generator
from models import user_store
from models.store.vault import Vault
import bcrypt

d_time = "%m/%d/%y %H:%M:%S"


class User:
    """generate a user"""
    def __init__(self, *args, **kwargs):
        """initialization of the user object
        Args:
            args (tuple): single indexed elements
            kwargs (dict): keyword elements

        Return:
            user object
        """
        if kwargs:
            if kwargs.get('__class__'):
                del kwargs['__class__']
            for key, value in kwargs.items():
                setattr(self, key, value)

            if kwargs.get('date_joined') and type(self.date_joined) is str:
                self.date_joined = datetime.datetime.strptime(
                    self.date_joined, d_time)
            else:
                self.date_joined = datetime.datetime.utcnow()

            if kwargs.get('date_updated') and type(self.date_updated) is str:
                self.date_updated = datetime.datetime.strptime(
                    self.date_updated, d_time)
            else:
                self.date_updated = datetime.datetime.utcnow()

            if kwargs.get('master_pass'):
                self.hash_pw = generate_login_hash(kwargs.get('master_pass'))

            if not kwargs.get('user_id'):
                self.user_id = str(uuid.uuid4())

            if not kwargs.get('salt'):
                self.salt = str(bcrypt.gensalt())

            # Initialize the vault only if master_pass is provided
            if kwargs.get('master_pass'):
                self.vault = Vault(
                    self.user_id, kwargs.get('master_pass'), self.salt)
                self.vault.load_vault()
            else:
                self.vault = None

            # delete password after use
            if kwargs.get('master_pass'):
                del kwargs['master_pass']

            if hasattr(self, 'master_pass'):
                del self.master_pass
        else:
            self.name = '--NO NAME--'
            self.user_id = str(uuid.uuid4())
            self.date_joined = datetime.datetime.utcnow()
            self.date_updated = self.date_joined
            self.master_pass = password_generator()
            self.hash_pw = generate_login_hash(self.master_pass)
            self.salt = str(bcrypt.gensalt())
            self.vault = None

    def add(self):
        """adds a user to the file storage"""
        self.date_updated = datetime.datetime.utcnow()
        user_store.add(self)

    def __str__(self):
        """returns a string representation of an object"""
        return f"[{self.name}] : [{self.user_id}] || [{self.obj_dict()}]"

    def obj_dict(self):
        """generates a json representation of a user object"""
        dictionary = self.__dict__.copy()
        dictionary['date_joined'] = self.date_joined.strftime(d_time)
        dictionary['date_updated'] = self.date_updated.strftime(
            d_time)
        dictionary['hash_pw'] = dictionary['hash_pw'].decode() \
            if dictionary['hash_pw'] else None
        dictionary['__class__'] = self.__class__.__name__
        if dictionary.get('vault'):
            del dictionary['vault']
        return dictionary

    # Methods required by Flask-Login
    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)
