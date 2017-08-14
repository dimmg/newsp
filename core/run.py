import json

import tornado.ioloop
import tornado.web

from app import Application


class JSONHandler(tornado.web.RequestHandler):
    def jsonify(self, data):
        self.add_header('Content-Type', 'application/json')

        self.write(json.dumps(data, sort_keys=True, indent=4))


if __name__ == "__main__":
    Application().listen(5000, '0.0.0.0')
    tornado.ioloop.IOLoop.current().start()
