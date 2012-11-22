from string import Template


class TemplateNotFoundException(Exception):

    '''Exception raised when a template is not found within the
    projectli.st application.
    '''

    def __init__(self, value):
        self.value = value


    def __str__(self):
        return repr(self.value)



class TemplateCache(dict):

    _template_dir = '/Users/signal9/Projects/projectli.st/views/templates/'

    def __init__(self):
        dict.__init__(self)


    def load_template(self, template_name):

        '''Load a template from file into local cache.
        '''

        template_file = template_name + '.html'
        template_path = TemplateCache._template_dir + template_file

        try:
            with open(template_path) as template:
                temp = template.read()
                self[template_name] = Template(temp)
        except:
            raise TemplateNotFoundException('Template %s not found.' % template_name)

        return self[template_name]
        


    def get_template(self, template_name):

        '''Retrieve a template from cache, loading if necessary.
        '''

        if template_name in self:
            return self[template_name]
        return self.load_template(template_name)
