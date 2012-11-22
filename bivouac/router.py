import sys
import re
from pprint import pformat
from webob import Request, exc


class Router(object):

    '''MVC Router class for WSGI applications.
    '''

    route_regex = re.compile('{(\w+)(?::([^}]+))?\}')

    def __init__(self):
        self.routes = []


    def add_route(self, template, defaults=None, **vars):

        '''add_route() - Add a route mapping to the application.

        The routes member is a list of tuples where each tuple contains
        a compiled regex to match against the current URL, the Route object,
        and any supporting arguments.
        '''

        controller = Route(defaults)
        self.routes.append((re.compile(self.template_to_regex(template)),
                            controller,
                            vars))


    def __call__(self, environ, start_response):

        req = Request(environ)
        for regex, controller, vars in self.routes:
            match = regex.match(req.path_info)
            if match:
                req.urlvars = match.groupdict()
                req.urlvars.update(vars)
                return controller(environ, start_response)

        return exc.HTTPNotFound()(environ, start_response)


    def template_to_regex(self, template):

        regex = ''
        last_pos = 0

        for match in Router.route_regex.finditer(template):
            regex += re.escape(template[last_pos:match.start()])
            name = match.group(1)
            expr = match.group(2) or '[^/]+'
            expr = '(?P<%s>%s)' % (name, expr)
            regex += expr
            last_pos = match.end()

        regex += re.escape(template[last_pos:])
        regex = '^%s$' % regex
        return regex


class Route(object):

    '''MVC Route class for WSGI applications.
    '''
    
    def __init__(self, defaults=None):
        self.defaults = defaults


    def __call__(self, environ, start_response):

        req = Request(environ)

        if 'controller' in req.urlvars:
            controller = req.urlvars['controller'].lower()
        else:
            controller = self.defaults['controller'].lower()
        controller = self.load_controller(controller)

        if 'action' in req.urlvars:
            action = req.urlvars['action']
        else:
            action = self.defaults['action']
        action = getattr(controller, action)
        
        return action(environ, start_response)


    def load_controller(self, module_name):

        __import__(module_name)
        module = sys.modules[module_name]
        controller_name = getattr(module, 'controller')
        controller = getattr(module, controller_name)

        return controller()
