import json

import tornado.web


class JSONHandler(tornado.web.RequestHandler):
    """
    Base Request Handler.
    Every other handler should inherit this handler.
    
    Assures the process of returning JSON to the clients.
    """

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def write_json(self, data):
        self.write(json.dumps(data, sort_keys=True, indent=4))
