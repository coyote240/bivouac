import sys
from user import User

class Model (object):

    def __init__(self, session=None):

        self.session = session
        self.user = None

    @property
    def User(self):

        if(self.user is None):
            uid = self.session.uid
            self.user = User.get_user(uid)

        return self.user
