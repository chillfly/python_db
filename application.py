import os
import tornado.web
import config
from handlers import mongo, mysql


base_dir = os.path.dirname(os.path.abspath(__file__))

handlers = [
    (r"/mongo/(?P<resource>\w+)/?(?P<id>\w+)?", mongo.ResourceHandler),
    (r"/mysql/(?P<resource>\w+)/?(?P<id>\w+)?", mysql.ResourceHandler),

]

settings = {
    "debug": config.DEBUG,
}


class Application(tornado.web.Application):
    def __init__(self):
        global handlers, settings
        super().__init__(handlers=handlers, **settings)

