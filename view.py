import sys
from xml.dom.minidom import parse
from webob import Request, Response, exc
from template import TemplateCache

class View(object):


    def __init__(self, model):
        
        self.model = model
        self.cache = TemplateCache()


    def populate_template(self):
        
        raise NotImplementedError('Method not implemented by inheriting class.')


    def __call__(self, environ, start_response):
        
        output = self.populate_template()
        resp = Response(body=output)
        return resp(environ, start_response)


    def __str__(self):
        return self.populate_template()
