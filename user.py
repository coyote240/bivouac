import hashlib
from pymongo import Connection
from bson import ObjectId

class User (dict):

    '''User Object'''

    
    @staticmethod
    def _get_user_collection():

        if not hasattr(User, '_collection'):

            connection = Connection('localhost', 27017)
            db = connection.projectlist
            User._collection = db.users

        return User._collection


    @staticmethod
    def get_active_users():

        users = User._get_user_collection()
        result = users.find(as_class=User)
        return result


    @staticmethod
    def get_user(id):
        
        '''Return a single User object from the database.
        If 'id' is not a valid ObjectId, throws an InvalidId exception
        If 'id' is not present in the database, say from a deleted User record,
        returns a None type.
        '''

        users = User._get_user_collection()
        user = users.find_one({'_id': ObjectId(id)}, as_class=User)
        return user


    @staticmethod
    def get_login_user(user_name, password):

        pwdhash = hashlib.md5(password).hexdigest()

        users = User._get_user_collection()
        user = users.find_one({'login': user_name, '_password': pwdhash}, as_class=User)
        return user

    
    def __init__(self, id=None):
        
        dict.__init__(self)
        self._password = None


    def __getitem__(self, key):
        if not hasattr(self, key):
            raise KeyError(key)
        else:
            return getattr(self, key)


    def __setitem__(self, key, value):
        setattr(self, key, value)


    @property
    def id(self):
        return str(self._id)


    @id.setter
    def id(self, strid):
        self._id = ObjectId(strid)
    

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = hashlib.md5(value).hexdigest()

    @password.deleter
    def password(self):
        del self._password

        
    def store(self):
        
        _id = User._get_user_collection().save(self.__dict__)
        return _id


    def delete(self):
        pass
