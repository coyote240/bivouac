import hashlib
from pymongo import Connection
from bson import ObjectId


class Session(dict):

    
    '''Session class.
    '''

    def __init__(self):
        dict.__init__(self)
        self._uid = None


    @staticmethod
    def _get_session_collection():

        if not hasattr(Session, '_collection'):

            connection = Connection('localhost', 27017)
            db = connection.projectlist
            Session._collection = db.sessions

        return Session._collection


    @staticmethod
    def get_session(id):

        '''Return a single Session object from the database.
        '''

        sessions = Session._get_session_collection()
        session = sessions.find_one({'_id': ObjectId(id)}, as_class=Session)
        return session


    @property
    def id(self):
        return str(self._id)

    
    @property
    def uid(self):
        return self._uid


    @uid.setter
    def uid(self, uid):
        self._uid = uid

    
    def store(self):

        self._id = Session._get_session_collection().save(self.__dict__)
        return self._id


    def delete(self):
        pass


    def __getitem__(self, key):
        if not key in self:
            raise KeyError(key)
        else:
            return getattr(self, key)


    def __setitem__(self, key, value):
        setattr(self, key, value)
