import tornado.web

from .common.database import init_motor_client
from .news import handlers as news_handlers
from .search import handlers as search_handlers
from .search.service import init_es_client


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/news', news_handlers.PostsHandler),
            (r'/news/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', news_handlers.PostsHandler),
            (r'/search', search_handlers.NewsSearchHandler)
        ]

        self.db = init_motor_client()

        self.es = init_es_client()

        settings = {
            'debug': True
        }

        tornado.web.Application.__init__(self, handlers, **settings)
