import sys
from xml.dom.minidom import parse
from webob import Request, Response, exc

class View(object):


    def __init__(self, model):
        
        self.model = model
        self.scripts = []
        self.styles = []


    def populate_template(self):
        
        raise NotImplementedError('Method not implemented by inheriting class.')


    @property
    def Model(self):
        
        return self.model;


    @Model.setter
    def Model(self, model):

        self.model = model;


    def __call__(self, environ, start_response):
        
        output = self.populate_template()
        resp = Response(body=output)
        return resp(environ, start_response)


    def __str__(self):
        return self.populate_template()
