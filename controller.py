import sys
import functools
import datetime
from pprint import pformat
from webob import Request, Response, exc
from user import User
from session import Session

import bivouac

def action(func):

    '''MVC @action decorator as a WSGI application.
    '''

    def replacement(self, environ, start_response):

        req = Request(environ)

        if self.require_auth:
            self.user = self.get_user(req)
            if self.user is None:
                resp = self.redirect('/login')
                return resp(environ, start_response)
            
        try:
            resp = func(self, req, **req.urlvars)   # original function called here
        except exc.HTTPException, e:
            resp = e

        if isinstance(resp, basestring):
            resp = Response(body=resp)
            
        return resp(environ, start_response)

    return replacement


def noauth(func):

    '''MVC @noauth decorator as a WSGI middleware application.
    @noauth prevents checking for user.  Used for "public" pages.
    '''
    
    def replacement(self, environ, start_response):
        self.require_auth = False
        return func(self, environ, start_response)

    return replacement
        
    

class Controller(object):

    '''MVC Controller for WSGI applications.
    Base class for MVC controllers.  Provides basic controller
    functionality, including credential checking, session management,
    and redirects.
    '''
    
    def __init__(self):

        self.session = None
        self.cookies = None
        self.user = None
        self.error = None

        self.require_auth = True


    def get_user(self, req):

        user = self.check_credentials(req)

        if user is None:
            user = self.check_session(req)

        return user


    def check_credentials(self, req):

        '''Check user credentials.
        For pages where authentication is required, check to see
        if user credentials have been passed in on the request.
        If credentials are present, initialize and return a User object.
        '''

        params = req.params
        user = None

        if 'user_id' in params:
            if 'password' in params:

                user_id = params['user_id']
                password = params['password']

                user = User.get_login_user(user_id, password)

        return user


    def check_session(self, req):

        '''Check session cookie.
        Check request for a session cookie.  If present, check the session
        for a valid user id.  If the user id is valid, initialize and return
        a User object.
        '''

        self.cookies = req.cookies

        if 'session' in self.cookies:
            self.session = Session.get_session(self.cookies['session'])

        if self.session is not None:

            user_id = self.session.uid
            self.user = User.get_user(user_id)

        return self.user
    

    def redirect(self, location):

        req = Request.blank('/', base_url=bivouac.base_url)
        e = exc.HTTPTemporaryRedirect(location=location)
        return req.get_response(e)


    def set_session(self, resp):

        self.session = Session()
        self.session.uid = self.user.id
        self.session.expires = datetime.datetime.now() + datetime.timedelta(days=1) 
        self.session.store()

        resp.set_cookie('session', self.session.id,
                        expires=self.session.expires)

        return self.session
