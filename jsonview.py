import json
import bivouac

class JSONView(bivouac.View):

    '''JSONView.
    A generic view to return JSON serialized objects.
    '''

    def __init__(self, model=None):

        bivouac.View.__init__(self, model)

        self.model = model


    def populate_template(self):

        return json.dumps(self.model)
