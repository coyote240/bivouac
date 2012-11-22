====================================================================
bivouac - a light-weight, wsgi-compliant MVC web framework in Python
====================================================================

Why bivouac?
------------

bivouac has grown out of my own efforts to build websites in Python with as thin a footprint as I can.  bivouac provides a basic MVC framework inspired by Microsoft's MVC 1.0 framework.  Expect further ruminations on the topic elsewhere.  In the past I suggested I would not support this project, but as I find I rely on bivouac for more of my own websites, I expect to do as much as I can to encourage adoption and support. I think we're on to something good here!

What is bivouac?
----------------

bivouac is WSGI compliant and aims to be as webserver-agnostic as it can.  Using mod_wsgi or isapi_wsgi, bivouac works well with both Apache and IIS, with NGINX being an untested likelihood.  Today bivouac supports authentication and user sessions using MongoDB.  Long-term look for this to become more database independent.

Currently, bivouac has a small number of dependencies:

* mod_wsgi or isapi_wsgi
* Paste & Webob
* mongodb
* PyMongo

Basic Usage
-----------

bivouac provides classes for MVC routing, controllers, models and views.  Here's a quick intro to getting a site up and running using bivouac.

For starters, create a module called app.py, or whatever you've specified as your WSGI entry point.  Here we see a simple WSGI entry point with some boiler-plate routing.  This will serve most folks needs, so feel free to start with this setup.
    

    import bivouac

    application = bivouac.Router()
    application.add_route('/', defaults={'controller': 'default', 'action': 'index'})
    application.add_route('/{controller}/', defaults={'action': 'index'})
    application.add_route('/{controller}/{action}')
    application.add_route('/{controller}/{action}/{id}')


Next you'll need a controller.  bivouac looks for controllers within your site directory, typically in the controllers package.  Your controller will inherit from bivouac.Controller.  Methods decorated with @action will be treated as controller actions and return bivouac views, or any WSGI compliant, iterable structure.


    import bivouac
    from bivouac.controller import action, noauth

    controller = "DefaultController"

    class DefaultController(bivouac.Controller):

        '''Default Controller.
        '''

        def __init__(self):

            bivouac.Controller.__init__(self)


        @noauth
        @action
        def index(self, req, **vars):

            import views.index as View

            view = View.IndexView()
            return view

